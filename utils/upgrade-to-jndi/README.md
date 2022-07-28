# upgrade-jndi-datastores.py
## Installation of requirements and code checkout

```bash
#Install pyenv
curl https://pyenv.run | bash
exec $SHELL
pyenv install 3.10.5
pyenv global 3.10.5
python3 -m venv ~/venv/upgrade-to-jndi
source ~/venv/upgrade-to-jndi/bin/activate
git clone git@github.com:geosolutions-it/scripts.git
cd scripts/utils/upgrade-to-jndi
pip3 install -r requirements.txt
```

## Use it

This example assumes that mosaic configuration (coverages) is placed in `/var/geoserver/datadir/data`
point it to the correct directory for your environment.

```bash
python3 ./upgrade-jndi-datastores.py --datadir /var/geoserver/datadir --coverages /var/geoserver/datadir/data/
```

## Files produced

- a `context.xml` file for Apache Tomcat is generated.
- edited datadir datastore configurations (datastore.properties, netcdf_datastore.properties, datastore.xml) are put in place of previous ones.
- backed up files for each datastore (datastore.properties-backup, netcdf_datastore.properties-backup, datastore.xml-backup) can be found along the modified file.
