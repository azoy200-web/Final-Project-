"""
enums.py

This module keeps the fixed choices of the system in one place, such as user roles,
access types, booking status, payment status, and usage type.

We separated these values because many errors can happen when the same words are typed
manually in different parts of the code. For example, booking rules, payment rules,
and user status checks all depend on these exact values, so keeping them here makes
the code easier to check and debug.
"""

from enum import Enum

"""
This file groups all Enum classes together.

Why this grouping is logical:
Enums are shared fixed values used across the whole project, such as roles, access types,
booking status, payment status, and usage type. Keeping them in one file avoids repeating
strings and prevents spelling mistakes in the booking rules.
"""

class UserRole(Enum):
    """
    UserRole stores the allowed actor types in the system.

    Purpose:
    - STUDENT, STAFF, and ADMIN are the only valid roles.
    - This prevents spelling mistakes and keeps role checks consistent.

    Logical reason:
    Booking rules depend on the role, so using an Enum makes the code safer than using random strings.
    """
    STUDENT = "STUDENT"
    STAFF = "STAFF"
    ADMIN = "ADMIN"
class AccessType(Enum):
    """
    AccessType stores the access level of a user.

    Purpose:
    - STANDARD users have limited booking permissions.
    - PREMIUM users have extra booking permissions and more booking credits.

    Logical reason:
    The system needs a clear way to check if a user can book premium facilities.
    """
    STANDARD = "STANDARD"
    PREMIUM = "PREMIUM"
class UserStatus(Enum):
    """
    UserStatus stores whether the user account is active or frozen.

    Purpose:
    - ACTIVE users can use the system normally.
    - FROZEN users are blocked from making bookings.

    Logical reason:
    This supports the penalty rule where users can be frozen after repeated violations.
    """
    ACTIVE = "ACTIVE"
    FROZEN = "FROZEN"
class BookingStatus(Enum):
    """
    BookingStatus tracks the lifecycle of a booking.

    Purpose:
    - CONFIRMED means the booking is active.
    - CANCELLED means the booking was cancelled.
    - NO_SHOW means the user did not attend.

    Logical reason:
    The admin dashboard and penalty system need to know the booking state.
    """
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    NO_SHOW = "NO_SHOW"
class UsageType(Enum):
    """
    UsageType explains why the facility is being used.

    Purpose:
    - INTERNAL use can be free for EventHall.
    - EXTERNAL use may require payment.

    Logical reason:
    EventHall cost depends on whether the booking is internal or external.
    """
    INTERNAL = "INTERNAL"
    EXTERNAL = "EXTERNAL"
class PaymentStatus(Enum):
    """
    PaymentStatus tracks payment progress and result.

    Purpose:
    - NOT_REQUIRED is used for free bookings.
    - PAID is used after a successful payment.
    - REFUNDED is available for returned payments.

    Logical reason:
    Receipts and booking records need a clear payment state.
    """
    NOT_REQUIRED = "NOT_REQUIRED"
    PENDING = "PENDING"
    PAID = "PAID"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"
class PaymentPurpose(Enum):
    """
    PaymentPurpose explains why a payment was created.

    Purpose:
    - BOOKING_FEE is used for paid facility bookings.
    - ACCESS_UPGRADE is used for upgrading to premium.

    Logical reason:
    This helps separate booking payments from upgrade payments.
    """
    BOOKING_FEE = "BOOKING_FEE"
    ACCESS_UPGRADE = "ACCESS_UPGRADE"
