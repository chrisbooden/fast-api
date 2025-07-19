"""
User Input
"""

first_name = input("Enter you first name: ")
days = int(input("How many days before your birthday: "))

print(f"Hi {first_name}\nOnly {days} before your birthday")

print(f"Hi {first_name}\nOnly {round(days/7,2)} before your birthday")