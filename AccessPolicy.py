"""
AccessPolicy.py

This module contains the AccessPolicy class.

We separated the access rules because the booking permissions changed during debugging.
For example, we found that credits per room or court were not logical, so the permission
and access checks needed to be easier to review without searching through the full
booking system code.
"""

from enums import UserRole, AccessType

"""
This file stores the AccessPolicy class.

Why this file is separate:
AccessPolicy contains the booking permission rules. It is separated from User and Facility
so the business rules are easy to update without changing the data classes.
"""

class AccessPolicy:
    """
    AccessPolicy controls booking permission rules.

    Purpose:
    - Checks role, access type, and facility type.

    Logical reason:
    Putting permission rules in one class makes the code easier to maintain and keeps the business logic clear.
    """
    def can_book(self, user, facility):
        """
        Purpose:
        - Checks whether a user can book a facility.

        Logical reason:
        This enforces role and access rules before booking is created.
        """
        role = user.get_role()
        access = user.get_access_type()
        facility_type = facility.get_facility_type()

        if role == UserRole.ADMIN:
            return False

        if facility_type == "STUDY_ROOM":
            return role == UserRole.STUDENT

        if facility_type == "SPORTS_COURT":
            return access == AccessType.PREMIUM and role in [UserRole.STUDENT, UserRole.STAFF]

        if facility_type == "EVENT_HALL":
            if role == UserRole.STAFF:
                return True
            return role == UserRole.STUDENT and access == AccessType.PREMIUM

        return False
