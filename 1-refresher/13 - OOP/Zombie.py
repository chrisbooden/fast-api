from Enemy import *

class Zombie(Enemy):
    def __init__(self):
        super().__init__(type_of_enemy="Zombie")

    @staticmethod
    def talk():
        print("Eughhhgggg")

    @staticmethod
    def spread_disease():
        print("Spread disease")