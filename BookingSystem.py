"""
BookingSystem.py

This module contains the BookingSystem controller class.

We separated this controller because it connects the other modules together: users,
facilities, bookings, payments, receipts, notifications, access rules, and saved data.
This made debugging easier because the main business process can be followed step by
step, such as login, upgrade payment, booking, cancellation, automatic freezing, and
admin slot closure.
"""

import pickle
import os
from datetime import datetime, date

from enums import UserRole, AccessType, UserStatus, BookingStatus, PaymentPurpose
from users import Student, Staff, Administrator
from facilities import StudyRoom, SportsCourt, EventHall
from Booking import Booking
from PaymentReceipt import Payment, Receipt
from Notification import Notification
from AccessPolicy import AccessPolicy
from FacilityCatalog import FacilityCatalog

"""
This file stores the BookingSystem controller class.

Why this file is separate:
BookingSystem is the main backend controller. It connects users, facilities, bookings,
payments, receipts, notifications, policies, and file storage. It is separated because it
contains the main system logic rather than one specific entity.
"""

class BookingSystem:
    """
    BookingSystem is the main controller for the backend system.

    Purpose:
    - Stores users, bookings, payments, receipts, notifications, announcements, and facilities.
    - Handles registration, login, booking, payment, penalties, admin actions, and pickle persistence.

    Logical reason:
    The full system needs one central controller to connect all classes together.
    """
    def __init__(self):
        """
        Constructor purpose:
        - Creates a new object and prepares its starting data.

        Logical reason:
        Each object must begin with valid attributes before the system can use it.
        """
        self.__system_name = "Smart Campus Facility Booking System"
        self.__support_email = "support@campus.ae"
        self.__users = {}
        self.__bookings = {}
        self.__payments = {}
        self.__receipts = {}
        self.__notifications = {}
        self.__announcements = []
        self.__facility_catalog = FacilityCatalog()
        self.__access_policy = AccessPolicy()
        self.__data_file_name = "smart_campus_data.dat"
        self.__session_file_name = "smart_campus_session.dat"
        self.__current_user_id = ""
        self.__remember_login = False
        self.__next_booking_number = 1

        self.load_data_from_file(self.__data_file_name)
        self.repair_loaded_data()

        if not self.__facility_catalog.get_facilities():
            self.create_default_facilities()

        self.load_session()

    def get_system_name(self):
        """
        Purpose:
        - Returns system name.

        Logical reason:
        The GUI can display it as the application title.
        """
        return self.__system_name

    def get_support_email(self):
        """
        Purpose:
        - Returns support email.

        Logical reason:
        Users need contact information for help.
        """
        return self.__support_email

    def get_users(self):
        """
        Purpose:
        - Returns all registered users.

        Logical reason:
        Admin dashboard needs user records.
        """
        return self.__users

    def get_bookings(self):
        """
        Purpose:
        - Returns all bookings.

        Logical reason:
        Users and admins need booking records.
        """
        return self.__bookings

    def get_payments(self):
        """
        Purpose:
        - Returns all payments.

        Logical reason:
        Payment history needs storage and display.
        """
        return self.__payments

    def get_receipts(self):
        """
        Purpose:
        - Returns all receipts.

        Logical reason:
        Receipts must be retrievable after booking.
        """
        return self.__receipts

    def get_notifications(self):
        """
        Purpose:
        - Returns notifications.

        Logical reason:
        Notifications must be saved and displayed.
        """
        return self.__notifications

    def get_announcements(self):
        """
        Purpose:
        - Returns announcements.

        Logical reason:
        Users need to see maintenance messages.
        """
        return self.__announcements

    def get_facility_catalog(self):
        """
        Purpose:
        - Returns catalog object.

        Logical reason:
        Other parts of the system need access to facilities.
        """
        return self.__facility_catalog

    def get_current_user_id(self):
        """
        Purpose:
        - Returns logged-in user ID.

        Logical reason:
        Booking and cancellation depend on current user.
        """
        return self.__current_user_id

    def get_current_user(self):
        """
        Purpose:
        - Returns logged-in user object.

        Logical reason:
        Screens and booking logic depend on the active user.
        """
        if self.__current_user_id in self.__users:
            return self.__users[self.__current_user_id]
        return None

    def create_default_facilities(self):
        """
        Purpose:
        - Creates default facilities when no saved data exists.

        Logical reason:
        The system needs facilities available immediately after first launch.
        """
        self.__facility_catalog.add_facility(StudyRoom("SR-A", "A", "Library - Floor 1", 6))
        self.__facility_catalog.add_facility(StudyRoom("SR-B", "B", "Library - Floor 2", 4))
        self.__facility_catalog.add_facility(SportsCourt("SC-B", "Basketball", "Sports Complex", 10, 20))
        self.__facility_catalog.add_facility(SportsCourt("SC-T", "Tennis", "Sports Complex", 4, 15))
        self.__facility_catalog.add_facility(EventHall("EH-1", "Main Building", 50, 100))
        self.__facility_catalog.add_facility(EventHall("EH-2", "Conference Building", 100, 150))

    def repair_loaded_data(self):
        """
        Purpose:
        - Adds missing attributes to old loaded objects.

        Logical reason:
        Saved pickle data from older code versions may not have new attributes.
        """
        for user in self.__users.values():
            if not hasattr(user, "_User__penalty_credits"):
                user.set_penalty_credits(3)

        for facility in self.__facility_catalog.get_facilities().values():
            if not hasattr(facility, "_Facility__booked_slots_by_date"):
                facility.set_booked_slots_by_date({})
            if not hasattr(facility, "_Facility__closed_slots_by_date"):
                facility.set_closed_slots_by_date({})

    def save_data_to_file(self, file_name):
        """
        Purpose:
        - Saves system data using pickle.

        Logical reason:
        Data must persist after closing the program.
        """
        try:
            with open(file_name, "wb") as file:
                pickle.dump({
                    "users": self.__users,
                    "bookings": self.__bookings,
                    "payments": self.__payments,
                    "receipts": self.__receipts,
                    "notifications": self.__notifications,
                    "announcements": self.__announcements,
                    "facility_catalog": self.__facility_catalog,
                    "next_booking_number": self.__next_booking_number
                }, file)
            return True
        except (pickle.PickleError, OSError) as error:
            raise OSError(f"Saving failed: {error}")

    def load_data_from_file(self, file_name):
        """
        Purpose:
        - Loads saved system data.

        Logical reason:
        Users, bookings, and admin changes should remain after restarting.
        """
        try:
            if os.path.exists(file_name):
                with open(file_name, "rb") as file:
                    data = pickle.load(file)

                self.__users = data.get("users", {})
                self.__bookings = data.get("bookings", {})
                self.__payments = data.get("payments", {})
                self.__receipts = data.get("receipts", {})
                self.__notifications = data.get("notifications", {})
                self.__announcements = data.get("announcements", [])
                self.__facility_catalog = data.get("facility_catalog", FacilityCatalog())
                self.__next_booking_number = data.get("next_booking_number", 1)

            return self
        except (EOFError, pickle.UnpicklingError, OSError, AttributeError):
            self.__users = {}
            self.__bookings = {}
            self.__payments = {}
            self.__receipts = {}
            self.__notifications = {}
            self.__announcements = []
            self.__facility_catalog = FacilityCatalog()
            self.__next_booking_number = 1
            return self

    def save_session(self, user_id):
        """
        Purpose:
        - Saves remembered login session.

        Logical reason:
        The remember-me checkbox needs persistent login data.
        """
        try:
            with open(self.__session_file_name, "wb") as file:
                pickle.dump({"current_user_id": user_id}, file)
            return True
        except OSError:
            return False

    def load_session(self):
        """
        Purpose:
        - Loads remembered login session.

        Logical reason:
        Users can return without logging in again.
        """
        try:
            if os.path.exists(self.__session_file_name):
                with open(self.__session_file_name, "rb") as file:
                    data = pickle.load(file)

                user_id = data.get("current_user_id", "")
                if user_id in self.__users:
                    self.__current_user_id = user_id
                    return self.__users[user_id]
            return None
        except (EOFError, pickle.UnpicklingError, OSError, AttributeError):
            return None

    def logout(self):
        """
        Purpose:
        - Clears current session.

        Logical reason:
        Users need to safely exit their account.
        """
        self.__current_user_id = ""
        if os.path.exists(self.__session_file_name):
            os.remove(self.__session_file_name)

    def generate_user_id(self, role, university_id):
        """
        Purpose:
        - Builds login ID from role and university/work ID.

        Logical reason:
        This makes IDs consistent, like STU20240001 or ADM1000.
        """
        if role == UserRole.STUDENT:
            return "STU" + university_id
        if role == UserRole.STAFF:
            return "STF" + university_id
        if role == UserRole.ADMIN:
            return "ADM" + university_id
        raise ValueError("Invalid role.")

    def register_user(self, role, university_id, name, email, password):
        """
        Purpose:
        - Creates and stores a new user account.

        Logical reason:
        The system needs registration before login and booking.
        """
        user_id = self.generate_user_id(role, university_id)

        if user_id in self.__users:
            raise ValueError("This account already exists.")

        if role == UserRole.STUDENT:
            user = Student(user_id, university_id, name, email, password)
        elif role == UserRole.STAFF:
            user = Staff(user_id, university_id, name, email, password)
        elif role == UserRole.ADMIN:
            user = Administrator(user_id, university_id, name, email, password)
        else:
            raise ValueError("Invalid role.")

        self.__users[user_id] = user
        self.save_data_to_file(self.__data_file_name)
        return user

    def validate_login(self, user_id, password, remember_login=False):
        """
        Purpose:
        - Checks user ID and password.

        Logical reason:
        Only registered users should access the dashboard.
        """
        if user_id not in self.__users:
            raise ValueError(
                "User ID not found.\n\n"
                "Example:\n"
                "Student 20240001 becomes STU20240001\n"
                "Staff 8899 becomes STF8899\n"
                "Admin 1000 becomes ADM1000"
            )

        user = self.__users[user_id]

        if not user.login(user_id, password):
            raise PermissionError("Incorrect password.")

        self.__current_user_id = user_id
        self.__remember_login = remember_login

        if remember_login:
            self.save_session(user_id)

        return user

    def validate_weekday_booking(self, selected_date):
        """
        Purpose:
        - Blocks weekend bookings.

        Logical reason:
        The business rule only allows Monday to Friday reservations.
        """
        booking_day = datetime.strptime(selected_date, "%Y-%m-%d").date()
        if booking_day.weekday() >= 5:
            raise ValueError("Bookings are only allowed from Monday to Friday.")
        return True

    def get_allowed_facilities(self, user):
        """
        Purpose:
        - Returns facilities the current user can book.

        Logical reason:
        The GUI should only show valid options to reduce errors.
        """
        allowed = {}
        for facility_id, facility in self.__facility_catalog.get_facilities().items():
            if facility.get_is_available() and self.__access_policy.can_book(user, facility):
                allowed[facility_id] = facility
        return allowed

    def count_user_bookings_on_date(self, user, selected_date):
        """
        Purpose:
        - Counts user bookings on one date.

        Logical reason:
        STANDARD users only have 1 booking credit per day.
        """
        count = 0
        for booking in self.__bookings.values():
            if (
                booking.get_user().get_user_id() == user.get_user_id()
                and booking.get_booking_date() == selected_date
                and booking.get_status() == BookingStatus.CONFIRMED
            ):
                count += 1
        return count

    def count_user_facility_type_bookings_on_date(self, user, facility_type, selected_date):
        """
        Purpose:
        - Counts premium user bookings by facility type.

        Logical reason:
        PREMIUM users have 3 credits per facility type per day.
        """
        count = 0
        for booking in self.__bookings.values():
            if (
                booking.get_user().get_user_id() == user.get_user_id()
                and booking.get_facility().get_facility_type() == facility_type
                and booking.get_booking_date() == selected_date
                and booking.get_status() == BookingStatus.CONFIRMED
            ):
                count += 1
        return count

    def get_daily_credit_text(self, user, selected_date=None):
        """
        Purpose:
        - Creates readable credit information.

        Logical reason:
        The dashboard should show remaining booking and penalty credits.
        """
        if selected_date is None:
            selected_date = str(date.today())

        if user.get_access_type() == AccessType.STANDARD:
            used = self.count_user_bookings_on_date(user, selected_date)
            return f"Booking Credit: {max(0, 1 - used)} / 1 | Penalty Credit: {user.get_penalty_credits()} / 3"

        allowed_types = set()
        for facility in self.get_allowed_facilities(user).values():
            allowed_types.add(facility.get_facility_type())

        credit_lines = []
        for facility_type in allowed_types:
            used = self.count_user_facility_type_bookings_on_date(user, facility_type, selected_date)
            credit_lines.append(f"{facility_type}: {max(0, 3 - used)} / 3")

        return " | ".join(credit_lines) + f" | Penalty Credit: {user.get_penalty_credits()} / 3"

    def check_booking_credit(self, user, facility, selected_date):
        """
        Purpose:
        - Enforces booking credit limits.

        Logical reason:
        Users should not exceed their daily booking allowance.
        """
        if user.get_access_type() == AccessType.STANDARD:
            if self.count_user_bookings_on_date(user, selected_date) >= 1:
                raise PermissionError("STANDARD access allows only 1 booking per day.")

        if user.get_access_type() == AccessType.PREMIUM:
            used = self.count_user_facility_type_bookings_on_date(
                user,
                facility.get_facility_type(),
                selected_date
            )
            if used >= 3:
                raise PermissionError(
                    f"PREMIUM access allows only 3 bookings per {facility.get_facility_type()} per day."
                )

    def check_booking_conflict(self, user, slot, selected_date):
        """
        Purpose:
        - Prevents same-time double booking.

        Logical reason:
        A user cannot reserve two facilities at the same time.
        """
        for booking in self.__bookings.values():
            if (
                booking.get_user().get_user_id() == user.get_user_id()
                and booking.get_booking_date() == selected_date
                and booking.get_slot() == slot
                and booking.get_status() == BookingStatus.CONFIRMED
            ):
                return True
        return False

    def auto_freeze_if_needed(self, user):
        """
        Purpose:
        - Freezes user automatically after penalty credits reach 0.

        Logical reason:
        Three violations should remove booking privileges.
        """
        if user.get_penalty_credits() <= 0:
            user.set_status(UserStatus.FROZEN)
            notification_id = "N-FREEZE-" + user.get_user_id()
            self.__notifications[notification_id] = Notification(
                notification_id,
                "Your account has been automatically frozen because you reached 3 violations."
            )

    def record_cancellation_violation(self, user):
        """
        Purpose:
        - Applies penalty after cancellation.

        Logical reason:
        Repeated cancellations should affect user status.
        """
        user.decrease_penalty_credit()
        self.auto_freeze_if_needed(user)
        self.save_data_to_file(self.__data_file_name)

    def record_no_show_violation(self, user):
        """
        Purpose:
        - Applies penalty after no-show.

        Logical reason:
        No-shows waste facility slots and should be punished.
        """
        user.decrease_penalty_credit()
        self.auto_freeze_if_needed(user)
        self.save_data_to_file(self.__data_file_name)

    def create_booking_after_payment(self, facility_id, slot, selected_date, usage_type):
        """
        Purpose:
        - Creates booking, payment, receipt, notification, and saves data.

        Logical reason:
        Booking should only be finalized after all rules and payment logic pass.
        """
        user = self.get_current_user()
        facility = self.__facility_catalog.get_facility(facility_id)

        if user.get_status() == UserStatus.FROZEN:
            raise PermissionError("Your account is FROZEN. You cannot book.")

        if not facility.get_is_available():
            raise PermissionError("Facility is unavailable.")

        datetime.strptime(selected_date, "%Y-%m-%d")
        self.validate_weekday_booking(selected_date)

        if datetime.strptime(selected_date, "%Y-%m-%d").date() < date.today():
            raise ValueError("Booking date cannot be in the past.")

        if not self.__access_policy.can_book(user, facility):
            raise PermissionError("You cannot book this facility.")

        if slot not in facility.get_available_slots(selected_date):
            raise ValueError("This slot is already booked or closed.")

        if self.check_booking_conflict(user, slot, selected_date):
            raise ValueError("You already have a booking at this time.")

        self.check_booking_credit(user, facility, selected_date)

        total_cost = facility.calculate_cost(usage_type)

        booking_id = "B" + str(self.__next_booking_number).zfill(4)
        self.__next_booking_number += 1

        booking = Booking(booking_id, user, facility, slot, selected_date, usage_type, total_cost)
        self.__bookings[booking_id] = booking
        facility.book_slot(selected_date, slot, booking_id)

        payment = Payment("P" + booking_id, total_cost, PaymentPurpose.BOOKING_FEE)
        payment.process_payment()
        self.__payments[payment.get_payment_id()] = payment

        receipt = Receipt("R" + booking_id, booking, payment)
        self.__receipts[receipt.get_receipt_id()] = receipt

        notification = Notification("N" + booking_id, f"Booking {booking_id} confirmed.")
        self.__notifications[notification.get_notification_id()] = notification

        self.save_data_to_file(self.__data_file_name)
        return booking, receipt

    def cancel_booking(self, booking_id):
        """
        Purpose:
        - Marks a booking as cancelled.

        Logical reason:
        Cancelled bookings should no longer count as active.
        """
        if booking_id not in self.__bookings:
            raise ValueError("Booking not found.")

        booking = self.__bookings[booking_id]

        if booking.get_user().get_user_id() != self.__current_user_id:
            raise PermissionError("You can only cancel your own booking.")

        booking.get_facility().release_slot(booking.get_booking_date(), booking.get_slot())
        booking.cancel_booking()
        self.record_cancellation_violation(booking.get_user())
        self.save_data_to_file(self.__data_file_name)

    def modify_booking(self, booking_id, new_slot, new_date):
        """
        Purpose:
        - Changes booking slot and date.

        Logical reason:
        Users need flexibility to update bookings while keeping availability correct.
        """
        if booking_id not in self.__bookings:
            raise ValueError("Booking not found.")

        booking = self.__bookings[booking_id]

        if booking.get_user().get_user_id() != self.__current_user_id:
            raise PermissionError("You can only modify your own booking.")

        self.validate_weekday_booking(new_date)

        facility = booking.get_facility()

        if new_slot not in facility.get_available_slots(new_date):
            raise ValueError("New slot is not available.")

        datetime.strptime(new_date, "%Y-%m-%d")

        facility.release_slot(booking.get_booking_date(), booking.get_slot())
        booking.set_slot(new_slot)
        booking.set_booking_date(new_date)
        facility.book_slot(new_date, new_slot, booking_id)

        self.save_data_to_file(self.__data_file_name)

    def mark_booking_no_show(self, booking_id):
        """
        Purpose:
        - Marks a booking as no-show and applies penalty.

        Logical reason:
        Admin must be able to punish missed bookings.
        """
        if booking_id not in self.__bookings:
            raise ValueError("Booking not found.")

        booking = self.__bookings[booking_id]
        user = booking.get_user()

        booking.get_facility().release_slot(booking.get_booking_date(), booking.get_slot())
        booking.mark_no_show()

        self.record_no_show_violation(user)
        self.save_data_to_file(self.__data_file_name)

    def process_upgrade_payment(self):
        """
        Purpose:
        - Processes premium upgrade payment.

        Logical reason:
        Users pay 30 AED before receiving PREMIUM access.
        """
        user = self.get_current_user()

        if user.get_access_type() == AccessType.PREMIUM:
            raise ValueError("User already has PREMIUM access.")

        payment = Payment("P-UP-" + user.get_user_id(), 30, PaymentPurpose.ACCESS_UPGRADE)
        payment.process_payment()
        self.__payments[payment.get_payment_id()] = payment

        user.set_access_type(AccessType.PREMIUM)
        self.save_data_to_file(self.__data_file_name)

    def downgrade_current_user(self):
        """
        Purpose:
        - Downgrades current user to STANDARD.

        Logical reason:
        Users can return to standard access without payment.
        """
        user = self.get_current_user()
        user.set_access_type(AccessType.STANDARD)
        self.save_data_to_file(self.__data_file_name)

    def freeze_user(self, user_id):
        """
        Purpose:
        - Freezes selected user.

        Logical reason:
        Admin can punish users who break rules.
        """
        if user_id not in self.__users:
            raise ValueError("User not found.")
        self.__users[user_id].set_status(UserStatus.FROZEN)
        self.save_data_to_file(self.__data_file_name)

    def unfreeze_user(self, user_id):
        """
        Purpose:
        - Restores selected user account.

        Logical reason:
        Admin can give access back after punishment.
        """
        if user_id not in self.__users:
            raise ValueError("User not found.")
        self.__users[user_id].reset_penalty_credits()
        self.save_data_to_file(self.__data_file_name)

    def upgrade_user_by_admin(self, user_id):
        """
        Purpose:
        - Admin upgrades a user to PREMIUM.

        Logical reason:
        Admin can help when upgrade issues happen.
        """
        if user_id not in self.__users:
            raise ValueError("User not found.")
        self.__users[user_id].set_access_type(AccessType.PREMIUM)
        self.save_data_to_file(self.__data_file_name)

    def downgrade_user_by_admin(self, user_id):
        """
        Purpose:
        - Admin downgrades a user to STANDARD.

        Logical reason:
        Admin can correct or manage access levels.
        """
        if user_id not in self.__users:
            raise ValueError("User not found.")
        self.__users[user_id].set_access_type(AccessType.STANDARD)
        self.save_data_to_file(self.__data_file_name)

    def close_facility_slot(self, facility_id, selected_date, slot):
        """
        Purpose:
        - Closes a specific facility slot.

        Logical reason:
        Admin can block bookings during maintenance.
        """
        facility = self.__facility_catalog.get_facility(facility_id)
        if facility is None:
            raise ValueError("Facility not found.")
        facility.close_slot(selected_date, slot)
        self.save_data_to_file(self.__data_file_name)

    def open_facility_slot(self, facility_id, selected_date, slot):
        """
        Purpose:
        - Reopens a closed slot.

        Logical reason:
        Admin can make a slot available again after maintenance.
        """
        facility = self.__facility_catalog.get_facility(facility_id)
        if facility is None:
            raise ValueError("Facility not found.")
        facility.open_slot(selected_date, slot)
        self.save_data_to_file(self.__data_file_name)

    def add_announcement(self, message):
        """
        Purpose:
        - Adds announcement with timestamp.

        Logical reason:
        Users need to see system updates and maintenance messages.
        """
        if not message:
            raise ValueError("Announcement cannot be empty.")
        stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.__announcements.append(f"{stamp}: {message}")
        self.save_data_to_file(self.__data_file_name)

    def get_bookings_by_date(self, selected_date):
        """
        Purpose:
        - Returns bookings for one selected date.

        Logical reason:
        Admin monitoring depends on daily booking reports.
        """
        return {
            booking_id: booking
            for booking_id, booking in self.__bookings.items()
            if booking.get_booking_date() == selected_date
        }
