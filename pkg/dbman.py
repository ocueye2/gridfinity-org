import sqlite3
from contextlib import contextmanager

@contextmanager
def connect():
    '''Makes connection and cursor for interacting with the database'''
    conn = sqlite3.connect("main.db")
    cursor = conn.cursor()
    try:
        yield conn, cursor  
    finally:
        conn.commit()  
        conn.close()   

# Initialize the database
with connect() as (conn, cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS plates (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE,
            x INTEGER,
            y INTEGER
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE,
            x INTEGER,
            y INTEGER,
            plate TEXT
        )   
    """)

def create(type,name,x,y,plate=None):
    with connect() as (conn, cursor):
        if type == "items":
             cursor.execute(f"INSERT INTO {type} (name, x, y, plate) VALUES (?, ?, ?, ?)", 
                       (name,x,y,plate))
        else:
            cursor.execute(f"INSERT INTO {type} (name, x, y) VALUES (?, ?, ?)", 
                       (name,x,y))

def lookup(name):
    with connect() as (conn, cursor):
        cursor.execute("SELECT name FROM items WHERE name LIKE ?", ("%" + name + "%",))
        result = cursor.fetchall()  
        return [row[0] for row in result] 

def listplates():
    with connect() as (conn, cursor):
        cursor.execute("SELECT name FROM plates")
        results = cursor.fetchall()
        print(results)
        return [row[0] for row in results]  

def platedata(name):
     with connect() as (conn, cursor):
        cursor.execute("SELECT x, y FROM plates WHERE name = ?", (name,))
        result = cursor.fetchone()
        if result:
            return result[0], result[1]  # Return x and y
        else:
            return None, None  # Return None if plate is not found

def getplate(name):
    with connect() as (conn, cursor):
        cursor.execute("SELECT plate FROM items WHERE name = ?", (name,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return None 

def itemdata(name):
     with connect() as (conn, cursor):
        cursor.execute("SELECT x, y FROM items WHERE name = ?", (name,))
        result = cursor.fetchone()
        if result:
            return result[0], result[1]  # Return x and y
        else:
            return None, None  # Return None if plate is not found

def delete(name,type):
    with connect() as (conn, cursor):
        if type == "item":
            cursor.execute("DELETE FROM items WHERE name= ?", (name,))
        elif type == "plate":
            cursor.execute("DELETE FROM plates WHERE name = ?", (name,))
            cursor.execute("DELETE FROM items WHERE plate = ?", (name,))
