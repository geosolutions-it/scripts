# Installation

```
git clone git@github.com:geosolutions-it/scripts.git
cd scripts/utils/upgrade-to-jndi
pip install -r requirements.txt
```

# Use it


This example assumes that mosaic configuration (coverages) is placed in `/var/geoserver/datadir/data` 
point it to the correct directory for your environment.

```
python3 ./upgrade-jndi-datastores.py --datadir /var/geoserver/datadir --coverages /var/geoserver/datadir/data/
```


# Files produced

- ./context.xml
- edited datadir datastore confiogurations (datastore.properties, netcdf_datastore.properties, datastore.xml)
- backed up files (datastore.properties, netcdf_datastore.properties, datastore.xml)

