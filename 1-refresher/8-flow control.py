"""
Flow control
"""

x = 3

if (x == 1):
    print("x is 1")
elif (x == 2):
    print("x is 2")
else:
    print("x is not 1 or 2")

match x:
    case 1:
        print("x is 1")
    case 2:
        print("x is 2")
    case _:
        print("x is not 1 or 2")


# Test
grade = 62
result = ""
if (grade >= 90):
    result = "A"
elif (80 <= grade < 90):
    result = "B"
elif (70 <= grade < 80):
    result = "C"
elif (60 <= grade < 70):
    result = "D"
else :
    result = "F"

print(f"Your grade = {result}")


