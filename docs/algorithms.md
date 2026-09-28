# Algorithms for the Modern Parking Management System

## 1. Introduction

The proposed Modern Parking Management System automates the major operations of a parking facility. The system allows drivers to view available parking spaces, register vehicles on arrival, automatically allocate parking spaces, calculate parking duration and fees, process payments, and control the exit barrier.

The system is divided into the following modules:

1. Parking Slot Display Module
2. Vehicle Registration Module
3. Parking Slot Allocation Module
4. Vehicle Exit Module
5. Fee Calculation Module
6. Payment Module
7. Barrier Control Module
8. Database Management Module

---

# 2. Parking Slot Display Algorithm

## Purpose

This algorithm displays the current status of all parking spaces before a vehicle enters the parking facility.

## Algorithm

```text
START

Retrieve all parking slots from the database.

Set available_slots = 0.
Set occupied_slots = 0.

FOR each parking slot:

    IF slot status is "Available":

        Display the slot as AVAILABLE.
        Increase available_slots by 1.

    ELSE:

        Display the slot as OCCUPIED.
        Increase occupied_slots by 1.

    END IF

END FOR

Display total available slots.
Display total occupied slots.

END
START

Request vehicle registration number.

Request vehicle type.

Request vehicle owner's name.

Search the database for the vehicle registration number.

IF the vehicle already has an active parking record:

    Display "Vehicle is already inside."

ELSE:

    Search for an available parking slot.

    IF no slot is available:

        Display "Parking is full."

    ELSE:

        Record the vehicle information.

        Record the current date and time.

        Create a parking record.

        Send the vehicle to the parking slot allocation process.

    END IF

END IF

END
START

Search the parking_slots table.

Find the first slot whose status is "Available".

IF an available slot is found:

    Assign the slot to the vehicle.

    Change the slot status to "Occupied".

    Record the slot allocation in the parking record.

    Display the allocated slot number.

ELSE:

    Display "No parking slot available."

END IF

END
START

Request vehicle registration number.

Search the database for an active parking record.

IF the vehicle is not found:

    Display "Vehicle not found."

ELSE:

    Retrieve the vehicle entry time.

    Record the current time as the exit time.

    Calculate:

        Duration = Exit Time - Entry Time

    Round the duration up to the next whole hour.

    Send the duration to the fee calculation module.

    Display vehicle information.

    Display parking duration.

    Display amount due.

END IF

END
START

Receive vehicle type.

Receive parking duration in hours.

Retrieve the applicable rate from the rates table.

IF parking duration is less than or equal to 1 hour:

    Fee = First Hour Rate.

ELSE:

    Additional Hours = Parking Duration - 1.

    Fee =
        First Hour Rate +
        (Additional Hours × Additional Hour Rate).

END IF

Return the calculated fee.

END
START

Display amount due.

Request payment method.

Request amount paid.

IF amount paid is less than amount due:

    Calculate remaining balance.

    Display "Payment unsuccessful."

    Keep the exit barrier CLOSED.

ELSE:

    Calculate change if necessary.

    Record payment in the database.

    Mark payment as PAID.

    Mark parking record as COMPLETED.

    Release the parking slot.

    Send request to the barrier control module.

END IF

END
START

Receive payment status.

IF payment status is "Paid":

    Open the exit barrier.

    Allow vehicle to leave.

    Change the parking slot status to "Available".

ELSE:

    Keep the barrier CLOSED.

    Do not allow vehicle to exit.

END IF

END
START

Connect to SQLite database.

IF database tables do not exist:

    Create the required tables.

    Create initial parking slots.

    Create parking rates.

END IF

When a vehicle enters:

    Store vehicle information.

    Store entry time.

    Store allocated parking slot.

When a vehicle exits:

    Store exit time.

    Store parking duration.

    Store amount due.

When payment is successful:

    Store payment information.

    Update parking record.

    Change parking slot status to AVAILABLE.

Close database connection.

END
START

Initialize the database.

Display the main menu.

WHILE the system is running:

    Display parking slot availability.

    Display system options.

    IF user selects Vehicle Entry:

        Register vehicle.

        Find available parking slot.

        Assign parking slot.

        Record entry time.

        Update slot status to OCCUPIED.

    ELSE IF user selects Vehicle Exit:

        Find vehicle record.

        Record exit time.

        Calculate parking duration.

        Calculate parking fee.

        Request payment.

        IF payment is successful:

            Record payment.

            Update parking record.

            Release parking slot.

            Open exit barrier.

        ELSE:

            Keep barrier closed.

        END IF

    ELSE IF user selects View Parking Slots:

        Display available and occupied slots.

    ELSE IF user selects Exit:

        Stop the system.

    ELSE:

        Display "Invalid option."

    END IF

END WHILE

END
