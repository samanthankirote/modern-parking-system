# Dynamic Database Design

## 1. Introduction

The Modern Parking Management System requires a dynamic database to store and manage information about vehicles, parking spaces, parking activities, payments, and parking rates.

The system uses SQLite as the database management system. SQLite is suitable for this project because it is lightweight, easy to deploy, and supports relational database operations.

---

## 2. Database Tables

The database consists of the following main tables:

1. Vehicles
2. Parking Slots
3. Parking Records
4. Payments
5. Rates

---

## 3. Vehicles Table

The `vehicles` table stores information about vehicles using the parking facility.

| Field | Data Type | Description |
|---|---|---|
| vehicle_id | INTEGER | Unique identifier for each vehicle |
| registration_no | TEXT | Vehicle registration number |
| vehicle_type | TEXT | Type of vehicle |
| owner_name | TEXT | Name of the vehicle owner |

### Primary Key

`vehicle_id` is the primary key.

### Constraint

`registration_no` is unique so that the same vehicle registration number cannot be registered twice.

---

## 4. Parking Slots Table

The `parking_slots` table stores information about the parking spaces.

| Field | Data Type | Description |
|---|---|---|
| slot_id | INTEGER | Unique identifier for the parking slot |
| slot_number | TEXT | Parking slot number |
| slot_type | TEXT | Type of parking slot |
| status | TEXT | Current availability of the slot |

### Possible Status Values

```text
Available
Occupied
