from Enemy import *
import random

class Zombie(Enemy):
    def __init__(self, health_points, attack_damage):
        super().__init__(
            type_of_enemy="Zombie",
            health_points=health_points,
            attack_damage=attack_damage
        )

    def special_attack(self):
        did_special_attack_work = random.random() < 0.5
        if did_special_attack_work:
            self.health_points += 2
            print("Zombie regenerated 2HP!")

    @staticmethod
    def talk():
        print("*Gumbling..*")

    @staticmethod
    def spread_disease():
        print("The zombie is trying to spread infection")