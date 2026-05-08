"""
users.py

This module contains the User inheritance group: User, Student, Staff, and Administrator.

We separated these classes together because they share the same parent class and many
common details such as ID, name, login, access type, status, and penalty credits.
This helped us debug the cancellation problem, because the penalty credits now belong
to the user object itself and the system can freeze the user automatically after repeated
violations instead of making the admin do it manually every time.
"""

from enums import UserRole, AccessType, UserStatus

"""
This file groups the User inheritance hierarchy.

Why this grouping is logical:
User is the parent class, while Student, Staff, and Administrator are child classes.
They are kept together because they share the same basic data and behavior, but each role
has its own booking purpose and system permissions. This clearly shows inheritance in the UML.
"""

class User:
    """
    User is the parent class for Student, Staff, and Administrator.

    Purpose:
    - Stores shared user information such as ID, name, email, password, role, access type, status, and penalty credits.
    - Provides shared actions like login, profile update, support contact, and access requests.

    Logical reason:
    Student, Staff, and Admin share common data, so inheritance avoids repeating the same code.
    """
    def __init__(self, user_id, university_id, name, email, password, role):
        """
        Constructor purpose:
        - Creates a new object and prepares its starting data.

        Logical reason:
        Each object must begin with valid attributes before the system can use it.
        """
        if not user_id:
            raise ValueError("User ID cannot be empty.")
        if not university_id:
            raise ValueError("University/work ID cannot be empty.")
        if not name:
            raise ValueError("Name cannot be empty.")
        if "@" not in email:
            raise ValueError("Invalid email format.")
        if len(password) < 4:
            raise ValueError("Password must be at least 4 characters.")

        self.__user_id = user_id
        self.__university_id = university_id
        self.__name = name
        self.__email = email
        self.__password = password
        self.__role = role
        self.__access_type = AccessType.STANDARD
        self.__status = UserStatus.ACTIVE
        self.__penalty_credits = 3

    def get_user_id(self):
        """
        Purpose:
        - Returns the user ID so the system can identify the user.

        Logical reason:
        Many actions such as login, booking ownership, and admin updates depend on user ID.
        """
        return self.__user_id

    def set_user_id(self, user_id):
        """
        Purpose:
        - Updates the user ID after validation.

        Logical reason:
        Setters protect private attributes from invalid changes.
        """
        if not user_id:
            raise ValueError("User ID cannot be empty.")
        self.__user_id = user_id

    def get_university_id(self):
        """
        Purpose:
        - Returns university or work ID.

        Logical reason:
        This ID is used to create the system login ID.
        """
        return self.__university_id

    def set_university_id(self, university_id):
        """
        Purpose:
        - Updates university or work ID after validation.

        Logical reason:
        The system should not store empty identification data.
        """
        if not university_id:
            raise ValueError("University/work ID cannot be empty.")
        self.__university_id = university_id

    def get_name(self):
        """
        Purpose:
        - Returns the user's name for profiles, receipts, and dashboards.

        Logical reason:
        Readable names make booking records easier to understand.
        """
        return self.__name

    def set_name(self, name):
        """
        Purpose:
        - Updates the user's name after validation.

        Logical reason:
        Profile changes should still protect required data.
        """
        if not name:
            raise ValueError("Name cannot be empty.")
        self.__name = name

    def get_email(self):
        """
        Purpose:
        - Returns the user's email.

        Logical reason:
        Email is part of the profile and support contact information.
        """
        return self.__email

    def set_email(self, email):
        """
        Purpose:
        - Updates the email after checking its format.

        Logical reason:
        The system should not save invalid contact information.
        """
        if "@" not in email:
            raise ValueError("Invalid email format.")
        self.__email = email

    def get_password(self):
        """
        Purpose:
        - Returns the saved password for login checking.

        Logical reason:
        The login function needs to compare entered and stored passwords.
        """
        return self.__password

    def set_password(self, password):
        """
        Purpose:
        - Updates the password with a minimum length rule.

        Logical reason:
        This prevents very weak or empty passwords.
        """
        if len(password) < 4:
            raise ValueError("Password must be at least 4 characters.")
        self.__password = password

    def get_role(self):
        """
        Purpose:
        - Returns the user's role.

        Logical reason:
        Access rules depend on whether the user is Student, Staff, or Admin.
        """
        return self.__role

    def set_role(self, role):
        """
        Purpose:
        - Updates the role only if it is a valid UserRole enum.

        Logical reason:
        This prevents invalid role values.
        """
        if not isinstance(role, UserRole):
            raise TypeError("role must be UserRole.")
        self.__role = role

    def get_access_type(self):
        """
        Purpose:
        - Returns STANDARD or PREMIUM access.

        Logical reason:
        Facility permissions and booking credits depend on access type.
        """
        return self.__access_type

    def set_access_type(self, access_type):
        """
        Purpose:
        - Updates access level after validation.

        Logical reason:
        Upgrade and downgrade actions must change this value safely.
        """
        if not isinstance(access_type, AccessType):
            raise TypeError("accessType must be AccessType.")
        self.__access_type = access_type

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
        if not isinstance(status, UserStatus):
            raise TypeError("status must be UserStatus.")
        self.__status = status

    def get_penalty_credits(self):
        """
        Purpose:
        - Returns remaining penalty credits.

        Logical reason:
        The system uses this to decide if the user should be frozen.
        """
        return self.__penalty_credits

    def set_penalty_credits(self, penalty_credits):
        """
        Purpose:
        - Updates penalty credits after checking the value is not negative.

        Logical reason:
        Penalty credits should stay within valid values.
        """
        if penalty_credits < 0:
            raise ValueError("Penalty credits cannot be negative.")
        self.__penalty_credits = penalty_credits

    def decrease_penalty_credit(self):
        """
        Purpose:
        - Reduces penalty credits after a violation.

        Logical reason:
        Repeated cancellations or no-shows should have consequences.
        """
        if self.__penalty_credits > 0:
            self.__penalty_credits -= 1

    def reset_penalty_credits(self):
        """
        Purpose:
        - Restores penalty credits and reactivates the user.

        Logical reason:
        Admin needs a way to restore frozen users.
        """
        self.__penalty_credits = 3
        self.__status = UserStatus.ACTIVE

    def login(self, user_id, password):
        """
        Purpose:
        - Checks user ID and password.

        Logical reason:
        Only valid users should enter the system.
        """
        return self.__user_id == user_id and self.__password == password

    def update_profile(self, name, email):
        """
        Purpose:
        - Updates name and email through validation setters.

        Logical reason:
        Users should be able to edit their profile safely.
        """
        self.set_name(name)
        self.set_email(email)

    def request_access_upgrade(self):
        """
        Purpose:
        - Records that a user wants premium access.

        Logical reason:
        Upgrade request is a user action before payment/admin approval.
        """
        return "Upgrade request submitted."

    def request_access_downgrade(self):
        """
        Purpose:
        - Changes the user's access back to STANDARD.

        Logical reason:
        Downgrades do not require payment in the business rules.
        """
        self.__access_type = AccessType.STANDARD

    def contact_support(self, subject, message):
        """
        Purpose:
        - Lets a user submit a support message.

        Logical reason:
        Users need a way to report issues such as upgrade or booking problems.
        """
        if not subject or not message:
            raise ValueError("Subject and message are required.")
        return f"Support request submitted: {subject} - {message}"
class Student(User):
    """
    Student represents a student actor in the system.

    Purpose:
    - Stores student-specific booking records.
    - Uses the shared User behavior from the parent class.

    Logical reason:
    Students follow different booking rules from staff, so they are modeled as their own class.
    """
    def __init__(self, user_id, university_id, name, email, password):
        """
        Constructor purpose:
        - Creates a new object and prepares its starting data.

        Logical reason:
        Each object must begin with valid attributes before the system can use it.
        """
        super().__init__(user_id, university_id, name, email, password, UserRole.STUDENT)
        self.__student_bookings = {}

    def get_student_bookings(self):
        """
        Purpose:
        - Returns student-specific booking records.

        Logical reason:
        Student booking history may be displayed in profile or tests.
        """
        return self.__student_bookings

    def set_student_bookings(self, student_bookings):
        """
        Purpose:
        - Updates student booking dictionary.

        Logical reason:
        The value must stay a dictionary for organized storage.
        """
        if not isinstance(student_bookings, dict):
            raise TypeError("studentBookings must be dictionary.")
        self.__student_bookings = student_bookings

    def view_student_bookings(self):
        """
        Purpose:
        - Displays all bookings for the student.

        Logical reason:
        Students need to review their own reservations.
        """
        return self.__student_bookings
class Staff(User):
    """
    Staff represents a staff actor in the system.

    Purpose:
    - Stores staff-specific booking records.
    - Uses the shared User behavior from the parent class.

    Logical reason:
    Staff can book different facilities from students, so they need a separate child class.
    """
    def __init__(self, user_id, university_id, name, email, password):
        """
        Constructor purpose:
        - Creates a new object and prepares its starting data.

        Logical reason:
        Each object must begin with valid attributes before the system can use it.
        """
        super().__init__(user_id, university_id, name, email, password, UserRole.STAFF)
        self.__staff_bookings = {}

    def get_staff_bookings(self):
        """
        Purpose:
        - Returns staff-specific booking records.

        Logical reason:
        Staff booking history may be displayed in profile or tests.
        """
        return self.__staff_bookings

    def set_staff_bookings(self, staff_bookings):
        """
        Purpose:
        - Updates staff booking dictionary.

        Logical reason:
        The value must stay a dictionary for organized storage.
        """
        if not isinstance(staff_bookings, dict):
            raise TypeError("staffBookings must be dictionary.")
        self.__staff_bookings = staff_bookings

    def view_staff_bookings(self):
        """
        Purpose:
        - Displays all bookings for the staff member.

        Logical reason:
        Staff need to review their own reservations.
        """
        return self.__staff_bookings
class Administrator(User):
    """
    Administrator represents the admin actor.

    Purpose:
    - Freezes and restores users.
    - Supports admin management actions in the GUI.

    Logical reason:
    Admin users have management permissions that normal students and staff should not have.
    """
    def __init__(self, user_id, university_id, name, email, password):
        """
        Constructor purpose:
        - Creates a new object and prepares its starting data.

        Logical reason:
        Each object must begin with valid attributes before the system can use it.
        """
        super().__init__(user_id, university_id, name, email, password, UserRole.ADMIN)
        self.__admin_bookings_view = {}

    def get_admin_bookings_view(self):
        """
        Purpose:
        - Returns the admin booking view.

        Logical reason:
        Admin needs to monitor system activity.
        """
        return self.__admin_bookings_view

    def set_admin_bookings_view(self, admin_bookings_view):
        """
        Purpose:
        - Updates admin booking view dictionary.

        Logical reason:
        Admin dashboard data should stay organized.
        """
        if not isinstance(admin_bookings_view, dict):
            raise TypeError("adminBookingsView must be dictionary.")
        self.__admin_bookings_view = admin_bookings_view

    def freeze_user(self, user):
        """
        Purpose:
        - Freezes selected user.

        Logical reason:
        Admin can punish users who break rules.
        """
        user.set_status(UserStatus.FROZEN)

    def restore_user(self, user):
        """
        Purpose:
        - Restores user penalty credits and active status.

        Logical reason:
        Admin needs a way to give booking access back.
        """
        user.reset_penalty_credits()
