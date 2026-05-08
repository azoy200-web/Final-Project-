"""
FacilityCatalog.py

This module contains the FacilityCatalog class.

We separated the catalog because the system needs one clear place to store, find, and
manage all facilities. This helped us debug facility selection and maintenance changes,
especially when admins needed to close a specific slot on a specific date.
"""

"""
This file stores the FacilityCatalog class.

Why this file is separate:
FacilityCatalog manages the collection of facility objects. This represents aggregation
because the catalog stores many facilities but the facility objects still have their own identity.
"""

class FacilityCatalog:
    """
    FacilityCatalog stores all facility objects.

    Purpose:
    - Adds, removes, finds, and displays facilities.

    Logical reason:
    BookingSystem needs one organized place to manage facility data.
    """
    def __init__(self):
        """
        Constructor purpose:
        - Creates a new object and prepares its starting data.

        Logical reason:
        Each object must begin with valid attributes before the system can use it.
        """
        self.__facilities = {}

    def get_facilities(self):
        """
        Purpose:
        - Returns all facilities.

        Logical reason:
        Booking and admin screens need the catalog data.
        """
        return self.__facilities

    def set_facilities(self, facilities):
        """
        Purpose:
        - Replaces facility dictionary.

        Logical reason:
        Pickle loading may restore a saved catalog.
        """
        self.__facilities = facilities

    def add_facility(self, facility):
        """
        Purpose:
        - Adds a facility to the catalog.

        Logical reason:
        The system needs a central place to store facilities.
        """
        self.__facilities[facility.get_facility_id()] = facility

    def remove_facility(self, facility_id):
        """
        Purpose:
        - Removes a facility from the catalog.

        Logical reason:
        Admin may remove unavailable or old facilities.
        """
        if facility_id in self.__facilities:
            del self.__facilities[facility_id]

    def get_facility(self, facility_id):
        """
        Purpose:
        - Finds a facility by ID.

        Logical reason:
        Booking uses facility ID selected from GUI.
        """
        return self.__facilities.get(facility_id)

    def display_all_facilities(self):
        """
        Purpose:
        - Returns all facilities for display.

        Logical reason:
        Admin dashboard needs to show facility data.
        """
        return self.__facilities
