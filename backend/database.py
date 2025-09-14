from sqlalchemy import create_engine, MetaData
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@postgres:5432/production_db")
engine = create_engine(DATABASE_URL)
metadata = MetaData()

def get_database_schema():
    metadata.reflect(bind=engine)
    return [
        {
            'table_name': table_name,
            'columns': [
                {
                    'name': col.name,
                    'type': str(col.type),
                    'primary_key': col.primary_key
                }
                for col in table.columns
            ]
        }
        for table_name, table in metadata.tables.items()
    ]