

def calculate_homework(homework_arg):
    sum_of_grades = 0
    for homework in homework_arg.values():
        sum_of_grades += homework

    final_grade = round(
        sum_of_grades/ len(homework_arg)
    , 2)

    print(final_grade)