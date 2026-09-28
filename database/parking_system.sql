-- Modern Parking Management System
-- SQLite Database Design

CREATE TABLE IF NOT EXISTS vehicles (
    vehicle_id INTEGER PRIMARY KEY AUTOINCREMENT,
    registration_no TEXT NOT NULL UNIQUE,
    vehicle_type TEXT NOT NULL,
    owner_name TEXT
);

CREATE TABLE IF NOT EXISTS parking_slots (
    slot_id INTEGER PRIMARY KEY AUTOINCREMENT,
    slot_number TEXT NOT NULL UNIQUE,
    slot_type TEXT NOT NULL DEFAULT 'Normal',
    status TEXT NOT NULL DEFAULT 'Available'
);

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
);

CREATE TABLE IF NOT EXISTS payments (
    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    parking_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    payment_method TEXT NOT NULL,
    payment_time DATETIME NOT NULL,
    payment_status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS rates (
    rate_id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_type TEXT NOT NULL UNIQUE,
    first_hour_rate REAL NOT NULL,
    additional_hour_rate REAL NOT NULL
);

-- Initial parking slots

INSERT OR IGNORE INTO parking_slots
(slot_number, slot_type, status)
VALUES
('A01', 'Normal', 'Available'),
('A02', 'Normal', 'Available'),
('A03', 'Normal', 'Available'),
('A04', 'Normal', 'Available'),
('A05', 'Normal', 'Available'),
('A06', 'Normal', 'Available'),
('A07', 'Normal', 'Available'),
('A08', 'Normal', 'Available');

-- Parking rates

INSERT OR IGNORE INTO rates
(vehicle_type, first_hour_rate, additional_hour_rate)
VALUES
('Car', 50, 30),
('SUV', 70, 40),
('Motorcycle', 30, 20);
