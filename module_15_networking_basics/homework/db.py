import sqlite3

def get_db():
    conn = sqlite3.connect("hotel.db")   # база в файле
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rooms (
            roomId INTEGER PRIMARY KEY AUTOINCREMENT,
            floor INTEGER,
            beds INTEGER,
            guestNum INTEGER,
            price INTEGER
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            bookingId INTEGER PRIMARY KEY AUTOINCREMENT,
            roomId INTEGER,
            checkIn TEXT,
            checkOut TEXT
        )
    """)
    conn.commit()
    conn.close()