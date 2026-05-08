"""
GUI-ONLY PART - Smart Campus Facility Booking System

What this file contains:
- CalendarPopup class: helps users/admins select dates from a small calendar window.
- SmartCampusGUI class: builds the Tkinter screens and connects buttons to backend functions.
- Main launcher: opens the Tkinter application safely.

Important note:
This is only the GUI section. It depends on the backend classes already being available:
BookingSystem, UserRole, UserStatus, AccessType, UsageType, and BookingStatus.
So either place this GUI code after the backend code, or import those backend classes from your backend file.

Why this separation is useful:
Separating the GUI makes the project easier to explain because the backend handles the rules/data,
while this GUI file only focuses on user interaction, screen navigation, buttons, entries, and messages.
"""

# Tkinter is used because the project requires a simple desktop interface for users and admins.
import tkinter as tk
from tkinter import ttk, messagebox

# calendar helps draw a real monthly calendar instead of forcing users to type dates manually.
import calendar

# date is used to start the calendar from today's month/year and to format selected dates correctly.
from datetime import date

# Backend dependency note:
# If this GUI is saved in a separate file, uncomment and adjust this import to match your backend filename.
# from backend_code import BookingSystem, UserRole, UserStatus, AccessType, UsageType, BookingStatus

class CalendarPopup:
    """
    CalendarPopup creates a small calendar selection window.

    Purpose:
    - Lets users select dates instead of typing them manually.
    - Refreshes related data after date selection when needed.

    Logical reason:
    Date format errors can break bookings, so a calendar improves usability and reduces mistakes.
    """
    def __init__(self, parent, target_entry, refresh_function=None):
        """
        Constructor purpose:
        - Creates a new object and prepares its starting data.

        Logical reason:
        Each object must begin with valid attributes before the system can use it.
        """
        self.__target_entry = target_entry
        self.__refresh_function = refresh_function
        self.__today = date.today()
        self.__year = self.__today.year
        self.__month = self.__today.month
        self.__window = tk.Toplevel(parent)
        self.__window.title("Select Date")
        self.__window.geometry("330x300")
        self.draw_calendar()

    def draw_calendar(self):
        """
        Purpose:
        - Draws calendar buttons for the selected month.

        Logical reason:
        Users can choose dates visually instead of typing.
        """
        for widget in self.__window.winfo_children():
            widget.destroy()

        header = tk.Frame(self.__window)
        header.pack(pady=10)

        tk.Button(header, text="<", command=self.previous_month).grid(row=0, column=0, padx=5)
        tk.Label(
            header,
            text=f"{calendar.month_name[self.__month]} {self.__year}",
            font=("Arial", 12, "bold")
        ).grid(row=0, column=1, padx=20)
        tk.Button(header, text=">", command=self.next_month).grid(row=0, column=2, padx=5)

        days_frame = tk.Frame(self.__window)
        days_frame.pack()

        for index, day_name in enumerate(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]):
            tk.Label(days_frame, text=day_name, width=5, font=("Arial", 9, "bold")).grid(row=0, column=index)

        month_days = calendar.monthcalendar(self.__year, self.__month)

        for row_number, week in enumerate(month_days, start=1):
            for column_number, day_number in enumerate(week):
                if day_number == 0:
                    tk.Label(days_frame, text="", width=5).grid(row=row_number, column=column_number)
                else:
                    tk.Button(
                        days_frame,
                        text=str(day_number),
                        width=5,
                        command=lambda selected_day=day_number: self.select_date(selected_day)
                    ).grid(row=row_number, column=column_number, padx=1, pady=1)

    def previous_month(self):
        """
        Purpose:
        - Moves calendar to previous month.

        Logical reason:
        Users may need to select dates in another month.
        """
        self.__month -= 1
        if self.__month == 0:
            self.__month = 12
            self.__year -= 1
        self.draw_calendar()

    def next_month(self):
        """
        Purpose:
        - Moves calendar to next month.

        Logical reason:
        Users may need to select future dates.
        """
        self.__month += 1
        if self.__month == 13:
            self.__month = 1
            self.__year += 1
        self.draw_calendar()

    def select_date(self, day_number):
        """
        Purpose:
        - Inserts selected date into the target entry.

        Logical reason:
        This connects the calendar popup to booking/admin date fields.
        """
        selected_date = date(self.__year, self.__month, day_number)
        self.__target_entry.delete(0, tk.END)
        self.__target_entry.insert(0, selected_date.strftime("%Y-%m-%d"))

        if self.__refresh_function:
            self.__refresh_function()

        self.__window.destroy()


class SmartCampusGUI:
    """
    SmartCampusGUI controls the Tkinter user interface.

    Purpose:
    - Shows login, registration, dashboard, booking, payment, user booking, and admin screens.
    - Connects button actions to BookingSystem backend logic.

    Logical reason:
    The GUI gives users and admins an easier way to interact with the system instead of using console commands.
    """
    def __init__(self, root):
        """
        Constructor purpose:
        - Creates a new object and prepares its starting data.

        Logical reason:
        Each object must begin with valid attributes before the system can use it.
        """
        self.__root = root
        self.__root.title("Smart Campus Facility Booking System")
        self.__root.geometry("1080x780")
        self.__system = BookingSystem()  # Connects the GUI to the backend controller, so every button can use real system logic.

        if self.__system.get_current_user() is not None:
            self.show_main_dashboard()
        else:
            self.show_login_screen()

    def clear_window(self):
        """
        Purpose:
        - Removes all widgets from the current GUI screen.

        Logical reason:
        Tkinter screens are rebuilt by clearing old widgets first.
        """
        for widget in self.__root.winfo_children():
            widget.destroy()

    def show_login_screen(self):
        """
        Purpose:
        - Displays login form.

        Logical reason:
        Users must log in before using the system.
        """
        self.clear_window()  # Clears the old screen first, because Tkinter does not automatically replace previous widgets.

        tk.Label(self.__root, text="Smart Campus Facility Booking System", font=("Arial", 22, "bold")).pack(pady=18)
        tk.Label(
            self.__root,
            text="Login Hint: Student 20240001 = STU20240001 | Staff 8899 = STF8899 | Admin 1000 = ADM1000",
            fg="gray"
        ).pack(pady=5)

        frame = tk.Frame(self.__root)
        frame.pack(pady=12)

        tk.Label(frame, text="User ID").grid(row=0, column=0, padx=5, pady=5)
        user_id_entry = tk.Entry(frame, width=35)
        user_id_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Password").grid(row=1, column=0, padx=5, pady=5)
        password_entry = tk.Entry(frame, width=35, show="*")
        password_entry.grid(row=1, column=1, padx=5, pady=5)

        remember_var = tk.BooleanVar()  # Stores whether the user wants the system to remember their login session.
        tk.Checkbutton(self.__root, text="Remember me", variable=remember_var).pack()

        def login_action():
            try:
                user = self.__system.validate_login(user_id_entry.get(), password_entry.get(), remember_var.get())
                messagebox.showinfo("Login Successful", f"Welcome {user.get_name()}")
                self.show_main_dashboard()
            except (ValueError, PermissionError) as error:
                messagebox.showerror("Login Error", str(error))

        tk.Button(self.__root, text="Login", width=25, command=login_action).pack(pady=5)
        tk.Button(self.__root, text="Create Account", width=25, command=self.show_register_screen).pack(pady=5)

    def show_register_screen(self):
        """
        Purpose:
        - Displays account creation form.

        Logical reason:
        New users need a way to register before login.
        """
        self.clear_window()  # Clears the old screen first, because Tkinter does not automatically replace previous widgets.

        tk.Label(self.__root, text="Create Account", font=("Arial", 18, "bold")).pack(pady=20)

        frame = tk.Frame(self.__root)
        frame.pack(pady=10)

        role_var = tk.StringVar(value="STUDENT")  # Starts with STUDENT as the default role to make registration faster for normal users.
        fields = {}  # Keeps all input boxes together, so registration data can be collected cleanly later.

        tk.Label(frame, text="Role").grid(row=0, column=0, padx=5, pady=5)
        ttk.Combobox(
            frame,
            textvariable=role_var,
            values=["STUDENT", "STAFF", "ADMIN"],
            state="readonly",
            width=32
        ).grid(row=0, column=1, padx=5, pady=5)

        for index, label in enumerate(["University/Work ID", "Name", "Email", "Password"], start=1):
            tk.Label(frame, text=label).grid(row=index, column=0, padx=5, pady=5)
            entry = tk.Entry(frame, width=35, show="*" if label == "Password" else "")
            entry.grid(row=index, column=1, padx=5, pady=5)
            fields[label] = entry

        def register_action():
            try:
                role = UserRole[role_var.get()]
                user = self.__system.register_user(
                    role,
                    fields["University/Work ID"].get(),
                    fields["Name"].get(),
                    fields["Email"].get(),
                    fields["Password"].get()
                )
                messagebox.showinfo("Account Created", f"Account created successfully.\nYour login User ID is:\n{user.get_user_id()}")
                self.show_login_screen()
            except (ValueError, TypeError) as error:
                messagebox.showerror("Registration Error", str(error))

        tk.Button(self.__root, text="Register", width=25, command=register_action).pack(pady=5)
        tk.Button(self.__root, text="Back", width=25, command=self.show_login_screen).pack(pady=5)

    def show_main_dashboard(self):
        """
        Purpose:
        - Displays the correct dashboard after login.

        Logical reason:
        Students/staff and admins need different buttons and information.
        """
        user = self.__system.get_current_user()
        self.clear_window()  # Clears the old screen first, because Tkinter does not automatically replace previous widgets.

        tk.Label(self.__root, text=f"Welcome, {user.get_name()}", font=("Arial", 18, "bold")).pack(pady=10)

        status_color = "red" if user.get_status() == UserStatus.FROZEN else "black"
        tk.Label(
            self.__root,
            text=f"Role: {user.get_role().value} | Access: {user.get_access_type().value} | Status: {user.get_status().value}",
            font=("Arial", 12, "bold"),
            fg=status_color
        ).pack()

        if user.get_status() == UserStatus.FROZEN:
            tk.Label(
                self.__root,
                text="Your account is frozen. You cannot make new bookings until admin restores your account.",
                fg="red",
                font=("Arial", 11, "bold")
            ).pack(pady=5)

        if user.get_role() != UserRole.ADMIN:
            tk.Label(
                self.__root,
                text=f"Credits Today: {self.__system.get_daily_credit_text(user)}",
                font=("Arial", 11, "bold"),
                fg="blue"
            ).pack(pady=5)

        if self.__system.get_announcements():
            tk.Label(self.__root, text="Announcements", font=("Arial", 13, "bold")).pack(pady=5)
            latest_announcements = "\n".join(self.__system.get_announcements()[-3:])
            tk.Label(self.__root, text=latest_announcements, justify="left", fg="purple").pack()

        frame = tk.Frame(self.__root)
        frame.pack(pady=20)

        if user.get_role() != UserRole.ADMIN:
            tk.Button(frame, text="Book Facility", width=32, command=self.show_booking_screen).grid(row=0, column=0, padx=8, pady=6)
            tk.Button(frame, text="View / Modify / Cancel Bookings", width=32, command=self.show_my_bookings).grid(row=0, column=1, padx=8, pady=6)
            tk.Button(frame, text="Update Profile", width=32, command=self.show_update_profile).grid(row=1, column=0, padx=8, pady=6)
            tk.Button(frame, text="Upgrade to Premium", width=32, command=self.show_upgrade_payment).grid(row=1, column=1, padx=8, pady=6)
            tk.Button(frame, text="Downgrade to Standard", width=32, command=self.downgrade_user).grid(row=2, column=0, padx=8, pady=6)

        if user.get_role() == UserRole.ADMIN:
            tk.Button(frame, text="Admin Dashboard", width=32, command=self.show_admin_dashboard).grid(row=0, column=0, padx=8, pady=6)

        tk.Button(frame, text="Logout", width=32, command=self.logout_action).grid(row=3, column=0, padx=8, pady=6)

    def logout_action(self):
        """
        Purpose:
        - Logs out current user and returns to login screen.

        Logical reason:
        Users need to end their session safely.
        """
        self.__system.logout()
        self.show_login_screen()

    def show_update_profile(self):
        """
        Purpose:
        - Lets users edit name and email.

        Logical reason:
        Profiles should be updateable through the GUI.
        """
        user = self.__system.get_current_user()
        self.clear_window()  # Clears the old screen first, because Tkinter does not automatically replace previous widgets.

        tk.Label(self.__root, text="Update Profile", font=("Arial", 18, "bold")).pack(pady=15)

        frame = tk.Frame(self.__root)
        frame.pack(pady=10)

        tk.Label(frame, text="Name").grid(row=0, column=0, padx=5, pady=5)
        name_entry = tk.Entry(frame, width=35)
        name_entry.insert(0, user.get_name())
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Email").grid(row=1, column=0, padx=5, pady=5)
        email_entry = tk.Entry(frame, width=35)
        email_entry.insert(0, user.get_email())
        email_entry.grid(row=1, column=1, padx=5, pady=5)

        def save_profile():
            try:
                user.update_profile(name_entry.get(), email_entry.get())
                self.__system.save_data_to_file("smart_campus_data.dat")
                messagebox.showinfo("Saved", "Profile updated.")
                self.show_main_dashboard()
            except ValueError as error:
                messagebox.showerror("Profile Error", str(error))

        tk.Button(self.__root, text="Save", width=25, command=save_profile).pack(pady=5)
        tk.Button(self.__root, text="Back", width=25, command=self.show_main_dashboard).pack(pady=5)

    def show_upgrade_payment(self):
        """
        Purpose:
        - Shows upgrade bill and payment confirmation window.

        Logical reason:
        Users should see the cost and benefits before upgrading.
        """
        user = self.__system.get_current_user()

        if user.get_access_type() == AccessType.PREMIUM:
            messagebox.showinfo("Already Premium", "You already have PREMIUM access.")
            return

        window = tk.Toplevel(self.__root)
        window.title("Upgrade Payment")
        window.geometry("460x320")

        bill = (
            "UPGRADE PAYMENT BILL\n"
            "-----------------------------\n"
            f"User: {user.get_name()}\n"
            f"Current Access: {user.get_access_type().value}\n"
            "New Access: PREMIUM\n"
            "Upgrade Fee: 30 AED\n\n"
            "Premium Benefits:\n"
            "- Book multiple facility types\n"
            "- 3 bookings per facility type per day\n"
            "- Priority access"
        )

        tk.Label(window, text=bill, justify="left", font=("Arial", 11)).pack(pady=15)

        def pay_upgrade():
            try:
                self.__system.process_upgrade_payment()
                messagebox.showinfo("Payment Successful", "Payment completed. Your access is now PREMIUM.")
                window.destroy()
                self.show_main_dashboard()
            except ValueError as error:
                messagebox.showerror("Upgrade Error", str(error))

        tk.Button(window, text="Pay 30 AED", width=20, command=pay_upgrade).pack(pady=10)

    def downgrade_user(self):
        """
        Purpose:
        - Downgrades logged-in user through GUI.

        Logical reason:
        Users need a simple dashboard action for downgrade.
        """
        self.__system.downgrade_current_user()
        messagebox.showinfo("Updated", "Your access is now STANDARD.")
        self.show_main_dashboard()

    def show_booking_screen(self):
        """
        Purpose:
        - Shows facility booking form.

        Logical reason:
        Users need to select facility, date, slot, usage type, and payment.
        """
        self.clear_window()  # Clears the old screen first, because Tkinter does not automatically replace previous widgets.
        user = self.__system.get_current_user()

        if user.get_status() == UserStatus.FROZEN:
            messagebox.showerror("Account Frozen", "Your account is frozen. You cannot make a booking.")
            self.show_main_dashboard()
            return

        tk.Label(self.__root, text="Book Facility", font=("Arial", 18, "bold")).pack(pady=10)

        frame = tk.Frame(self.__root)
        frame.pack(pady=10)

        facility_var = tk.StringVar()  # Stores the selected facility text from the dropdown so the booking logic knows what the user chose.
        slot_var = tk.StringVar()  # Stores the selected time slot, which is needed before confirming or closing a booking.
        usage_var = tk.StringVar(value=UsageType.INTERNAL.value)  # Internal is the default because most campus bookings are expected to be internal use.

        allowed_facilities = self.__system.get_allowed_facilities(user)
        facility_display = []

        for facility_id, facility in allowed_facilities.items():
            facility_display.append(
                f"{facility_id} - {facility.get_facility_name()} | "
                f"Type: {facility.get_facility_type()} | "
                f"Capacity: {facility.get_capacity()} | "
                f"Price: {facility.get_price_per_hour()} AED"
            )

        tk.Label(frame, text="Facility").grid(row=0, column=0, padx=5, pady=5)
        facility_box = ttk.Combobox(frame, textvariable=facility_var, values=facility_display, state="readonly", width=85)
        facility_box.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Date").grid(row=1, column=0, padx=5, pady=5)
        date_entry = tk.Entry(frame, width=30)
        date_entry.insert(0, str(date.today()))
        date_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        tk.Label(frame, text="Time Slot").grid(row=2, column=0, padx=5, pady=5)
        slot_box = ttk.Combobox(frame, textvariable=slot_var, state="readonly", width=30)
        slot_box.grid(row=2, column=1, sticky="w", padx=5, pady=5)

        tk.Label(frame, text="Usage Type").grid(row=3, column=0, padx=5, pady=5)
        usage_box = ttk.Combobox(
            frame,
            textvariable=usage_var,
            values=[UsageType.INTERNAL.value, UsageType.EXTERNAL.value],
            state="disabled",
            width=30
        )
        usage_box.grid(row=3, column=1, sticky="w", padx=5, pady=5)

        credit_label = tk.Label(self.__root, text="", font=("Arial", 11, "bold"), fg="blue")
        credit_label.pack(pady=5)

        details_label = tk.Label(self.__root, text="", justify="left", font=("Arial", 11))
        details_label.pack(pady=10)

        def update_facility_details(event=None):
            credit_label.config(
                text=f"Credits for {date_entry.get()}: {self.__system.get_daily_credit_text(user, date_entry.get())}"
            )

            if not facility_var.get():
                return

            facility_id = facility_var.get().split(" - ")[0]
            facility = self.__system.get_facility_catalog().get_facility(facility_id)
            available_slots = facility.get_available_slots(date_entry.get())

            slot_box["values"] = available_slots

            if available_slots:
                slot_var.set(available_slots[0])
            else:
                slot_var.set("")

            if facility.get_facility_type() == "EVENT_HALL":
                usage_box.config(state="readonly")
            else:
                usage_var.set(UsageType.INTERNAL.value)
                usage_box.config(state="disabled")

            details_label.config(
                text=f"Facility Details\n"
                     f"Name: {facility.get_facility_name()}\n"
                     f"Type: {facility.get_facility_type()}\n"
                     f"Location: {facility.get_location()}\n"
                     f"Capacity: {facility.get_capacity()}\n"
                     f"Available Slots: {len(available_slots)}\n"
                     f"Available: {facility.get_is_available()}\n"
                     f"{facility.get_rules()}"
            )

        tk.Button(
            frame,
            text="Open Calendar",
            command=lambda: CalendarPopup(self.__root, date_entry, update_facility_details)
        ).grid(row=1, column=1, padx=250)

        facility_box.bind("<<ComboboxSelected>>", update_facility_details)
        usage_box.bind("<<ComboboxSelected>>", update_facility_details)
        update_facility_details()

        def show_payment_bill():
            try:
                if not facility_var.get():
                    raise ValueError("Please select a facility.")
                if not slot_var.get():
                    raise ValueError("Please select an available time slot.")

                facility_id = facility_var.get().split(" - ")[0]
                facility = self.__system.get_facility_catalog().get_facility(facility_id)
                cost = facility.calculate_cost(usage_var.get())

                bill_window = tk.Toplevel(self.__root)
                bill_window.title("Booking Bill")
                bill_window.geometry("540x480")

                bill_text = (
                    "BOOKING BILL\n"
                    "-----------------------------\n"
                    f"User: {user.get_name()}\n"
                    f"Facility: {facility.get_facility_name()}\n"
                    f"Location: {facility.get_location()}\n"
                    f"Capacity: {facility.get_capacity()}\n"
                    f"Date: {date_entry.get()}\n"
                    f"Time Slot: {slot_var.get()}\n"
                    f"Usage Type: {usage_var.get()}\n"
                    f"Total Cost: {cost} AED\n\n"
                    f"{facility.get_rules()}\n\n"
                    "Click confirm to finalize the booking."
                )

                tk.Label(bill_window, text=bill_text, justify="left", font=("Arial", 11)).pack(pady=10)

                def pay_and_confirm():
                    try:
                        booking, receipt = self.__system.create_booking_after_payment(
                            facility_id,
                            slot_var.get(),
                            date_entry.get(),
                            usage_var.get()
                        )
                        messagebox.showinfo("Receipt", receipt.generate_receipt())
                        bill_window.destroy()
                        self.show_main_dashboard()
                    except (ValueError, PermissionError) as error:
                        messagebox.showerror("Booking Error", str(error))

                button_text = "Pay and Confirm" if cost > 0 else "Confirm Free Booking"
                tk.Button(bill_window, text=button_text, width=25, command=pay_and_confirm).pack(pady=10)

            except (ValueError, PermissionError) as error:
                messagebox.showerror("Booking Error", str(error))

        tk.Button(self.__root, text="Continue to Payment / Confirmation", width=35, command=show_payment_bill).pack(pady=5)
        tk.Button(self.__root, text="Back", width=25, command=self.show_main_dashboard).pack(pady=5)

    def show_my_bookings(self):
        """
        Purpose:
        - Displays user bookings and allows modify/cancel.

        Logical reason:
        Users need to manage their own reservations.
        """
        self.clear_window()  # Clears the old screen first, because Tkinter does not automatically replace previous widgets.
        user = self.__system.get_current_user()

        tk.Label(self.__root, text="My Bookings", font=("Arial", 18, "bold")).pack(pady=10)

        text = tk.Text(self.__root, width=120, height=22)
        text.pack(pady=8)

        my_bookings = []
        for booking in self.__system.get_bookings().values():
            if booking.get_user().get_user_id() == user.get_user_id():
                my_bookings.append(booking)

        if not my_bookings:
            text.insert(tk.END, "No bookings found.")
        else:
            for booking in my_bookings:
                text.insert(tk.END, booking.generate_booking_summary() + "\n-----------------------------\n")

        action_frame = tk.Frame(self.__root)
        action_frame.pack(pady=5)

        tk.Label(action_frame, text="Booking ID").grid(row=0, column=0, padx=5)
        booking_entry = tk.Entry(action_frame, width=15)
        booking_entry.grid(row=0, column=1, padx=5)

        tk.Label(action_frame, text="New Slot").grid(row=0, column=2, padx=5)
        new_slot_entry = tk.Entry(action_frame, width=15)
        new_slot_entry.grid(row=0, column=3, padx=5)

        tk.Label(action_frame, text="New Date").grid(row=0, column=4, padx=5)
        new_date_entry = tk.Entry(action_frame, width=15)
        new_date_entry.insert(0, str(date.today()))
        new_date_entry.grid(row=0, column=5, padx=5)

        def cancel_action():
            try:
                self.__system.cancel_booking(booking_entry.get())
                messagebox.showinfo("Cancelled", "Booking cancelled. Penalty credit decreased.")
                self.show_my_bookings()
            except (ValueError, PermissionError) as error:
                messagebox.showerror("Cancel Error", str(error))

        def modify_action():
            try:
                self.__system.modify_booking(booking_entry.get(), new_slot_entry.get(), new_date_entry.get())
                messagebox.showinfo("Modified", "Booking modified.")
                self.show_my_bookings()
            except (ValueError, PermissionError) as error:
                messagebox.showerror("Modify Error", str(error))

        tk.Button(action_frame, text="Cancel", command=cancel_action).grid(row=0, column=6, padx=5)
        tk.Button(action_frame, text="Modify", command=modify_action).grid(row=0, column=7, padx=5)
        tk.Button(self.__root, text="Back", width=25, command=self.show_main_dashboard).pack(pady=8)

    def show_admin_dashboard(self):
        """
        Purpose:
        - Displays admin tabs for user, booking, facility, and announcement management.

        Logical reason:
        Admins need organized tools for monitoring and control.
        """
        self.clear_window()  # Clears the old screen first, because Tkinter does not automatically replace previous widgets.

        tk.Label(self.__root, text="Admin Dashboard", font=("Arial", 18, "bold")).pack(pady=8)

        notebook = ttk.Notebook(self.__root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        users_tab = tk.Frame(notebook)
        bookings_tab = tk.Frame(notebook)
        facilities_tab = tk.Frame(notebook)
        announcements_tab = tk.Frame(notebook)

        notebook.add(users_tab, text="Users Dashboard")
        notebook.add(bookings_tab, text="Bookings Calendar")
        notebook.add(facilities_tab, text="Facilities")
        notebook.add(announcements_tab, text="Announcements")

        self.build_users_tab(users_tab)
        self.build_bookings_tab(bookings_tab)
        self.build_facilities_tab(facilities_tab)
        self.build_announcements_tab(announcements_tab)

        tk.Button(self.__root, text="Back", width=25, command=self.show_main_dashboard).pack(pady=5)

    def build_users_tab(self, parent):
        """
        Purpose:
        - Builds admin user management tab.

        Logical reason:
        Admin must upgrade, downgrade, freeze, and unfreeze users.
        """
        text = tk.Text(parent, width=120, height=20)
        text.pack(pady=8)

        text.insert(tk.END, "USER DASHBOARD\n")
        text.insert(tk.END, "User ID | Name | Role | Access | Status | Booking Credit | Penalty Credit\n")
        text.insert(tk.END, "-" * 120 + "\n")

        for user_id, user in self.__system.get_users().items():
            text.insert(
                tk.END,
                f"{user_id} | {user.get_name()} | {user.get_role().value} | "
                f"{user.get_access_type().value} | {user.get_status().value} | "
                f"{self.__system.get_daily_credit_text(user)} | Penalty: {user.get_penalty_credits()} / 3\n"
            )

        frame = tk.Frame(parent)
        frame.pack(pady=5)

        tk.Label(frame, text="User ID").grid(row=0, column=0, padx=5)
        user_entry = tk.Entry(frame, width=20)
        user_entry.grid(row=0, column=1, padx=5)

        def do_action(action):
            try:
                user_id = user_entry.get()

                if action == "upgrade":
                    self.__system.upgrade_user_by_admin(user_id)
                elif action == "downgrade":
                    self.__system.downgrade_user_by_admin(user_id)
                elif action == "freeze":
                    self.__system.freeze_user(user_id)
                elif action == "unfreeze":
                    self.__system.unfreeze_user(user_id)

                messagebox.showinfo("Updated", "User updated.")
                self.show_admin_dashboard()

            except (ValueError, KeyError) as error:
                messagebox.showerror("Admin Error", str(error))

        tk.Button(frame, text="Upgrade", command=lambda: do_action("upgrade")).grid(row=0, column=2, padx=5)
        tk.Button(frame, text="Downgrade", command=lambda: do_action("downgrade")).grid(row=0, column=3, padx=5)
        tk.Button(frame, text="Freeze", command=lambda: do_action("freeze")).grid(row=0, column=4, padx=5)
        tk.Button(frame, text="Unfreeze / Reset Penalty", command=lambda: do_action("unfreeze")).grid(row=0, column=5, padx=5)

    def build_bookings_tab(self, parent):
        """
        Purpose:
        - Builds admin booking monitoring tab.

        Logical reason:
        Admin needs to review bookings and mark no-shows.
        """
        control = tk.Frame(parent)
        control.pack(pady=5)

        tk.Label(control, text="Date").grid(row=0, column=0, padx=5)

        date_entry = tk.Entry(control, width=15)
        date_entry.insert(0, str(date.today()))
        date_entry.grid(row=0, column=1, padx=5)

        output = tk.Text(parent, width=120, height=21)
        output.pack(pady=5)

        def refresh():
            output.delete("1.0", tk.END)
            selected_date = date_entry.get()

            output.insert(tk.END, f"BOOKINGS ON {selected_date}\n")
            output.insert(tk.END, "=" * 90 + "\n\n")

            bookings = self.__system.get_bookings_by_date(selected_date)

            if not bookings:
                output.insert(tk.END, "No bookings on this date.\n\n")
            else:
                for booking in bookings.values():
                    output.insert(
                        tk.END,
                        f"{booking.get_booking_id()} | "
                        f"{booking.get_user().get_name()} | "
                        f"{booking.get_facility().get_facility_name()} | "
                        f"{booking.get_slot()} | "
                        f"{booking.get_status().value} | "
                        f"{booking.get_total_cost()} AED\n"
                    )

            output.insert(tk.END, "\nFACILITY SLOT STATUS\n")
            output.insert(tk.END, "=" * 90 + "\n")

            for facility in self.__system.get_facility_catalog().get_facilities().values():
                output.insert(tk.END, f"\n{facility.get_facility_name()} - {facility.get_location()}\n")
                available_slots = facility.get_available_slots(selected_date)
                closed_slots = facility.get_closed_slots(selected_date)

                for slot in facility.get_time_slots():
                    if slot in closed_slots:
                        output.insert(tk.END, f"  {slot}: CLOSED BY ADMIN\n")
                    elif slot in available_slots:
                        output.insert(tk.END, f"  {slot}: Available\n")
                    else:
                        output.insert(tk.END, f"  {slot}: BOOKED\n")

        tk.Button(control, text="Open Calendar", command=lambda: CalendarPopup(self.__root, date_entry, refresh)).grid(row=0, column=2, padx=5)
        tk.Button(control, text="Refresh", command=refresh).grid(row=0, column=3, padx=5)

        action_frame = tk.Frame(parent)
        action_frame.pack(pady=5)

        tk.Label(action_frame, text="Booking ID").grid(row=0, column=0, padx=5)
        no_show_entry = tk.Entry(action_frame, width=15)
        no_show_entry.grid(row=0, column=1, padx=5)

        def mark_no_show_action():
            try:
                self.__system.mark_booking_no_show(no_show_entry.get())
                messagebox.showinfo("No-Show Recorded", "No-show recorded. Penalty credit decreased. User may be frozen automatically.")
                self.show_admin_dashboard()
            except ValueError as error:
                messagebox.showerror("No-Show Error", str(error))

        tk.Button(action_frame, text="Mark No-Show", command=mark_no_show_action).grid(row=0, column=2, padx=5)

        refresh()

    def build_facilities_tab(self, parent):
        """
        Purpose:
        - Builds admin facility management tab.

        Logical reason:
        Admin needs to open, close, and manage facility availability.
        """
        text = tk.Text(parent, width=120, height=16)
        text.pack(pady=8)

        for facility_id, facility in self.__system.get_facility_catalog().get_facilities().items():
            text.insert(
                tk.END,
                f"{facility_id} | {facility.get_facility_name()} | {facility.get_facility_type()} | "
                f"{facility.get_location()} | Capacity: {facility.get_capacity()} | "
                f"Price: {facility.get_price_per_hour()} AED | Available: {facility.get_is_available()}\n"
            )

        frame = tk.Frame(parent)
        frame.pack(pady=5)

        facility_var = tk.StringVar()  # Stores the selected facility text from the dropdown so the booking logic knows what the user chose.
        options = []

        for facility_id, facility in self.__system.get_facility_catalog().get_facilities().items():
            options.append(f"{facility_id} - {facility.get_facility_name()}")

        tk.Label(frame, text="Facility").grid(row=0, column=0, padx=5)

        ttk.Combobox(frame, textvariable=facility_var, values=options, state="readonly", width=40).grid(row=0, column=1, padx=5)

        def set_availability(flag):
            try:
                if not facility_var.get():
                    raise ValueError("Select a facility first.")

                facility_id = facility_var.get().split(" - ")[0]
                facility = self.__system.get_facility_catalog().get_facility(facility_id)
                facility.set_is_available(flag)
                self.__system.save_data_to_file("smart_campus_data.dat")

                messagebox.showinfo("Updated", "Facility availability updated.")
                self.show_admin_dashboard()

            except ValueError as error:
                messagebox.showerror("Facility Error", str(error))

        tk.Button(frame, text="Set Available", command=lambda: set_availability(True)).grid(row=0, column=2, padx=5)
        tk.Button(frame, text="Set Unavailable", command=lambda: set_availability(False)).grid(row=0, column=3, padx=5)

        closure_frame = tk.Frame(parent)
        closure_frame.pack(pady=10)

        tk.Label(closure_frame, text="Closure Date").grid(row=0, column=0, padx=5)

        closure_date_entry = tk.Entry(closure_frame, width=15)
        closure_date_entry.insert(0, str(date.today()))
        closure_date_entry.grid(row=0, column=1, padx=5)

        tk.Button(closure_frame, text="Open Calendar", command=lambda: CalendarPopup(self.__root, closure_date_entry)).grid(row=0, column=2, padx=5)

        tk.Label(closure_frame, text="Time Slot").grid(row=0, column=3, padx=5)

        slot_var = tk.StringVar()  # Stores the selected time slot, which is needed before confirming or closing a booking.
        slot_box = ttk.Combobox(
            closure_frame,
            textvariable=slot_var,
            values=[
                "09:00-10:00",
                "10:00-11:00",
                "11:00-12:00",
                "12:00-13:00",
                "14:00-15:00",
                "15:00-16:00"
            ],
            state="readonly",
            width=18
        )
        slot_box.grid(row=0, column=4, padx=5)

        def close_selected_slot():
            try:
                if not facility_var.get():
                    raise ValueError("Select a facility first.")
                if not slot_var.get():
                    raise ValueError("Select a time slot first.")

                facility_id = facility_var.get().split(" - ")[0]
                self.__system.close_facility_slot(facility_id, closure_date_entry.get(), slot_var.get())
                messagebox.showinfo("Closed", "The selected facility slot is now closed.")
                self.show_admin_dashboard()

            except ValueError as error:
                messagebox.showerror("Closure Error", str(error))

        def open_selected_slot():
            try:
                if not facility_var.get():
                    raise ValueError("Select a facility first.")
                if not slot_var.get():
                    raise ValueError("Select a time slot first.")

                facility_id = facility_var.get().split(" - ")[0]
                self.__system.open_facility_slot(facility_id, closure_date_entry.get(), slot_var.get())
                messagebox.showinfo("Opened", "The selected facility slot is now available again.")
                self.show_admin_dashboard()

            except ValueError as error:
                messagebox.showerror("Opening Error", str(error))

        tk.Button(closure_frame, text="Close Selected Slot", command=close_selected_slot).grid(row=0, column=5, padx=5)
        tk.Button(closure_frame, text="Open Selected Slot", command=open_selected_slot).grid(row=0, column=6, padx=5)

    def build_announcements_tab(self, parent):
        """
        Purpose:
        - Builds admin announcement tab.

        Logical reason:
        Admin needs to post maintenance or system messages.
        """
        text = tk.Text(parent, width=120, height=18)
        text.pack(pady=8)

        if not self.__system.get_announcements():
            text.insert(tk.END, "No announcements yet.")
        else:
            for announcement in self.__system.get_announcements():
                text.insert(tk.END, announcement + "\n")

        frame = tk.Frame(parent)
        frame.pack(pady=5)

        tk.Label(frame, text="New Announcement").grid(row=0, column=0, padx=5)
        announcement_entry = tk.Entry(frame, width=70)
        announcement_entry.grid(row=0, column=1, padx=5)

        def add_announcement():
            """
            Purpose:
            - Adds announcement with timestamp.

            Logical reason:
            Users need to see system updates and maintenance messages.
            """
            try:
                self.__system.add_announcement(announcement_entry.get())
                messagebox.showinfo("Added", "Announcement added.")
                self.show_admin_dashboard()
            except ValueError as error:
                messagebox.showerror("Announcement Error", str(error))

        tk.Button(frame, text="Add Announcement", command=add_announcement).grid(row=0, column=2, padx=5)


if __name__ == "__main__":
    try:
        root = tk.Tk()  # Creates the main Tkinter window that will contain all GUI screens.
        app = SmartCampusGUI(root)
        root.mainloop()  # Keeps the window open and listens for user actions such as clicks and typing.

    except tk.TclError:
        print("Tkinter GUI cannot open here. Run it locally in PyCharm.")

    except KeyboardInterrupt:
        print("Program closed by user.")
