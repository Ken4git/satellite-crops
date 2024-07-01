# Satellite Crops

🌱 Land parcels segmentation and crops identification from satellite images 🛰️


- 9 778 397 parcels annotated each year on 10 years
- 10m resolution picture of France per month (5 439 400 000 pixels ! per month)
- 23 groups of crop

## Setup satellitecrops package
For installing the package, run the following command in the root of the repo :
```bash
pip install {-e} .
# -e only in developper mode
```

### Environnement variables
Secrets and connection logs are stored as environnement variables.

Please use `.env` file to set them. You can use the `.env.sample`. If you add any variable mandatory to run the package please update the `.env.sample` file and add the reference in the `satellitecrops/params.py` file.

If you want to load the environnement variables in a `python file`, import them like so
```python
from satellitecrops.params import *
```


## Utils
### SQLConnection

```python
from satellitecrops.utils.sql_connector import SQLConnection

# Instanciate connector object
conn = SQLConnection()

# Write SQL query
# This is a test query for getting first row of db
query = """
  SELECT * FROM parcelles_graphiques LIMIT 1
"""

# Send request and store result in res variable
res = conn.select(query)

```


# Data sources
## French agricultural parcels as declared to EU 
- Description of data:
GPKG are SQLite files
- How to get it:
https://geoservices.ign.fr/telechargement-api/RPG

## Satellite images from Sentinel2 
- Description of data: Satellite documents used are *Sentinel-2 Cloud-Optimized GeoTIFFs*. Each satellite view (a certain location at a certain date) is stored as a folder containing images from different spectral bandwidths and a description file.
- How to get it: [Element 84 search API](https://earth-search.aws.element84.com/v1/search) returns as results, a list of URLs to satellite documents corresponding to the query. The satellite documents are then downloaded directly in a Google Bucket.
  
## Regional/departemental production per crop (France)
- Description of data:
- How to get it:
