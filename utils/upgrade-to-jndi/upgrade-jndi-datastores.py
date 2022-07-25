import os
import re
import argparse
import logging
from iteration_utilities import *
import mmap
from jinja2 import Environment, FileSystemLoader
import lxml.etree as le

#location of templates
ENV = Environment(loader=FileSystemLoader('.'))

#load the template file
template= ENV.get_template("context.xml.j2")

mosaics_connections_factor = 5
vector_connections_factor = 20
# Script arguments handling

parser = argparse.ArgumentParser(description='Update GeoServer database connection pool to JNDI for PostgreSQL')

parser.add_argument('--datadir', nargs=1,
                    help='GeoServer datadir path')
parser.add_argument('--coverages', nargs=1,
                    help='Coverages configuration path')

args = parser.parse_args()


# Creating classes to manipulate the logs.
class AppFilter(logging.Filter):
    filter_name = ""

    def filter(self, record):
        record.app_name = self.filter_name
        return True


class OneLineExceptionFormatter(logging.Formatter):
    def formatException(self, exc_info):
        result = super().formatException(exc_info)
        return repr(result)

    def format(self, record):
        result = super().format(record)
        if record.exc_text:
            result = result.replace("\n", "")
        return result




def check_stores():
    configs_list = []
    mosaic_final_configs = []
    vector_final_configs = []
    count_mosaics = 0
    count_mosaics_connections = 0
    jndi_connection_id = 0
    for root, subdirs, files in os.walk(args.coverages[0]):
        for f in files:
            db_config = {}
            if re.match(r'datastore\.properties$', f):
                #I count mosaics,netcdf datastore will be eventually adapted to jndi.
                count_mosaics = count_mosaics + 1
                filename=open(os.path.join(root, f))
                for line in filename:
                    if 'host=' in line:
                        db_config["host"] = line.replace("host=","").replace("\n","")
                    if 'user=' in line:
                        db_config["user"] = line.replace("user=","").replace("\n","")
                    if 'passwd=' in line:
                        db_config["pass"] = line.replace("passwd=","").replace("\n","")
                    if 'database=' in line:
                        db_config["database"] = line.replace("database=","").replace("\n","")
                    # if 'schema=' in line:
                    #     db_config["schema"] = line.replace("schema=","").replace("\n","")
                if db_config not in configs_list and db_config != {}:
                    configs_list.append(db_config)


    for db_config in configs_list:
        match = 0
        count_mosaics_max_connections = 0
        count_mosaics_min_connections = 0
        # count mosaics per configuration, this will make an average number min connections
        for root, subdirs, files in os.walk(args.coverages[0]):
            for f in files:
                if re.match(r'datastore\.properties$', f):
                    filename=open(os.path.join(root, f))
                    for line in filename:
                        if db_config["host"] in line:
                            count_mosaics = count_mosaics + 1


        # count connections per configuration
        for root, subdirs, files in os.walk(args.coverages[0]):
            for f in files:
                if re.match(r'datastore\.properties$', f):
                    with open(os.path.join(root, f)) as current_file:
                        if re.findall('^(host='+ db_config["host"] + '|' + "max\ connections=" + ')$',current_file.read(),re.MULTILINE):
                            coverage_datastore_properties = open(os.path.join(root, f))
                            for line in coverage_datastore_properties:
                                if "max\ connections=" in line:
                                    count_mosaics_max_connections = count_mosaics_max_connections + int(line.replace("max\ connections=","").replace("\n",""))
                        else:
                            count_mosaics_max_connections = count_mosaics_max_connections + 1
                        if re.findall('^(host='+ db_config["host"] + '|' + "min\ connections=" + ')$',current_file.read(),re.MULTILINE):
                            coverage_datastore_properties = open(os.path.join(root, f))
                            for line in coverage_datastore_properties:
                                if "min\ connections=" in line:
                                    count_mosaics_min_connections = count_mosaics_min_connections + int(line.replace("min\ connections=","").replace("\n",""))
                        else:
                            count_mosaics_min_connections = count_mosaics_min_connections + 1
        db_config["max_conn"] = count_mosaics_max_connections
        db_config["min_conn"] = count_mosaics_min_connections

        if db_config["max_conn"] == 0:
            db_config["max_conn"] = 10 * db_config["min_conn"]
        db_config["name"] = "geoserver-mosaics-jndi-" + str(jndi_connection_id)
        mosaic_final_configs.append(db_config)

        # Increment jndi id to differentiate

        jndi_connection_id += 1


    #empty configs list for vectors
    jndi_connection_id = 0
    configs_list = []
    for root, subdirs, files in os.walk(os.path.join(args.datadir[0] + "/workspaces")):
        for f in files:
            db_config = {}
            if re.match(r'datastore\.xml$', f):
                for line in open(os.path.join(root, f)):
                    if re.findall('<type>PostGIS</type>',line):
                        continue
                    else:
                        break
                with open(os.path.join(root, f) + '-backup', 'w') as backup_datastore:
                    for line in open(os.path.join(root, f)):
                        backup_datastore.write(line)
                        if "<entry key=\"host\">" in line:
                            db_config["host"]=line.replace("<entry key=\"host\">","").replace('</entry>',"").replace('\n',"").replace(" ","")

                            # if '${' not in database_hostname:
                            #     db_config["host"]=database_hostname
                            # else:
                            #     logger.info('skipping this vector datastore as the db hostname is defined by a variable')
                            #     break
                        if "<entry key=\"user\">" in line:
                            db_config["user"]=line.replace("<entry key=\"user\">","").replace('</entry>',"").replace('\n',"").replace(" ","")
                        if "<entry key=\"passwd\">" in line:
                            if not 'crypt1:' in line:
                                db_config["pass"]=line.replace("<entry key=\"passwd\">","").replace('</entry>',"").replace('\n',"").replace(" ","")
                            else:
                                db_config["pass"]='DUMMY_PASS_ORIGINAL_WAS_ENCRYPTED'
                        if "<entry key=\"port\">" in line:
                            db_config["port"]=line.replace("<entry key=\"port\">","").replace('</entry>',"").replace('\n',"").replace(" ","")
                        if "<entry key=\"database\">" in line:
                            db_config["database"]=line.replace("<entry key=\"database\">","").replace('</entry>',"").replace('\n',"").replace(" ","")
                        # if "<entry key=\"schema\">" in line:
                            # db_config["schema"]=line.replace("<entry key=\"schema\">","").replace('</entry>',"").replace('\n',"").replace(" ","")
            if db_config not in configs_list and db_config != {}:
                configs_list.append(db_config)

    for db_config in configs_list:
        match = 0
        # Do Vector datastores
        count_vectors_max_connections = 0
        count_vectors_min_connections = 0

        for root, subdirs, files in os.walk(os.path.join(args.datadir[0] + "/workspaces")):
            for f in files:
                if re.match(r'datastore\.xml$', f):
                    with open(os.path.join(root, f)) as current_file:
                        if re.findall('<type>PostGIS</type>',line):
                            continue
                        else:
                            break
                        if re.findall('(schema=' + db_config[schema] + '| host='+ db_config["host"] + '|' + 'max\ connections' + ')',current_file.read(),re.MULTILINE):
                            for line in current_file:
                                if "max connections=" in line:
                                    count_vectors_max_connections = count_vectors_max_connections + int(line.replace("<entry key=\"max connections\">","").replace("\n","").replace(" ","").replace('</entry>',""))
                        else:
                            count_vectors_max_connections = count_vectors_max_connections + 1
                        if re.findall('(schema=' + db_config[schema] + '| host='+ db_config["host"] + '|' + "min\ connections" + ')$',current_file.read(),re.MULTILINE):
                            for line in current_file:
                                if "min connections=" in line:
                                    count_vectors_min_connections = count_vectors_min_connections + int(line.replace("<entry key=\"min connections\">","").replace("\n","").replace(" ","").replace('</entry>',""))
                        else:
                            count_vectors_min_connections = count_vectors_min_connections + 1
        db_config["max_conn"] = count_vectors_max_connections
        db_config["min_conn"] = count_vectors_min_connections
        if db_config["max_conn"] == 0:
            db_config["max_conn"] = 10 * db_config["min_conn"]
        db_config["name"] = "geoserver-vectors-jndi-" + str(jndi_connection_id)
        vector_final_configs.append(db_config)

        # Increment jndi id to differentiate

        jndi_connection_id += 1

    return mosaic_final_configs, vector_final_configs



def build_context(configs_list):
    with open("./context.xml", "w") as context:
        context.write(template.render(configs_list=configs_list))
        logger.info('Context file for tomcat saved in current directory: ./context.xml')

def edit_mosaic_datastore(config={}):

    for root, subdirs, files in os.walk(args.coverages[0]):
        for f in files:
            if re.match(r'datastore\.properties$', f):
                filename=os.path.join(root, f)
                filename_backup= filename + '-backup'
                with open(filename_backup, 'w') as backup:
                    for line in open(filename):
                        backup.write(line)
                check_db_host = open(filename_backup, 'r')
                if re.findall('(' + config["database"] + '|' + config["host"] + '|' + config["user"] + ')', check_db_host.read(),re.MULTILINE):
                    logger.info('yay matched!')
                # if config["host"] in check_db_host.read() and config["user"] in check_db_host.read() and config["database"] in check_db_host.read():
                    with open(filename, 'w') as new_datastore:
                        for line in open(filename_backup, 'r'):
                            if 'schema=' in line:
                                new_datastore.write(line)
                            elif 'Estimated\ extends=' in line:
                                new_datastore.write(line)
                            elif 'Loose\ bbox' in line:
                                new_datastore.write(line)
                            elif 'preparedStatements=' in line:
                                new_datastore.write(line)
                        new_datastore.write('SPI=org.geotools.data.postgis.PostgisNGJNDIDataStoreFactory' + "\n")
                        new_datastore.write("jndiReferenceName=java:comp/env/" + "jdbc/datastore" + config["name"] + "\n")

    for root, subdirs, files in os.walk(args.coverages[0]):
        for f in files:
            if re.match(r'netcdf_datastore\.properties$', f):
                filename=os.path.join(root, f)
                filename_backup=filename + '-backup'
                with open(filename_backup, 'w') as backup:
                    for line in open(filename):
                        backup.write(line)
                # for line in open(filename_backup, 'r'):
                #     if config["host"] in line:
                check_db_host = open(filename_backup, 'r')
                if re.findall('(' + config["database"] + '|' + config["host"] + '|' + config["user"] + ')', check_db_host.read(),re.MULTILINE):
                    with open(filename, 'w') as new_datastore:
                        for line in open(filename_backup, 'r'):
                            if 'schema=' in line:
                                new_datastore.write(line)
                            elif 'Estimated\ extends=' in line:
                                new_datastore.write(line)
                            elif 'Loose\ bbox' in line:
                                new_datastore.write(line+"\n")
                            elif 'preparedStatements=' in line:
                                new_datastore.write(line+"\n")
                        new_datastore.write('SPI=org.geotools.data.postgis.PostgisNGJNDIDataStoreFactory' + "\n")
                        new_datastore.write("jndiReferenceName=java:comp/env/" + "jdbc/datastore" + config["name"] + "\n")

def edit_vector_datastore(config={}):

    for root, subdirs, files in os.walk(os.path.join(args.datadir[0] + "/workspaces")):
        for f in files:
            if re.findall(r'datastore\.xml$', f):
                filename_backup=os.path.join(root, f) + '-backup'
                fopen=open(filename_backup)
                doc=le.parse(filename_backup)
                if re.findall('(' + config["database"] + '|' + config["host"] + '|' + config["user"] + ')', fopen.read(),re.MULTILINE):
                    tag_type=doc.find('type')
                    tag_type.text = 'PostGIS (JNDI)'
                    tag_entry = doc.find("connectionParameters/entry")
                    new_tag_entry = le.SubElement(tag_entry, "entry")
                    new_tag_entry.attrib['key'] = 'jndiReferenceName'
                    new_tag_entry.text = 'java:comp/env/' + 'jdbc/datastore' + config["name"]
                    tag_entry.addnext(new_tag_entry)
                    for elem in doc.xpath('//*[attribute::key]'):
                        if elem.attrib['key']=='host':
                            parent=elem.getparent()
                            parent.remove(elem)
                        if elem.attrib['key']=='passwd':
                            parent=elem.getparent()
                            parent.remove(elem)
                        if elem.attrib['key']=='user':
                            parent=elem.getparent()
                            parent.remove(elem)
                        if elem.attrib['key']=='database':
                            parent=elem.getparent()
                            parent.remove(elem)
                        if elem.attrib['key']=='port':
                            parent=elem.getparent()
                            parent.remove(elem)
                        if elem.attrib['key']=='Evictor run periodicity':
                            parent=elem.getparent()
                            parent.remove(elem)
                        if elem.attrib['key']=='Max open prepared statements':
                            parent=elem.getparent()
                            parent.remove(elem)
                        if elem.attrib['key']=='validate connections':
                            parent=elem.getparent()
                            parent.remove(elem)
                        if elem.attrib['key']=='Connection timeout':
                            parent=elem.getparent()
                            parent.remove(elem)
                        if elem.attrib['key']=='SSL mode':
                            parent=elem.getparent()
                            parent.remove(elem)
                        if elem.attrib['key']=='schema':
                            parent=elem.getparent()
                            parent.remove(elem)
            # add JNDI string jndiReferenceName java:comp/env/jdbc/jndiReferenceName


            # print(le.tostring(doc))
            # logger.info(original_datastore)
                    doc.write(os.path.join(root, f), pretty_print=True, xml_declaration=False, encoding="utf-8")


# def rollback()

# Enable Logging
layer_name = []
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(app_name)s %(levelname)s:%(message)s')
handler = logging.StreamHandler()
formatter = OneLineExceptionFormatter(logging.BASIC_FORMAT)
handler.setFormatter(formatter)
logger = logging.getLogger(layer_name)
logger.setLevel(os.environ.get("LOGLEVEL", "INFO"))
filter = AppFilter()
logger.addFilter(filter)

#
configs_mosaics,configs_vectors = check_stores()
build_context(configs_mosaics + configs_vectors)

for config in configs_mosaics:
    edit_mosaic_datastore(config)

for config in configs_vectors:
    edit_vector_datastore(config)