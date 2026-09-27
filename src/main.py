# Modern Parking Management System
# Parking Slot Module

parking_slots = {
    "A01": "Available",
    "A02": "Available",
    "A03": "Available",
    "A04": "Available",
    "A05": "Available",
    "A06": "Available",
    "A07": "Available",
    "A08": "Available",
}


def display_parking_slots():
    print("\n========================================")
    print("       PARKING SLOT AVAILABILITY")
    print("========================================")

    available = 0
    occupied = 0

    for slot, status in parking_slots.items():
        if status == "Available":
            print(f"{slot} - 🟩 Available")
            available += 1
        else:
            print(f"{slot} - 🟥 Occupied")
            occupied += 1

    print("----------------------------------------")
    print(f"Available slots: {available}")
    print(f"Occupied slots:  {occupied}")
    print("========================================")


def allocate_slot():
    for slot, status in parking_slots.items():
        if status == "Available":
            parking_slots[slot] = "Occupied"
            return slot

    return None


def release_slot(slot):
    if slot in parking_slots:
        parking_slots[slot] = "Available"


# Test the parking slot module
display_parking_slots()

allocated_slot = allocate_slot()

if allocated_slot:
    print(f"\nAllocated parking slot: {allocated_slot}")
else:
    print("\nParking is full.")

display_parking_slots()

from datetime import datetime

vehicles = {}


def register_vehicle():
    print("\n========================================")
    print("          VEHICLE ENTRY")
    print("========================================")

    registration = input("Enter vehicle registration number: ").strip().upper()
    vehicle_type = input("Enter vehicle type: ").strip().title()

    # Check whether the vehicle is already inside
    if registration in vehicles:
        print("\nVehicle is already registered in the parking lot.")
        return

    # Find an available parking slot
    slot = allocate_slot()

    if slot is None:
        print("\nSorry, the parking lot is full.")
        return

    # Record the entry time
    entry_time = datetime.now()

    # Store vehicle information
    vehicles[registration] = {
        "vehicle_type": vehicle_type,
        "slot": slot,
        "entry_time": entry_time
    }

    print("\nVehicle successfully registered!")
    print(f"Registration: {registration}")
    print(f"Vehicle type: {vehicle_type}")
    print(f"Allocated slot: {slot}")
    print(f"Entry time: {entry_time.strftime('%Y-%m-%d %H:%M:%S')}")
    register_vehicle()
display_parking_slots()
