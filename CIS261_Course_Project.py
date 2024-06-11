from datetime import datetime
import hashlib

# User class to handle authentication and authorization
class User:
    def __init__(self, user_id, password, role):
        self.user_id = user_id
        self.password = password  # Store the hashed password directly
        self.role = role

    @staticmethod
    def authenticate(user_id, password, users):
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        for user in users:
            if user.user_id == user_id:
                if user.password == password_hash:
                    return user
                else:
                    print("Incorrect password. Please try again.")
                    return None
        print("User ID not found. Please try again.")
        return None

    @staticmethod
    def load_users(file_name):
        users = []
        try:
            with open(file_name, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    user_id, password_hash, role = line.strip().split("|")
                    users.append(User(user_id, password_hash, role))
        except FileNotFoundError:
            print(f"User file '{file_name}' not found. No users loaded.")
        return users

    @staticmethod
    def save_user(file_name, user):
        with open(file_name, 'a') as file:
            file.write(f"{user.user_id}|{user.password}|{user.role}\n")

def input_date_range():
    while True:
        from_date = input("Enter from date (mm/dd/yyyy): ")
        to_date = input("Enter to date (mm/dd/yyyy): ")
        try:
            datetime.strptime(from_date, "%m/%d/%Y")
            datetime.strptime(to_date, "%m/%d/%Y")
            return from_date, to_date
        except ValueError:
            print("Invalid date format. Please enter the date in mm/dd/yyyy format.")

def input_employee_name():
    return input("Enter employee's name: ")

def input_total_hours():
    while True:
        try:
            hours = float(input("Enter total hours worked: "))
            if hours >= 0:
                return hours
            else:
                print("Total hours cannot be negative.")
        except ValueError:
            print("Invalid input. Please enter a numeric value for total hours.")

def input_hourly_rate():
    while True:
        try:
            rate = float(input("Enter hourly rate: "))
            if rate >= 0:
                return rate
            else:
                print("Hourly rate cannot be negative.")
        except ValueError:
            print("Invalid input. Please enter a numeric value for hourly rate.")

def input_tax_rate():
    while True:
        try:
            tax_rate = float(input("Enter income tax rate (as a percentage): ")) / 100
            if 0 <= tax_rate <= 1:
                return tax_rate
            else:
                print("Tax rate must be between 0 and 100.")
        except ValueError:
            print("Invalid input. Please enter a numeric value for tax rate.")

def calculate_pay(hours, rate, tax_rate):
    gross = hours * rate
    tax = gross * tax_rate
    return gross, tax, gross - tax

def display_employee_info(from_date, to_date, name, hours, rate, gross, tax_rate, tax, net):
    print(f"\nFrom Date: {from_date}\nTo Date: {to_date}\nEmployee: {name}\nHours: {hours}\nRate: ${rate:.2f}\nGross: ${gross:.2f}\nTax Rate: {tax_rate*100:.1f}%\nTax: ${tax:.2f}\nNet: ${net:.2f}\n")

def display_summary(totals):
    print(f"Summary:\nCount: {totals['count']}\nHours: {totals['sum_hours']}\nGross: ${totals['sum_gross']:.2f}\nTax: ${totals['sum_tax']:.2f}\nNet: ${totals['sum_net']:.2f}")

def append_employee_data_to_file(file_name, employee_data):
    with open(file_name, 'a') as file:
        file.write("|".join(map(str, employee_data)) + "\n")

def process_employee_data(employee_data):
    totals = {
        'count': 0,
        'sum_hours': 0,
        'sum_gross': 0,
        'sum_tax': 0,
        'sum_net': 0
    }

    for data in employee_data:
        from_date, to_date, name, hours, rate, tax_rate = data
        gross, tax, net = calculate_pay(hours, rate, tax_rate)
        display_employee_info(from_date, to_date, name, hours, rate, gross, tax_rate, tax, net)
        
        totals['count'] += 1
        totals['sum_hours'] += hours
        totals['sum_gross'] += gross
        totals['sum_tax'] += tax
        totals['sum_net'] += net

    return totals

def read_employee_data_from_file(file_name, report_from_date):
    with open(file_name, 'r') as file:
        lines = file.readlines()

    employee_data = []
    for line in lines:
        data = line.strip().split("|")
        from_date, to_date = data[0], data[1]
        if report_from_date.lower() == "all" or from_date == report_from_date:
            employee_data.append((from_date, to_date, data[2], float(data[3]), float(data[4]), float(data[5])))

    return employee_data

def get_report_from_date():
    while True:
        report_from_date = input("Enter From Date for report (mm/dd/yyyy) or 'All' for all records: ")
        if report_from_date.lower() == "all":
            return report_from_date
        try:
            datetime.strptime(report_from_date, "%m/%d/%Y")
            return report_from_date
        except ValueError:
            print("Invalid date format. Please enter the date in mm/dd/yyyy format.")

def load_user_ids(file_name):
    user_ids = []
    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()
            for line in lines:
                user_id, _, _ = line.strip().split("|")
                user_ids.append(user_id)
    except FileNotFoundError:
        print(f"User file '{file_name}' not found. No users loaded.")
    return user_ids

def add_user(file_name):
    user_ids = load_user_ids(file_name)

    while True:
        user_id = input("Enter User ID: ")
        if user_id in user_ids:
            print("User ID already exists. Please enter a different User ID.")
            continue

        password = input("Enter Password: ")
        password_hash = hashlib.sha256(password.encode()).hexdigest()  # Hash the password before storing
        role = input("Enter Authorization (Admin/User): ")
        if role not in ["Admin", "User"]:
            print("Invalid authorization. Please enter 'Admin' or 'User'.")
            continue

        user = User(user_id, password_hash, role)
        User.save_user(file_name, user)
        user_ids.append(user_id)
        print(f"User {user_id} added successfully.")

        while True:
            next_step = input("Type 'M' to return to the main menu or 'A' to add another user: ").upper()
            if next_step == 'M':
                return
            elif next_step == 'A':
                break
            else:
                print("Invalid choice. Please type 'M' to return to the main menu or 'A' to add another user.")

def display_users(file_name):
    users = User.load_users(file_name)
    for user in users:
        print(f"User ID: {user.user_id}, Password: {'*' * 8}, Authorization: {user.role}")

def admin_actions(employee_file):
    while True:
        print("Admin Menu:")
        print("1. Enter Employee Data")
        print("2. View Employee Data")
        print("3. Return to Main Menu")
        choice = input("Select an option: ")
        if choice == '1':
            employee_data = []
            while input("Type 'End' to exit or press Enter to continue: ").lower() != 'end':
                from_date, to_date = input_date_range()
                name = input_employee_name()
                hours = input_total_hours()
                rate = input_hourly_rate()
                tax_rate = input_tax_rate()
                employee_data.append((from_date, to_date, name, hours, rate, tax_rate))
                append_employee_data_to_file(employee_file, (from_date, to_date, name, hours, rate, tax_rate))
            if employee_data:
                report_from_date = get_report_from_date()
                stored_employee_data = read_employee_data_from_file(employee_file, report_from_date)
                totals = process_employee_data(stored_employee_data)
                display_summary(totals)
        elif choice == '2':
            report_from_date = get_report_from_date()
            stored_employee_data = read_employee_data_from_file(employee_file, report_from_date)
            totals = process_employee_data(stored_employee_data)
            display_summary(totals)
        elif choice == '3':
            return
        else:
            print("Invalid choice. Please select a valid option.")

def user_actions(employee_file):
    while True:
        print("User Menu:")
        print("1. View Employee Data")
        print("2. Return to Main Menu")
        choice = input("Select an option: ")
        if choice == '1':
            report_from_date = get_report_from_date()
            stored_employee_data = read_employee_data_from_file(employee_file, report_from_date)
            totals = process_employee_data(stored_employee_data)
            display_summary(totals)
        elif choice == '2':
            return
        else:
            print("Invalid choice. Please select a valid option.")

def dashboard_menu():
    print("Dashboard Menu:")
    print("1. Add User")
    print("2. Display Users")
    print("3. Login and Perform Actions")
    print("4. Exit")

def main_menu():
    user_file = 'users.txt'
    employee_file = 'employee_data.txt'
    
    while True:
        dashboard_menu()
        choice = input("Select an option: ")
        if choice == '1':
            add_user(user_file)
        elif choice == '2':
            display_users(user_file)
        elif choice == '3':
            users = User.load_users(user_file)
            user_id = input("Enter User ID: ")
            password = input("Enter Password: ")
            user = User.authenticate(user_id, password, users)

            if not user:
                print("Authentication failed. Returning to dashboard menu.")
                continue

            print(f"Welcome, {user_id}! Your role is {user.role}.")

            if user.role == 'Admin':
                admin_actions(employee_file)
            elif user.role == 'User':
                user_actions(employee_file)
            else:
                print("Invalid role. Returning to dashboard menu.")
        elif choice == '4':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main_menu()
