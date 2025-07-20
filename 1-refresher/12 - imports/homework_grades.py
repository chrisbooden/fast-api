"""
Modules help to create files with specific purposes
Helps with more structured code that is easier to maintain
"""

from grade_average_service import calculate_homework


homework_assignment_grades = {
    'homework_1': 85,
    'homework_2': 100,
    'homework_3': 81
}

calculate_homework(homework_assignment_grades)

