"""
facilities.py

This module contains the Facility inheritance group: Facility, StudyRoom, SportsCourt,
EventHall, and TimeSlot.

We separated these classes together because all facility types share the same booking
idea, but each one still has its own rule. This helped us fix the maintenance issue,
because closed slots are now stored by date and time instead of closing the whole
facility for every date.
"""

from enums import UsageType

"""
This file groups the Facility inheritance hierarchy.

Why this grouping is logical:
Facility is the parent class, while StudyRoom, SportsCourt, and EventHall are facility types.
They are kept together because they share common slot and availability behavior, while each
facility type has different rules and pricing. TimeSlot is also here because it supports
facility booking time management.
"""

class Facility:
    """
    Facility is the parent class for StudyRoom, SportsCourt, and EventHall.

    Purpose:
    - Stores facility details like ID, name, type, location, capacity, price, rules, time slots, booked slots, and closed slots.
    - Controls booking availability and slot management.

    Logical reason:
    All facility types share common data, so a parent class avoids repeated code.
    """
    def __init__(self, facility_id, facility_name, facility_type, location, capacity, price_per_hour, rules):
        """
        Constructor purpose:
        - Creates a new object and prepares its starting data.

        Logical reason:
        Each object must begin with valid attributes before the system can use it.
        """
        self.__facility_id = facility_id
        self.__facility_name = facility_name
        self.__facility_type = facility_type
        self.__location = location
        self.__capacity = capacity
        self.__is_available = True
        self.__price_per_hour = price_per_hour
        self.__rules = rules
        self.__time_slots = [
            "09:00-10:00",
            "10:00-11:00",
            "11:00-12:00",
            "12:00-13:00",
            "14:00-15:00",
            "15:00-16:00"
        ]
        self.__booked_slots_by_date = {}
        self.__closed_slots_by_date = {}

    def get_facility_id(self):
        """
        Purpose:
        - Returns facility ID.

        Logical reason:
        The catalog uses this ID to find and store facilities.
        """
        return self.__facility_id

    def set_facility_id(self, facility_id):
        """
        Purpose:
        - Updates facility ID.

        Logical reason:
        Facility identity may need correction in admin management.
        """
        self.__facility_id = facility_id

    def get_facility_name(self):
        """
        Purpose:
        - Returns facility name.

        Logical reason:
        Users need readable facility names in the GUI.
        """
        return self.__facility_name

    def set_facility_name(self, facility_name):
        """
        Purpose:
        - Updates facility name.

        Logical reason:
        Admin may need to rename facilities.
        """
        self.__facility_name = facility_name

    def get_facility_type(self):
        """
        Purpose:
        - Returns facility type.

        Logical reason:
        Access rules depend on the facility type.
        """
        return self.__facility_type

    def set_facility_type(self, facility_type):
        """
        Purpose:
        - Updates facility type.

        Logical reason:
        Admin may need to correct facility classification.
        """
        self.__facility_type = facility_type

    def get_location(self):
        """
        Purpose:
        - Returns facility location.

        Logical reason:
        Users need to know where to go.
        """
        return self.__location

    def set_location(self, location):
        """
        Purpose:
        - Updates facility location.

        Logical reason:
        Facility details must stay accurate.
        """
        self.__location = location

    def get_capacity(self):
        """
        Purpose:
        - Returns facility capacity.

        Logical reason:
        Users and admins need to know maximum occupancy.
        """
        return self.__capacity

    def set_capacity(self, capacity):
        """
        Purpose:
        - Updates capacity after validation.

        Logical reason:
        Capacity cannot be zero or negative.
        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive.")
        self.__capacity = capacity

    def get_is_available(self):
        """
        Purpose:
        - Returns whether the whole facility is available.

        Logical reason:
        Unavailable facilities should not appear as bookable.
        """
        return self.__is_available

    def set_is_available(self, is_available):
        """
        Purpose:
        - Opens or closes the whole facility.

        Logical reason:
        Admin needs to disable facilities during maintenance.
        """
        self.__is_available = is_available

    def get_price_per_hour(self):
        """
        Purpose:
        - Returns facility price.

        Logical reason:
        The payment screen must show and calculate cost.
        """
        return self.__price_per_hour

    def set_price_per_hour(self, price_per_hour):
        """
        Purpose:
        - Updates price after validation.

        Logical reason:
        Prices cannot be negative.
        """
        if price_per_hour < 0:
            raise ValueError("Price cannot be negative.")
        self.__price_per_hour = price_per_hour

    def get_rules(self):
        """
        Purpose:
        - Returns facility rules.

        Logical reason:
        Users should see rules before confirming bookings.
        """
        return self.__rules

    def set_rules(self, rules):
        """
        Purpose:
        - Updates facility rules.

        Logical reason:
        Admin can change policies or instructions.
        """
        self.__rules = rules

    def get_time_slots(self):
        """
        Purpose:
        - Returns all possible facility time slots.

        Logical reason:
        The GUI needs this list for booking choices.
        """
        return self.__time_slots

    def set_time_slots(self, time_slots):
        """
        Purpose:
        - Updates available time slot list.

        Logical reason:
        Admin may adjust operating hours.
        """
        self.__time_slots = time_slots

    def get_booked_slots_by_date(self):
        """
        Purpose:
        - Returns confirmed booked slots by date.

        Logical reason:
        The system must remember which slots are already taken.
        """
        return self.__booked_slots_by_date

    def set_booked_slots_by_date(self, booked_slots_by_date):
        """
        Purpose:
        - Restores booked slot data.

        Logical reason:
        This helps repair or load pickle data.
        """
        self.__booked_slots_by_date = booked_slots_by_date

    def get_closed_slots_by_date(self):
        """
        Purpose:
        - Returns admin-closed slots by date.

        Logical reason:
        Maintenance closures must be stored separately from booked slots.
        """
        return self.__closed_slots_by_date

    def set_closed_slots_by_date(self, closed_slots_by_date):
        """
        Purpose:
        - Restores closed slot data.

        Logical reason:
        This helps old saved data work with updated code.
        """
        self.__closed_slots_by_date = closed_slots_by_date

    def get_closed_slots(self, booking_date):
        """
        Purpose:
        - Returns closed slots for one date.

        Logical reason:
        The booking screen must block closed slots.
        """
        if booking_date not in self.__closed_slots_by_date:
            self.__closed_slots_by_date[booking_date] = []
        return self.__closed_slots_by_date[booking_date]

    def close_slot(self, booking_date, slot):
        """
        Purpose:
        - Closes one specific slot for a facility.

        Logical reason:
        Admin can block a time for maintenance without closing the whole facility.
        """
        if slot not in self.__time_slots:
            raise ValueError("Invalid time slot.")
        if booking_date not in self.__closed_slots_by_date:
            self.__closed_slots_by_date[booking_date] = []
        if slot not in self.__closed_slots_by_date[booking_date]:
            self.__closed_slots_by_date[booking_date].append(slot)

    def open_slot(self, booking_date, slot):
        """
        Purpose:
        - Reopens a previously closed slot.

        Logical reason:
        Admin needs to undo maintenance closures.
        """
        if booking_date in self.__closed_slots_by_date:
            if slot in self.__closed_slots_by_date[booking_date]:
                self.__closed_slots_by_date[booking_date].remove(slot)

    def get_available_slots(self, booking_date):
        """
        Purpose:
        - Returns slots that are not booked and not closed.

        Logical reason:
        Users should only be offered valid booking options.
        """
        if booking_date not in self.__booked_slots_by_date:
            self.__booked_slots_by_date[booking_date] = {}
        if booking_date not in self.__closed_slots_by_date:
            self.__closed_slots_by_date[booking_date] = []

        booked = self.__booked_slots_by_date[booking_date]
        closed = self.__closed_slots_by_date[booking_date]

        return [
            slot for slot in self.__time_slots
            if slot not in booked and slot not in closed
        ]

    def book_slot(self, booking_date, slot, booking_id):
        """
        Purpose:
        - Marks a slot as booked for a date.

        Logical reason:
        This prevents another user from booking the same facility slot.
        """
        if slot not in self.__time_slots:
            raise ValueError("Invalid time slot.")
        if booking_date not in self.__booked_slots_by_date:
            self.__booked_slots_by_date[booking_date] = {}
        if slot in self.__booked_slots_by_date[booking_date]:
            raise ValueError("This slot is already booked.")
        if slot in self.get_closed_slots(booking_date):
            raise ValueError("This slot is closed by admin.")
        self.__booked_slots_by_date[booking_date][slot] = booking_id

    def release_slot(self, booking_date, slot):
        """
        Purpose:
        - Frees a slot after cancellation, modification, or no-show.

        Logical reason:
        Released slots should become available for other users.
        """
        if booking_date in self.__booked_slots_by_date:
            if slot in self.__booked_slots_by_date[booking_date]:
                del self.__booked_slots_by_date[booking_date][slot]

    def calculate_cost(self, usage_type):
        """
        Purpose:
        - Calculates facility booking cost.

        Logical reason:
        Payment depends on the selected facility and usage type.
        """
        return self.__price_per_hour

    def display_details(self):
        """
        Purpose:
        - Returns a simple facility summary.

        Logical reason:
        The GUI and admin dashboard need readable facility info.
        """
        return f"{self.__facility_name} | {self.__location} | Capacity: {self.__capacity}"
class StudyRoom(Facility):
    """
    StudyRoom represents study room facilities.

    Purpose:
    - Creates student-only rooms with no booking fee.

    Logical reason:
    Study rooms have their own access rules, so they are represented as a child class of Facility.
    """
    def __init__(self, facility_id, room_code, location, capacity):
        """
        Constructor purpose:
        - Creates a new object and prepares its starting data.

        Logical reason:
        Each object must begin with valid attributes before the system can use it.
        """
        super().__init__(
            facility_id,
            f"Study Room {room_code}",
            "STUDY_ROOM",
            location,
            capacity,
            0,
            "Rules: Students only. Keep the room clean. Arrive on time."
        )
        self.__room_code = room_code

    def get_room_code(self):
        """
        Purpose:
        - Returns study room code.

        Logical reason:
        Room codes help identify specific study rooms.
        """
        return self.__room_code

    def set_room_code(self, room_code):
        """
        Purpose:
        - Updates study room code.

        Logical reason:
        Admin may need to correct room labels.
        """
        self.__room_code = room_code
class SportsCourt(Facility):
    """
    SportsCourt represents sports facilities.

    Purpose:
    - Stores sport type and hourly price.
    - Supports premium student and premium staff bookings.

    Logical reason:
    Sports courts have different access and payment rules from study rooms and event halls.
    """
    def __init__(self, facility_id, sport_type, location, capacity, price_per_hour):
        """
        Constructor purpose:
        - Creates a new object and prepares its starting data.

        Logical reason:
        Each object must begin with valid attributes before the system can use it.
        """
        super().__init__(
            facility_id,
            f"{sport_type} Court",
            "SPORTS_COURT",
            location,
            capacity,
            price_per_hour,
            "Rules: Sports shoes required. Respect the booked time."
        )
        self.__sport_type = sport_type

    def get_sport_type(self):
        """
        Purpose:
        - Returns sport type.

        Logical reason:
        Users need to know what court they are booking.
        """
        return self.__sport_type

    def set_sport_type(self, sport_type):
        """
        Purpose:
        - Updates sport type.

        Logical reason:
        Admin may need to correct court details.
        """
        self.__sport_type = sport_type
class EventHall(Facility):
    """
    EventHall represents large event spaces.

    Purpose:
    - Allows internal and external usage.
    - Makes internal use free and external use paid.

    Logical reason:
    EventHall has special pricing, so it overrides calculate_cost().
    """
    def __init__(self, facility_id, location, capacity, external_rate):
        """
        Constructor purpose:
        - Creates a new object and prepares its starting data.

        Logical reason:
        Each object must begin with valid attributes before the system can use it.
        """
        super().__init__(
            facility_id,
            "Event Hall",
            "EVENT_HALL",
            location,
            capacity,
            external_rate,
            "Rules: Internal use is free. External use requires payment."
        )
        self.__internal_use_free = True
        self.__external_rate = external_rate

    def get_internal_use_free(self):
        """
        Purpose:
        - Returns whether internal EventHall use is free.

        Logical reason:
        This supports EventHall payment rules.
        """
        return self.__internal_use_free

    def set_internal_use_free(self, internal_use_free):
        """
        Purpose:
        - Updates internal-use payment rule.

        Logical reason:
        Admin may need to change hall policy.
        """
        self.__internal_use_free = internal_use_free

    def get_external_rate(self):
        """
        Purpose:
        - Returns external EventHall rate.

        Logical reason:
        External booking payment uses this value.
        """
        return self.__external_rate

    def set_external_rate(self, external_rate):
        """
        Purpose:
        - Updates external EventHall rate.

        Logical reason:
        Admin may adjust event hall pricing.
        """
        self.__external_rate = external_rate
        self.set_price_per_hour(external_rate)

    def calculate_cost(self, usage_type):
        """
        Purpose:
        - Calculates facility booking cost.

        Logical reason:
        Payment depends on the selected facility and usage type.
        """
        if usage_type == UsageType.INTERNAL.value:
            return 0
        return self.__external_rate
class TimeSlot:
    """
    TimeSlot represents a time period.

    Purpose:
    - Stores start and end time.
    - Tracks whether a slot is booked.

    Logical reason:
    This matches the UML TimeSlot class, even though the GUI mainly uses string slots.
    """
    def __init__(self, slot_id, start_time, end_time):
        """
        Constructor purpose:
        - Creates a new object and prepares its starting data.

        Logical reason:
        Each object must begin with valid attributes before the system can use it.
        """
        self.__slot_id = slot_id
        self.__start_time = start_time
        self.__end_time = end_time
        self.__is_booked = False

    def get_slot_id(self):
        """
        Purpose:
        - Returns slot ID.

        Logical reason:
        Time slots need identifiers for tracking.
        """
        return self.__slot_id

    def set_slot_id(self, slot_id):
        """
        Purpose:
        - Updates slot ID.

        Logical reason:
        Slot labels may need correction.
        """
        self.__slot_id = slot_id

    def get_start_time(self):
        """
        Purpose:
        - Returns slot start time.

        Logical reason:
        Time conflicts depend on start and end times.
        """
        return self.__start_time

    def set_start_time(self, start_time):
        """
        Purpose:
        - Updates slot start time.

        Logical reason:
        Admin may adjust slot timing.
        """
        self.__start_time = start_time

    def get_end_time(self):
        """
        Purpose:
        - Returns slot end time.

        Logical reason:
        Time conflicts depend on start and end times.
        """
        return self.__end_time

    def set_end_time(self, end_time):
        """
        Purpose:
        - Updates slot end time.

        Logical reason:
        Admin may adjust slot timing.
        """
        self.__end_time = end_time

    def get_is_booked(self):
        """
        Purpose:
        - Returns whether this TimeSlot is booked.

        Logical reason:
        The UML requires tracking booked state.
        """
        return self.__is_booked

    def set_is_booked(self, is_booked):
        """
        Purpose:
        - Updates booked status.

        Logical reason:
        Booking confirmation and cancellation must update slot state.
        """
        self.__is_booked = is_booked
