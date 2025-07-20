
from Enemy import *

enemy = Enemy("zombie")

print(f"{enemy.type_of_enemy} has {enemy.health_points} health point and attack damage {enemy.attack_damage}")

enemy.talk()
enemy.walk_forward()
enemy.attack()
enemy.show_damage()
enemy.beep()

