# Satellite Crops

🌱 Land parcels segmentation and crops identification from satellite images 🛰️


- 9 778 397 parcels annotated each year on 10 years
- 10m resolution picture of France per month (5 439 400 000 pixels ! per month)
- 23 groups of crop

## Setup satellitecrops package
A la racine du repo, executer la commande suivante :
`pip install .`

Les variables d'environnement sont accessibles via `from satellitecrops.params import *`

## Utils
### SQLConnection

`from satellitecrops.utils.sql_connector import SQLConnection`
# Data sources

https://geoservices.ign.fr/telechargement-api/RPG
GPKG are SQLite files
