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

https://geoservices.ign.fr/telechargement-api/RPG
GPKG are SQLite files
