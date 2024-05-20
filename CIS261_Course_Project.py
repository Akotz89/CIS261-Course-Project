from datetime import datetime

def input_date_range():
    from_date = input("Enter from date (mm/dd/yyyy): ")
    to_date = input("Enter to date (mm/dd/yyyy): ")
    return from_date, to_date

def input_employee_name():
    return input("Enter employee's name: ")

def input_total_hours():
    return float(input("Enter total hours worked: "))

def input_hourly_rate():
    return float(input("Enter hourly rate: "))

def input_tax_rate():
    return float(input("Enter income tax rate (as a percentage): ")) / 100

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

def main():
    file_name = 'employee_data.txt'
    employee_data = []

    while input("Type 'End' to exit or press Enter to continue: ").lower() != 'end':
        from_date, to_date = input_date_range()
        name = input_employee_name()
        hours = input_total_hours()
        rate = input_hourly_rate()
        tax_rate = input_tax_rate()

        employee_data.append((from_date, to_date, name, hours, rate, tax_rate))
        append_employee_data_to_file(file_name, (from_date, to_date, name, hours, rate, tax_rate))

    if employee_data:
        report_from_date = get_report_from_date()
        stored_employee_data = read_employee_data_from_file(file_name, report_from_date)
        totals = process_employee_data(stored_employee_data)
        display_summary(totals)

if __name__ == "__main__":
    main()

