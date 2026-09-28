# Modern Parking Management System

## 1. Project Overview

The Modern Parking Management System is a software solution designed to automate the operations of a parking facility.

The system allows drivers to view available parking spaces before entering, records vehicles when they arrive, automatically assigns available parking slots, calculates parking duration and parking fees when vehicles exit, records payments, and opens the exit barrier after successful payment.

The system is designed as a prototype for a parking facility operating in Kenya.

---

## 2. Project Objectives

The main objectives of the system are to:

- Display available and occupied parking slots.
- Register vehicles entering the parking facility.
- Automatically allocate available parking slots.
- Record vehicle entry and exit times.
- Calculate parking duration automatically.
- Calculate parking fees based on vehicle type and duration.
- Record payment transactions.
- Release occupied parking slots after vehicles exit.
- Control the exit barrier based on payment status.
- Store parking information in a database.

---

## 3. System Modules

The system consists of the following modules:

### 1. Parking Slot Display Module

Displays all parking slots and their current status.

### 2. Vehicle Registration Module

Records vehicle registration numbers, vehicle types, and owner information.

### 3. Parking Slot Allocation Module

Automatically identifies and assigns an available parking slot.

### 4. Vehicle Exit Module

Identifies vehicles leaving the facility and calculates their parking duration.

### 5. Fee Calculation Module

Calculates the amount payable based on the vehicle type and parking duration.

### 6. Payment Module

Records payments and verifies whether the required amount has been paid.

### 7. Barrier Control Module

Simulates opening the exit barrier after successful payment.

### 8. Database Management Module

Stores and manages vehicle, parking, payment, slot, and rate information.

---

## 4. Technologies Used

- Python
- SQLite
- SQL
- GitHub
- Markdown

---

## 5. Database Design

The system uses a relational SQLite database consisting of five main tables:

- `vehicles`
- `parking_slots`
- `parking_records`
- `payments`
- `rates`

The database stores vehicle information, parking availability, parking sessions, payment transactions, and parking rates.

The SQL database structure is available in:

`database/parking_system.sql`

---

## 6. Parking Rates

The prototype uses the following parking rates:

| Vehicle Type | First Hour | Additional Hour |
|---|---:|---:|
| Car | KSh 50 | KSh 30 |
| SUV | KSh 70 | KSh 40 |
| Motorcycle | KSh 30 | KSh 20 |

These rates are sample values for the prototype and can be changed in the database.

---

## 7. System Process

The general system process is:

```text
Driver Arrives
      |
      v
View Available Parking Slots
      |
      v
Register Vehicle
      |
      v
Allocate Parking Slot
      |
      v
Vehicle Parks
      |
      v
Vehicle Requests Exit
      |
      v
Calculate Parking Duration
      |
      v
Calculate Parking Fee
      |
      v
Process Payment
      |
      v
Payment Successful?
     / \
   YES  NO
    |    |
    v    v
Open   Keep
Barrier Closed
    |
    v
Release Parking Slot
    |
    v
Update Database
