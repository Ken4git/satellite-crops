from satellitecrops.params import *
from google.cloud.sql.connector import Connector, IPTypes
from geopandas.geoseries import GeoSeries

import sqlalchemy

class SQLConnection:

    def __init__(self):
        """
        Initializes a connection pool for a Cloud SQL instance of Postgres.

        Uses the Cloud SQL Python Connector package.
        """
        connector = Connector(IPTypes.PUBLIC)

        def getconn():
            conn = connector.connect(
                DB_INSTANCE,
                "pg8000",
                user=DB_USER,
                password=DB_PASS,
                db=DB_NAME,
            )
            return conn

        self.engine = sqlalchemy.create_engine(
            "postgresql+pg8000://",
            creator=getconn,
        )
        self.db_conn = self.engine.connect()


    def select(self: object, query: str) -> list:
        """SQL select query on postgres

        Args:
            query (str): SELECT statement

        Returns:
            list: SELECT results
        """
        return self.db_conn.execute(
            sqlalchemy.text(query)
        ).fetchall()


    def get_parcelles_in_bbox(self: object, geometry: GeoSeries, crs: str) -> list:
        """Get the parcelles contained in the bounding box passed as
        bbox argument. Converts the polygon to the givien crs

        Args:
            geometry (GeoSeries): coordinates of the search zone

            crs (str): CRS code for conversion

        Returns:
            list: All the parcelles contained in the bbox
        """
        query = """
        SELECT * FROM parcelles_graphiques
        WHERE geom && ST_MakeEnvelope(:minx, :miny, :maxx, :maxy, :crs)"""

        bounds = geometry.bounds

        params = dict(
            minx=bounds.minx[0],
            miny=bounds.miny[0],
            maxx=bounds.maxx[0],
            maxy=bounds.maxy[0],
            crs=crs
        )

        return self.db_conn.execute(
            sqlalchemy.text(query), params).fetchall()

if __name__ == "__main__":
    connector = SQLConnection()
    res = connector.select("""
                     SELECT * FROM parcelles_graphiques LIMIT 1
                     """)
    print(res)
