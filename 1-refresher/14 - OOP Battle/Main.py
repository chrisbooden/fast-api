from Enemy import *
from Ogre import *
from Zombie import *
from Hero import *

def battle(e1: Enemy, e2: Enemy):
    e1.talk()
    e2.talk()

    while e1.health_points > 0 and e2.health_points > 0:
        print("----------------------")
        e1.special_attack()
        e2.special_attack()
        print(f"{e1.get_type_of_enemy()}: {e1.health_points} HP left")
        print(f"{e2.get_type_of_enemy()}: {e2.health_points} HP left")

        e2.attack()
        e1.health_points -= e2.attack_damage

        e1.attack()
        e2.health_points -= e1.attack_damage

    print("----------------------")
    if e1.health_points > 0:
        print(f"{e1.get_type_of_enemy()} wins")
    else:
        print(f"{e2.get_type_of_enemy()} wins")

zombie = Zombie(50, 1)
ogre = Ogre(20, 3)

battle(zombie, ogre)


def hero_battle(h: Hero, e: Enemy):

    while h.health_points > 0 and e.health_points > 0:
        print("----------------------")
        h.attack()
        e.special_attack()
        print(f"hero has {h.health_points} HP left")
        print(f"{e.get_type_of_enemy()}: {e.health_points} HP left")

        h.attack()
        e.health_points -= h.attack_damage

        e.attack()
        h.health_points -= e.attack_damage

    print("----------------------")
    if h.health_points > 0:
        print(f"Hero wins")
    else:
        print(f"{e.get_type_of_enemy()} wins")

hero = Hero(10, 1)
zom = Zombie(10, 1)
weapon = Weapon("Sword", 1)

hero.weapon = weapon
hero.equip_weapon()

hero_battle(hero, zom)