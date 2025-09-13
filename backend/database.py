from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, TIMESTAMP, ForeignKey, Boolean
from sqlalchemy.engine.url import URL
from sqlalchemy import text
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/production_db")

engine = create_engine(DATABASE_URL)
metadata = MetaData()


def get_database_schema():
    """Получает схему БД и возвращает список таблиц с колонками"""
    metadata.reflect(bind=engine)
    schema = []

    for table_name in metadata.tables:
        table = metadata.tables[table_name]
        columns_info = []

        for column in table.columns:
            col_info = {
                'name': column.name,
                'type': str(column.type),
                'nullable': column.nullable,
                'primary_key': column.primary_key
            }
            columns_info.append(col_info)

        schema.append({
            'table_name': table_name,
            'columns': columns_info
        })

    return schema


def get_procedures_and_triggers():
    """Получает информацию о процедурах и триггерах"""
    procedures = []
    triggers = []

    # Получение процедур
    try:
        with engine.connect() as conn:
            # Для PostgreSQL
            result = conn.execute(text("""
                SELECT proname as name, pg_get_functiondef(p.oid) as definition 
                FROM pg_proc p 
                WHERE p.pronamespace = (SELECT oid FROM pg_namespace WHERE nspname = 'public')
            """))
            for row in result:
                procedures.append({
                    'name': row['name'],
                    'definition': row['definition']
                })
    except Exception as e:
        print(f"Error getting procedures: {e}")

    # Получение триггеров
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT tgname as name, pg_get_triggerdef(t.oid) as definition 
                FROM pg_trigger t 
                WHERE NOT tgisinternal
            """))
            for row in result:
                triggers.append({
                    'name': row['name'],
                    'definition': row['definition']
                })
    except Exception as e:
        print(f"Error getting triggers: {e}")

    return procedures, triggers