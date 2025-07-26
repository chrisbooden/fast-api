
from Enemy import *
from Zombie import *
from Ogre import *


def battle(e: Enemy):
    """
    Example of polymorphism
    As children of enemy can be passed in
    """
    e.talk()
    e.attack()

enemy = Enemy("zombie")

print(f"{enemy.type_of_enemy} has {enemy.health_points} health point and attack damage {enemy.attack_damage}")

enemy.talk()
enemy.walk_forward()
enemy.attack()
enemy.show_damage()
enemy.beep()


z = Zombie()
z.walk_forward()
z.talk()
z.spread_disease()

o = Ogre()
o.talk()
o.show_damage()

battle(o)
battle(z)
