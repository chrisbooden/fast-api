"""
Encapsulate properties and functionality into a single object

Primitive data type:
- str, int, float etc

OOP
1. Encapsulation    (bundle related attributes/methods together)
2. Abstraction      (functionality is hidden/abstracted away so they do not need to know the details of how something works. We just exposure the method for them to use)
3. Inheritance      (parent, child classes)
4. Polymorphism     ()

"""

class Dog():
    """
    A class about a dog
    """
    def __init__(self, legs, ears, tail, age):
        self.legs = legs
        self.ears = ears
        self.tail = tail
        self.age = age


my_dog = Dog(4, 2, True, 10)

print(my_dog.age)


