import sqlite3

Database = sqlite3.Connection


def get_database() -> Database:
    database = sqlite3.connect("data/doorbell_faces.db")

    database.execute("""
      CREATE TABLE IF NOT EXISTS person (
        person_id INTEGER PRIMARY KEY,
        name STRING TEXT NULL)
    """)

    database.commit()

    return database


