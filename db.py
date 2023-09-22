import sqlite3

conn = sqlite3.connect("/data/parser.db")
cursor = conn.cursor()

cursor.execute("""CREATE TABLE entities
                  (title text, date text)
               """)