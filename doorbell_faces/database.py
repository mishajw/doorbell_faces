import sqlite3

Database = sqlite3.Connection


def get_database() -> Database:
    database = sqlite3.connect("data/doorbell_faces.db")

    database.execute("""
      CREATE TABLE IF NOT EXISTS person (
        person_id INTEGER PRIMARY KEY,
        name STRING TEXT NULL)
    """)

    database.execute("""
      CREATE TABLE IF NOT EXISTS capture (
        capture_id INTEGER PRIMARY KEY,
        time INTEGER,
        hash TEXT)
    """)

    database.execute("""
      CREATE TABLE IF NOT EXISTS recognition (
        person_id INTEGER,
        capture_id INTEGER,
        face_embedding BLOB,
        FOREIGN KEY (person_id) REFERENCES person(person_id),
        FOREIGN KEY (capture_id) REFERENCES capture(capture_id),
        PRIMARY KEY (person_id, capture_id))
    """)

    database.commit()

    return database


