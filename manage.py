import sqlite3
conn = sqlite3.connect('PoliceNote.sqlite3')

cursor = conn.cursor()


cursor.execute("""
Create Table PoliceMan(
Id integer primary key,
Officer_name text not null,
Reason text not null,
Thought text not null
)
""")