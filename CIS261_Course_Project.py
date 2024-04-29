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

def display_employee_info(name, hours, rate, gross, tax_rate, tax, net):
    print(f"Employee: {name}\nHours: {hours}\nRate: ${rate:.2f}\nGross: ${gross:.2f}\nTax Rate: {tax_rate*100:.1f}%\nTax: ${tax:.2f}\nNet: ${net:.2f}")

def display_summary(count, total_hours, total_gross, total_tax, total_net):
    print(f"Summary:\nCount: {count}\nHours: {total_hours}\nGross: ${total_gross:.2f}\nTax: ${total_tax:.2f}\nNet: ${total_net:.2f}")

def main():
    count, sum_hours, sum_gross, sum_tax, sum_net = 0, 0, 0, 0, 0

    while input("Type 'End' to exit or press Enter to continue: ").lower() != 'end':
        name = input_employee_name()
        hours = input_total_hours()
        rate = input_hourly_rate()
        tax_rate = input_tax_rate()

        gross, tax, net = calculate_pay(hours, rate, tax_rate)
        display_employee_info(name, hours, rate, gross, tax_rate, tax, net)

        count += 1
        sum_hours += hours
        sum_gross += gross
        sum_tax += tax
        sum_net += net

    if count > 0:
        display_summary(count, sum_hours, sum_gross, sum_tax, sum_net)

if __name__ == "__main__":
    main()
