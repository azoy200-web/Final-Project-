"""
Notification.py

This module contains the Notification class.

We separated notifications because system messages are used in many places, such as
booking confirmation, admin announcements, and frozen account warnings. This made it
easier to debug user feedback because the system can clearly tell the user what happened
after an action.
"""

from datetime import date

"""
This file stores the Notification class.

Why this file is separate:
Notifications are system messages used after important actions such as booking confirmation
or account freezing. Separating it makes the communication feature easy to identify.
"""

class Notification:
    """
    Notification represents a system message.

    Purpose:
    - Stores booking confirmations, freeze warnings, and system updates.

    Logical reason:
    Users must be informed when important actions happen.
    """
    def __init__(self, notification_id, message):
        """
        Constructor purpose:
        - Creates a new object and prepares its starting data.

        Logical reason:
        Each object must begin with valid attributes before the system can use it.
        """
        self.__notification_id = notification_id
        self.__message = message
        self.__send_date = str(date.today())
        self.__is_read = False

    def get_notification_id(self):
        """
        Purpose:
        - Returns notification ID.

        Logical reason:
        Notifications need IDs for storage.
        """
        return self.__notification_id

    def get_message(self):
        """
        Purpose:
        - Returns notification message.

        Logical reason:
        The GUI displays this text to users.
        """
        return self.__message

    def get_send_date(self):
        """
        Purpose:
        - Returns notification date.

        Logical reason:
        Users and admins may need message history.
        """
        return self.__send_date

    def get_is_read(self):
        """
        Purpose:
        - Returns read/unread state.

        Logical reason:
        The GUI can separate unread notifications.
        """
        return self.__is_read

    def mark_as_read(self):
        """
        Purpose:
        - Marks notification as read.

        Logical reason:
        Users should know which notifications are new.
        """
        self.__is_read = True
