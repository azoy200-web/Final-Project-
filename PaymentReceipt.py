"""
PaymentReceipt.py

This module contains the Payment and Receipt classes.

We grouped them together because the receipt depends on the payment result. This helped
us fix the first trial problems where the upgrade did not have a fee or bill, and the
booking bill was empty because the needed objects were not connected properly.
"""

from datetime import date
from enums import PaymentStatus

"""
This file groups Payment and Receipt together.

Why this grouping is logical:
Receipt depends directly on Payment because the receipt proves the booking/payment result.
Keeping them together shows the payment flow clearly: create payment, process payment,
then generate receipt as confirmation.
"""

class Payment:
    """
    Payment represents money handling for bookings or upgrades.

    Purpose:
    - Stores amount, date, status, and payment purpose.
    - Processes paid and free transactions.

    Logical reason:
    The system needs payment records to create receipts and show financial proof.
    """
    def __init__(self, payment_id, amount, purpose):
        """
        Constructor purpose:
        - Creates a new object and prepares its starting data.

        Logical reason:
        Each object must begin with valid attributes before the system can use it.
        """
        self.__payment_id = payment_id
        self.__amount = amount
        self.__payment_date = str(date.today())
        self.__status = PaymentStatus.PENDING if amount > 0 else PaymentStatus.NOT_REQUIRED
        self.__purpose = purpose

    def get_payment_id(self):
        """
        Purpose:
        - Returns payment ID.

        Logical reason:
        Payments need IDs for storage and receipts.
        """
        return self.__payment_id

    def get_amount(self):
        """
        Purpose:
        - Returns payment amount.

        Logical reason:
        Receipts and payment records need the amount.
        """
        return self.__amount

    def get_payment_date(self):
        """
        Purpose:
        - Returns payment date.

        Logical reason:
        Receipts need transaction date.
        """
        return self.__payment_date

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

    def get_purpose(self):
        """
        Purpose:
        - Returns payment purpose.

        Logical reason:
        The system should know if the payment was for booking or upgrade.
        """
        return self.__purpose

    def process_payment(self):
        """
        Purpose:
        - Completes payment processing.

        Logical reason:
        Paid bookings should become PAID, while free bookings should be NOT_REQUIRED.
        """
        if self.__amount == 0:
            self.__status = PaymentStatus.NOT_REQUIRED
        else:
            self.__status = PaymentStatus.PAID
        return True
class Receipt:
    """
    Receipt represents proof of a completed booking/payment.

    Purpose:
    - Combines booking and payment information into a readable receipt.

    Logical reason:
    Users need confirmation that their booking and payment were completed.
    """
    def __init__(self, receipt_id, booking, payment):
        """
        Constructor purpose:
        - Creates a new object and prepares its starting data.

        Logical reason:
        Each object must begin with valid attributes before the system can use it.
        """
        self.__receipt_id = receipt_id
        self.__booking = booking
        self.__payment = payment
        self.__issue_date = str(date.today())

    def get_receipt_id(self):
        """
        Purpose:
        - Returns receipt ID.

        Logical reason:
        Receipts need IDs for storage.
        """
        return self.__receipt_id

    def generate_receipt(self):
        """
        Purpose:
        - Creates receipt text.

        Logical reason:
        Users need proof of booking and payment.
        """
        return (
            "BOOKING RECEIPT\n"
            "----------------------\n"
            f"Receipt ID: {self.__receipt_id}\n"
            f"Issue Date: {self.__issue_date}\n"
            f"Payment Status: {self.__payment.get_status().value}\n"
            f"Payment Amount: {self.__payment.get_amount()} AED\n\n"
            f"{self.__booking.generate_booking_summary()}"
        )
