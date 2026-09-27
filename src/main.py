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
