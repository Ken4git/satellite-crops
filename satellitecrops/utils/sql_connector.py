from satellitecrops.params import *
from google.cloud.sql.connector import Connector, IPTypes

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


if __name__ == "__main__":
    connector = SQLConnection()
    res = connector.select("""
                     SELECT * FROM parcelles_graphiques LIMIT 1
                     """)
    print(res)
