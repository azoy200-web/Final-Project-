"""
Booking.py

This module contains the Booking class.

We separated Booking because it is the object that connects the user, facility, date,
time slot, usage type, cost, and status together. This helped us fix the first trial
problem where the booking history was missing important details such as the location,
and it also made the receipt information easier to generate correctly.
"""

from enums import BookingStatus

"""
This file stores the Booking class.

Why this file is separate:
Booking is the relationship object that connects a user, a facility, a date, and a time slot.
It is separated because it is central to the system and is used by payments, receipts,
facility availability, and admin reports.
"""

class Booking:
    """
    Booking represents a confirmed reservation.

    Purpose:
    - Connects User, Facility, slot, date, usage type, cost, and booking status.
    - Generates booking summaries for receipts and GUI display.

    Logical reason:
    Booking is the relationship object proving that a user reserved a facility at a specific time.
    """
    def __init__(self, booking_id, user, facility, slot, booking_date, usage_type, total_cost):
        """
        Constructor purpose:
        - Creates a new object and prepares its starting data.

        Logical reason:
        Each object must begin with valid attributes before the system can use it.
        """
        self.__booking_id = booking_id
        self.__user = user
        self.__facility = facility
        self.__slot = slot
        self.__booking_date = booking_date
        self.__usage_type = usage_type
        self.__total_cost = total_cost
        self.__status = BookingStatus.CONFIRMED

    def get_booking_id(self):
        """
        Purpose:
        - Returns booking ID.

        Logical reason:
        Bookings need IDs for modification, cancellation, and admin reports.
        """
        return self.__booking_id

    def get_user(self):
        """
        Purpose:
        - Returns the user linked to the booking.

        Logical reason:
        The system must know who owns each booking.
        """
        return self.__user

    def get_facility(self):
        """
        Purpose:
        - Finds a facility by ID.

        Logical reason:
        Booking uses facility ID selected from GUI.
        """
        return self.__facility

    def get_slot(self):
        """
        Purpose:
        - Returns the booked slot.

        Logical reason:
        Reports, conflicts, and modifications need the booking time.
        """
        return self.__slot

    def set_slot(self, slot):
        """
        Purpose:
        - Updates the booking slot.

        Logical reason:
        Users can modify their booking time.
        """
        self.__slot = slot

    def get_booking_date(self):
        """
        Purpose:
        - Returns the booking date.

        Logical reason:
        Reports and conflict checks need the date.
        """
        return self.__booking_date

    def set_booking_date(self, booking_date):
        """
        Purpose:
        - Updates the booking date.

        Logical reason:
        Users can modify their booking date.
        """
        self.__booking_date = booking_date

    def get_usage_type(self):
        """
        Purpose:
        - Returns internal or external usage.

        Logical reason:
        EventHall cost depends on usage type.
        """
        return self.__usage_type

    def get_total_cost(self):
        """
        Purpose:
        - Returns booking cost.

        Logical reason:
        Payments and receipts need this amount.
        """
        return self.__total_cost

    def get_status(self):
        """
        Purpose:
        - Returns current object status.

        Logical reason:
        The system needs status for users, bookings, or payments.
        """
        return self.__status

    def set_status(self, status):
        """
        Purpose:
        - Updates status safely.

        Logical reason:
        Object state changes during booking, payment, cancellation, and freezing.
        """
        self.__status = status

    def cancel_booking(self):
        """
        Purpose:
        - Marks a booking as cancelled.

        Logical reason:
        Cancelled bookings should no longer count as active.
        """
        self.__status = BookingStatus.CANCELLED

    def mark_no_show(self):
        """
        Purpose:
        - Marks booking as no-show.

        Logical reason:
        No-shows reduce penalty credits and may freeze the user.
        """
        self.__status = BookingStatus.NO_SHOW

    def generate_booking_summary(self):
        """
        Purpose:
        - Creates readable booking details.

        Logical reason:
        Receipts, tests, and GUI screens need a clear booking summary.
        """
        return (
            f"Booking ID: {self.__booking_id}\n"
            f"User: {self.__user.get_name()}\n"
            f"Facility: {self.__facility.get_facility_name()}\n"
            f"Facility Type: {self.__facility.get_facility_type()}\n"
            f"Location: {self.__facility.get_location()}\n"
            f"Date: {self.__booking_date}\n"
            f"Time Slot: {self.__slot}\n"
            f"Usage Type: {self.__usage_type}\n"
            f"Cost: {self.__total_cost} AED\n"
            f"Status: {self.__status.value}\n"
            f"{self.__facility.get_rules()}"
        )
