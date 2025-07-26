

class Enemy:
    # Class attributes
    health_points: int = 10
    attack_damage: int = 1

    # Instance methods
    def __init__(self, type_of_enemy):
        self.type_of_enemy: str = type_of_enemy

    def talk(self):
        print(f"I am a {self.type_of_enemy}. Be prepared to fight!")

    def walk_forward(self):
        print(f"{self.type_of_enemy} walks forward")

    def attack(self):
        print(f"{self.type_of_enemy} attacks for {self.attack_damage} damage")

    @classmethod
    def show_damage(cls):
        print(f"I have {cls.attack_damage} damage")

    @staticmethod
    def beep():
        print("Beep beep!")






    
                 

