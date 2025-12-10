from flask import Blueprint, request, jsonify
import sqlite3

bp = Blueprint('api', __name__)

def get_db():
    conn = sqlite3.connect("hotel.db")
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

@bp.route('/room', methods=['GET'])
def get_rooms():
    check_in = request.args.get("checkIn")
    check_out = request.args.get("checkOut")
    guests_num = request.args.get("guestsNum")

    conn = get_db()
    cursor = conn.cursor()

    if check_in and check_out and guests_num:
        cursor.execute("""
            SELECT * FROM rooms r
            WHERE r.guestNum >= ?
            AND r.roomId NOT IN (
                SELECT b.roomId FROM bookings b
                WHERE NOT (b.checkOut <= ? OR b.checkIn >= ?)
            )
        """, (int(guests_num), check_in, check_out))
    else:
        cursor.execute("SELECT * FROM rooms")

    rows = cursor.fetchall()
    conn.close()

    rooms = []
    for row in rows:
        rooms.append({
            "roomId": row["roomId"],
            "floor": row["floor"],
            "beds": row["beds"],
            "guestNum": row["guestNum"],
            "price": row["price"]
        })

    return jsonify({"rooms": rooms}), 200

@bp.route('/add-room', methods=['POST'])
def add_room():
    data = request.get_json()
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO rooms (floor, beds, guestNum, price)
        VALUES (?, ?, ?, ?)
    """, (data['floor'], data['beds'], data['guestNum'], data['price']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Room added successfully"}), 200

@bp.route('/booking', methods=['POST'])
def book_room():
    data = request.get_json()
    room_id = data['roomId']
    check_in = str(data['bookingDates']['checkIn'])
    check_out = str(data['bookingDates']['checkOut'])

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM bookings WHERE roomId = ?
        AND NOT (checkOut <= ? OR checkIn >= ?)
    """, (room_id, check_in, check_out))
    if cursor.fetchone():
        conn.close()
        return jsonify({"error": "Room already booked"}), 409

    cursor.execute("""
        INSERT INTO bookings (roomId, checkIn, checkOut)
        VALUES (?, ?, ?)
    """, (room_id, check_in, check_out))
    conn.commit()
    conn.close()
    return jsonify({"message": "Booking successful"}), 200