from Enemy import *


class Ogre(Enemy):
    def __init__(self):
        super().__init__("Ogre")

    @staticmethod
    def talk():
        print("Slams hands on the ground")

    