from ursina import *
from weapons import Musket, Bayonet, Pistol, Sword, Flag

class GameClass:
    def __init__(self, name, health, speed, weapons):
        self.name = name
        self.health = health
        self.speed = speed
        self.weapons = weapons 

from weapons import Musket, Bayonet, Pistol, Sword, Flag, Rifle, Lance, Ramrod

# Factory for weapons
def create_musket(owner): return Musket(owner)
def create_bayonet(owner): return Bayonet(owner)
def create_flag(owner): return Flag(owner)
def create_pistol(owner): return Pistol(owner)
def create_sword(owner): return Sword(owner)
def create_rifle(owner): return Rifle(owner)
def create_lance(owner): return Lance(owner)
def create_ramrod(owner): return Ramrod(owner)

class Classes:
    LineInfantry = GameClass("Line Infantry", 100, 8, [create_musket, create_bayonet])
    Officer = GameClass("Officer", 120, 9, [create_pistol, create_sword])
    StandardBearer = GameClass("Standard Bearer", 100, 8, [create_flag, create_pistol])
    # New Classes
    Skirmisher = GameClass("Skirmisher", 80, 10, [create_rifle, create_sword])
    Artillery = GameClass("Artillery", 100, 8, [create_ramrod, create_pistol])
    Cavalry = GameClass("Cavalry", 100, 9, [create_lance, create_sword])

