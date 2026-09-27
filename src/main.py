from datetime import datetime
import sqlite3
from database import get_connection, initialize_database


def display_parking_slots():
    """Display all parking slots and their current status."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT slot_number, status
        FROM parking_slots
        ORDER BY slot_number
    """)

    slots = cursor.fetchall()
    connection.close()

    print("\n========================================")
    print("       PARKING SLOT AVAILABILITY")
    print("========================================")

    available = 0
    occupied = 0

    for slot_number, status in slots:
        if status == "Available":
            print(f"{slot_number} - 🟩 Available")
            available += 1
        else:
            print(f"{slot_number} - 🟥 Occupied")
            occupied += 1

    print("----------------------------------------")
    print(f"Available slots: {available}")
    print(f"Occupied slots:  {occupied}")
    print("========================================")


def find_available_slot():
    """Find the first available parking slot."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT slot_id, slot_number
        FROM parking_slots
        WHERE status = 'Available'
        ORDER BY slot_number
        LIMIT 1
    """)

    slot = cursor.fetchone()
    connection.close()

    return slot


def register_vehicle():
    """Register a vehicle and assign an available parking slot."""

    print("\n========================================")
    print("          VEHICLE ENTRY")
    print("========================================")

    registration = input(
        "Enter vehicle registration number: "
    ).strip().upper()

    vehicle_type = input(
        "Enter vehicle type (Car/SUV/Motorcycle): "
    ).strip().title()

    owner_name = input(
        "Enter owner name: "
    ).strip()

    connection = get_connection()
    cursor = connection.cursor()

    # Check whether vehicle is already inside
    cursor.execute("""
        SELECT vehicle_id
        FROM vehicles
        WHERE registration_no = ?
    """, (registration,))

    existing_vehicle = cursor.fetchone()

    if existing_vehicle:
        cursor.execute("""
            SELECT parking_id
            FROM parking_records
            WHERE vehicle_id = ?
            AND status = 'Active'
        """, (existing_vehicle[0],))

        active_record = cursor.fetchone()

        if active_record:
            print("\nVehicle is already inside the parking lot.")
            connection.close()
            return

    # Find an available slot
    cursor.execute("""
        SELECT slot_id, slot_number
        FROM parking_slots
        WHERE status = 'Available'
        ORDER BY slot_number
        LIMIT 1
    """)

    slot = cursor.fetchone()

    if slot is None:
        print("\nSorry, the parking lot is full.")
        connection.close()
        return

    slot_id, slot_number = slot

    try:
        # Add vehicle if it doesn't already exist
        cursor.execute("""
            INSERT OR IGNORE INTO vehicles
            (registration_no, vehicle_type, owner_name)
            VALUES (?, ?, ?)
        """, (registration, vehicle_type, owner_name))

        cursor.execute("""
            SELECT vehicle_id
            FROM vehicles
            WHERE registration_no = ?
        """, (registration,))

        vehicle_id = cursor.fetchone()[0]

        entry_time = datetime.now()

        # Create parking record
        cursor.execute("""
            INSERT INTO parking_records
            (vehicle_id, slot_id, entry_time, status)
            VALUES (?, ?, ?, 'Active')
        """, (vehicle_id, slot_id, entry_time))

        # Mark slot as occupied
        cursor.execute("""
            UPDATE parking_slots
            SET status = 'Occupied'
            WHERE slot_id = ?
        """, (slot_id,))

        connection.commit()

        print("\nVehicle successfully registered!")
        print(f"Registration: {registration}")
        print(f"Vehicle type: {vehicle_type}")
        print(f"Parking slot: {slot_number}")
        print(
            f"Entry time: {entry_time.strftime('%Y-%m-%d %H:%M:%S')}"
        )

    except sqlite3.Error as error:
        connection.rollback()
        print(f"\nDatabase error: {error}")

    finally:
        connection.close()


def calculate_fee(vehicle_type, duration_hours):
    """Calculate the parking fee using the stored vehicle rate."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT first_hour_rate, additional_hour_rate
        FROM rates
        WHERE vehicle_type = ?
    """, (vehicle_type,))

    rate = cursor.fetchone()
    connection.close()

    if rate is None:
        # Default rate if vehicle type is not found
        first_hour = 50
        additional_hour = 30
    else:
        first_hour, additional_hour = rate

    if duration_hours <= 1:
        return first_hour

    return first_hour + (
        (duration_hours - 1) * additional_hour
    )


def vehicle_exit():
    """Process vehicle exit, calculate fee and record the exit."""

    print("\n========================================")
    print("           VEHICLE EXIT")
    print("========================================")

    registration = input(
        "Enter vehicle registration number: "
    ).strip().upper()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            pr.parking_id,
            pr.entry_time,
            pr.slot_id,
            ps.slot_number,
            v.vehicle_id,
            v.vehicle_type
        FROM parking_records pr
        JOIN vehicles v
            ON pr.vehicle_id = v.vehicle_id
        JOIN parking_slots ps
            ON pr.slot_id = ps.slot_id
        WHERE v.registration_no = ?
        AND pr.status = 'Active'
    """, (registration,))

    record = cursor.fetchone()

    if record is None:
        print("\nVehicle not found in the parking lot.")
        connection.close()
        return

    (
        parking_id,
        entry_time_string,
        slot_id,
        slot_number,
        vehicle_id,
        vehicle_type
    ) = record

    entry_time = datetime.fromisoformat(entry_time_string)
    exit_time = datetime.now()

    duration = exit_time - entry_time
    total_minutes = duration.total_seconds() / 60

    # Charge at least one hour
    duration_hours = max(
        1,
        int((total_minutes + 59) // 60)
    )

    amount = calculate_fee(
        vehicle_type,
        duration_hours
    )

    print("\n----------------------------------------")
    print(f"Vehicle:       {registration}")
    print(f"Vehicle type:  {vehicle_type}")
    print(f"Parking slot:  {slot_number}")
    print(
        f"Entry time:    "
        f"{entry_time.strftime('%Y-%m-%d %H:%M:%S')}"
    )
    print(
        f"Exit time:     "
        f"{exit_time.strftime('%Y-%m-%d %H:%M:%S')}"
    )
    print(f"Time parked:   {duration_hours} hour(s)")
    print(f"Amount due:    KSh {amount:.2f}")
    print("----------------------------------------")

    connection.close()

    process_payment(
        parking_id,
        slot_id,
        amount,
        registration,
        exit_time,
        duration_hours
    )


def process_payment(
    parking_id,
    slot_id,
    amount,
    registration,
    exit_time,
    duration_hours
):
    """Process payment and open the barrier after successful payment."""

    print("\n========================================")
    print("             PAYMENT")
    print("========================================")
    print(f"Amount to pay: KSh {amount:.2f}")

    payment_method = input(
        "Payment method (Cash/M-Pesa/Card): "
    ).strip().title()

    payment_input = input(
        "Enter amount paid: KSh "
    ).strip()

    try:
        payment = float(payment_input)
    except ValueError:
        print("\nInvalid payment amount.")
        close_barrier()
        return

    if payment < amount:
        balance = amount - payment

        print("\nPayment unsuccessful.")
        print(f"Remaining balance: KSh {balance:.2f}")

        close_barrier()
        return

    change = payment - amount

    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Record payment
        cursor.execute("""
            INSERT INTO payments
            (parking_id, amount, payment_method,
             payment_time, payment_status)
            VALUES (?, ?, ?, ?, 'Paid')
        """, (
            parking_id,
            amount,
            payment_method,
            exit_time
        ))

        # Complete parking record
        cursor.execute("""
            UPDATE parking_records
            SET
                exit_time = ?,
                duration_hours = ?,
                amount_due = ?,
                status = 'Completed'
            WHERE parking_id = ?
        """, (
            exit_time,
            duration_hours,
            amount,
            parking_id
        ))

        # Free parking slot
        cursor.execute("""
            UPDATE parking_slots
            SET status = 'Available'
            WHERE slot_id = ?
        """, (slot_id,))

        connection.commit()

        print("\nPayment successful!")
        print(f"Payment method: {payment_method}")
        print(f"Amount paid: KSh {payment:.2f}")

        if change > 0:
            print(f"Change: KSh {change:.2f}")

        open_barrier()

    except sqlite3.Error as error:
        connection.rollback()
        print(f"\nDatabase error: {error}")
        close_barrier()

    finally:
        connection.close()


def open_barrier():
    """Open the exit barrier."""

    print("\n========================================")
    print("           EXIT BARRIER")
    print("========================================")
    print("Payment confirmed.")
    print("Barrier OPEN.")
    print("Vehicle may exit.")
    print("========================================")


def close_barrier():
    """Keep the exit barrier closed."""

    print("\nBarrier CLOSED.")
    print("Payment is required before exit.")


def main():
    """Main menu of the parking management system."""

    initialize_database()

    while True:
        print("\n")
        print("╔══════════════════════════════════════╗")
        print("║   MODERN PARKING MANAGEMENT SYSTEM  ║")
        print("╠══════════════════════════════════════╣")
        print("║ 1. View Parking Slots               ║")
        print("║ 2. Vehicle Entry                    ║")
        print("║ 3. Vehicle Exit                     ║")
        print("║ 4. Exit System                      ║")
        print("╚══════════════════════════════════════╝")

        choice = input("Select an option: ").strip()

        if choice == "1":
            display_parking_slots()

        elif choice == "2":
            register_vehicle()

        elif choice == "3":
            vehicle_exit()

        elif choice == "4":
            print("\nThank you for using the system.")
            break

        else:
            print("\nInvalid option. Please try again.")


if __name__ == "__main__":
    main()
