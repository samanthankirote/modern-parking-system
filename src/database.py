import sqlite3
from pathlib import Path


# Find the project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Database file location
DATABASE_PATH = BASE_DIR / "database" / "parking_system.db"


def get_connection():
    """Create and return a connection to the SQLite database."""
    connection = sqlite3.connect(DATABASE_PATH)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database():
    """Create all database tables and insert initial data."""

    connection = get_connection()
    cursor = connection.cursor()

    # Vehicles table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vehicles (
            vehicle_id INTEGER PRIMARY KEY AUTOINCREMENT,
            registration_no TEXT NOT NULL UNIQUE,
            vehicle_type TEXT NOT NULL,
            owner_name TEXT
        )
    """)

    # Parking slots table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS parking_slots (
            slot_id INTEGER PRIMARY KEY AUTOINCREMENT,
            slot_number TEXT NOT NULL UNIQUE,
            slot_type TEXT NOT NULL DEFAULT 'Normal',
            status TEXT NOT NULL DEFAULT 'Available'
        )
    """)

    # Parking records table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS parking_records (
            parking_id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_id INTEGER NOT NULL,
            slot_id INTEGER NOT NULL,
            entry_time DATETIME NOT NULL,
            exit_time DATETIME,
            duration_hours INTEGER,
            amount_due REAL DEFAULT 0,
            status TEXT NOT NULL DEFAULT 'Active',

            FOREIGN KEY (vehicle_id) REFERENCES vehicles(vehicle_id),
            FOREIGN KEY (slot_id) REFERENCES parking_slots(slot_id)
        )
    """)

    # Payments table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            parking_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            payment_method TEXT NOT NULL,
            payment_time DATETIME NOT NULL,
            payment_status TEXT NOT NULL
        )
    """)

    # Rates table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rates (
            rate_id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_type TEXT NOT NULL UNIQUE,
            first_hour_rate REAL NOT NULL,
            additional_hour_rate REAL NOT NULL
        )
    """)

    # Add parking slots
    slots = [
        ("A01", "Normal"),
        ("A02", "Normal"),
        ("A03", "Normal"),
        ("A04", "Normal"),
        ("A05", "Normal"),
        ("A06", "Normal"),
        ("A07", "Normal"),
        ("A08", "Normal")
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO parking_slots
        (slot_number, slot_type, status)
        VALUES (?, ?, 'Available')
    """, slots)

    # Add parking rates
    rates = [
        ("Car", 50, 30),
        ("SUV", 70, 40),
        ("Motorcycle", 30, 20)
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO rates
        (vehicle_type, first_hour_rate, additional_hour_rate)
        VALUES (?, ?, ?)
    """, rates)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    initialize_database()
    print("Database initialized successfully.")
