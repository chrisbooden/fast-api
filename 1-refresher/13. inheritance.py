

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

class Student(Person):
    def __init__(self, name, age, degree):
        super().__init__(name, age)
        self.degree = degree


p = Person("Charlie", 36)
s = Student("Charlie", 36, "Dance")

print(f"name: {s.name}, age: {s.age}, degree: {s.degree}")

