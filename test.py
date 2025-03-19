import sqlite3

def createTable(tableName, columns):
    conn = sqlite3.connect("Servify.db")
    cursor = conn.cursor()
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS {tableName} ({columns})""")
    conn.commit()
    conn.close()
    
def replaceTable(newTable, newColumns, oldTable, oldColumns):
    createTable(newTable, newColumns)
    
    conn = sqlite3.connect("Servify.db")
    cursor = conn.cursor()
    cursor.execute(f"""INSERT INTO {newTable} ({newColumns}) 
                   SELECT {oldColumns} FROM {oldTable}""")
    conn.commit()
    
    # delete oldTable
    cursor.execute(f"""DROP TABLE IF EXISTS {oldTable}""")
    conn.commit()
    
    # rename new table to the name of oldTable
    cursor.execute(f"""ALTER TABLE {newTable} RENAME TO {oldTable}""")
    conn.commit()
    
    conn.close()

def renameTable(referencedTable, otherTable):
    conn = sqlite3.connect("Servify.db")
    cursor = conn.cursor()
    cursor.execute(f"""ALTER TABLE {referencedTable} RENAME TO {otherTable}""")
    conn.commit()
    conn.close()

def dropTable(tableName):
    conn = sqlite3.connect("Servify.db")
    cursor = conn.cursor()
    cursor.execute(f"""DROP TABLE IF EXISTS {tableName}""")
    conn.commit()
    conn.close()

def alterTable(tableName, newColumn):
    conn = sqlite3.connect("Servify.db")
    cursor = conn.cursor()
    
    alter_query = f"""ALTER TABLE {tableName} ADD COLUMN {newColumn}"""
    
    cursor.execute(alter_query)
    conn.commit()
    conn.close()

def deleteRow(tableName, column, referenceId):
    conn = sqlite3.connect("Servify.db")
    cursor = conn.cursor()
    cursor.execute(f"""DELETE FROM {tableName} WHERE {column} = ?""", (referenceId,))
    conn.commit()
    conn.close()

# newColumn = """EventId INTEGER PRIMARY KEY, 
# title TEXT NOT NULL, 
# description TEXT NOT NULL, 
# date TEXT NOT NULL, 
# venue TEXT NOT NULL, 
# status TEXT NOT NULL, 
# publisher TEXT NOT NULL, 
# publisherId INTEGER, 
# publishedSince TEXT NOT NULL, 
# currParticipants INTEGER NOT NULL DEFAULT 0, 
# maxParticipants INTEGER NOT NULL DEFAULT 0,
# FOREIGN KEY (publisherId) REFERENCES USERS(UserId)"""

# columns = """ReferenceId INTEGER PRIMARY KEY,
# UserId INTEGER,
# interest TEXT NOT NULL,
# FOREIGN KEY (UserId) REFERENCES USERS(UserId)
# """

# columns = """UserId INTEGER PRIMARY KEY,
# username TEXT NOT NULL,
# password TEXT NOT NULL,
# email TEXT NOT NULL,
# aboutMe TEXT NOT NULL,
# creationDate TEXT NOT NULL,
# lastActive TEXT NOT NULL,
# services TEXT NOT NULL,
# role TEXT NOT NULL
# """
# dropTable("USERS")
# createTable("USERS", columns)

deleteRow("EVENTS","EventId",1)


