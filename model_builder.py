from ursina import *

def try_load_external(parent, name):
    # check if model exists by trying to load it
    m = load_model(name)
    if m:
        parent.model = m
        # Try finding texture
        t = load_texture(name)
        if t: parent.texture = t
        parent.color = color.white
        return True
    return False

def build_horse_model(parent):
    if try_load_external(parent, 'horse'): return parent
    # Body
    Entity(parent=parent, model='cube', color=color.hex('#5D4037'), scale=(0.5, 0.5, 1.2), position=(0, 0.5, 0))
    # Neck/Head
    Entity(parent=parent, model='cube', color=color.hex('#5D4037'), scale=(0.25, 0.6, 0.4), position=(0, 1.0, 0.6), rotation=(-45, 0, 0))
    Entity(parent=parent, model='cube', color=color.hex('#5D4037'), scale=(0.25, 0.25, 0.5), position=(0, 1.3, 0.7), rotation=(10, 0, 0))
    # Legs (Already cubes)
    Entity(parent=parent, model='cube', color=color.hex('#3E2723'), scale=(0.15, 0.6, 0.15), position=(-0.2, 0.2, 0.5))
    Entity(parent=parent, model='cube', color=color.hex('#3E2723'), scale=(0.15, 0.6, 0.15), position=(0.2, 0.2, 0.5))
    Entity(parent=parent, model='cube', color=color.hex('#3E2723'), scale=(0.15, 0.6, 0.15), position=(-0.2, 0.2, -0.5))
    Entity(parent=parent, model='cube', color=color.hex('#3E2723'), scale=(0.15, 0.6, 0.15), position=(0.2, 0.2, -0.5))
    # Tail
    Entity(parent=parent, model='cube', color=color.black, scale=(0.1, 0.4, 0.1), position=(0, 0.6, -0.6), rotation=(20, 0, 0))
    return parent

def build_cannon_model(parent):
    if try_load_external(parent, 'cannon'): return parent
    # Carriage
    Entity(parent=parent, model='cube', color=color.hex('#5D4037'), scale=(0.8, 0.2, 1.5), position=(0, 0.3, 0))
    # Wheels (Approximated with crossed cubes)
    def make_wheel(x):
        w = Entity(parent=parent, position=(x, 0.3, 0), rotation=(0, 0, 90))
        Entity(parent=w, model='cube', color=color.hex('#3E2723'), scale=(0.8, 0.1, 0.1))
        Entity(parent=w, model='cube', color=color.hex('#3E2723'), scale=(0.1, 0.8, 0.1))
        # Rim logic is hard with cubes, just simplified block wheels
        Entity(parent=w, model='cube', color=color.hex('#3E2723'), scale=(0.6, 0.6, 0.05))
        
    make_wheel(-0.5)
    make_wheel(0.5)

    # Barrel (Long Cube)
    Entity(parent=parent, model='cube', color=color.hex('#1C1C1C'), scale=(0.25, 1.8, 0.25), position=(0, 0.6, 0.2), rotation=(80, 0, 0))
    return parent

def build_lance_model(parent):
    if try_load_external(parent, 'lance'): return parent
    # Pole
    Entity(parent=parent, model='cube', color=color.hex('#5D4037'), scale=(0.03, 2.5, 0.03), position=(0, 0, 0.5), rotation=(90, 0, 0))
    # Tip (Sharp Cube)
    Entity(parent=parent, model='cube', color=color.hex('#CFD8DC'), scale=(0.02, 0.3, 0.02), position=(0, 0, 1.8), rotation=(90, 0, 0))
    # Pennant
    Entity(parent=parent, model='cube', color=color.red, scale=(0.01, 0.2, 0.4), position=(0, 0.05, 1.5))
    return parent

def build_ramrod_model(parent):
    if try_load_external(parent, 'ramrod'): return parent
    # Stick
    Entity(parent=parent, model='cube', color=color.hex('#D7CCC8'), scale=(0.04, 1.5, 0.04), position=(0, 0, 0.5), rotation=(90, 0, 0))
    # Sponge
    Entity(parent=parent, model='cube', color=color.white, scale=(0.08, 0.2, 0.08), position=(0, 0, 1.2), rotation=(90, 0, 0))
    return parent

def build_musket_model(parent):
    if try_load_external(parent, 'musket'): return parent
    # Main Stock
    Entity(parent=parent, model='cube', color=color.hex('#5D4037'), scale=(0.05, 0.1, 1.2), position=(0, 0, 0))
    # Buttstock
    Entity(parent=parent, model='cube', color=color.hex('#5D4037'), scale=(0.05, 0.12, 0.6), position=(0, -0.08, -0.8), rotation=(10, 0, 0))
    
    # Barrel (Hexagonal approximation -> Cube)
    Entity(parent=parent, model='cube', color=color.hex('#1f2122'), scale=(0.03, 1.4, 0.03), position=(0, 0.06, 0.6), rotation=(90, 0, 0))
    
    # Bands
    Entity(parent=parent, model='cube', color=color.hex('#B0BEC5'), scale=(0.055, 0.11, 0.05), position=(0, 0.03, 0.4))
    Entity(parent=parent, model='cube', color=color.hex('#B0BEC5'), scale=(0.052, 0.1, 0.05), position=(0, 0.03, 0.9))
    
    # Trigger Guard
    Entity(parent=parent, model='cube', color=color.gold, scale=(0.02, 0.1, 0.15), position=(0, -0.15, -0.2))

    # Bayonet (Spike)
    Entity(parent=parent, model='cube', color=color.hex('#B0BEC5'), scale=(0.015, 0.8, 0.015), position=(0, 0.06, 1.4), rotation=(90, 0, 0))

    return parent

def build_character_model(parent, uniform_color=color.blue, class_type="Infantry"):
    if try_load_external(parent, class_type.lower().replace(" ", "_")) or try_load_external(parent, 'character'): return parent
    # Head (Cube)
    Entity(parent=parent, model='cube', color=color.hex('#F5F5DC'), scale=0.4, position=(0, 1.6, 0)) 
    
    # Hats based on Class
    if class_type == "Infantry" or class_type == "Line Infantry":
        # Shako
        Entity(parent=parent, model='cube', color=color.black, scale=(0.4, 0.6, 0.4), position=(0, 2.0, 0))
        Entity(parent=parent, model='cube', color=color.gold, scale=(0.1, 0.2, 0.05), position=(0, 2.2, 0.23))
        Entity(parent=parent, model='cube', color=color.white, scale=(0.02, 0.3, 0.02), position=(0, 2.4, 0))
        
    elif class_type == "Officer":
        # Bicorne
        Entity(parent=parent, model='cube', color=color.black, scale=(0.8, 0.3, 0.3), position=(0, 1.9, 0))
        Entity(parent=parent, model='cube', color=color.gold, scale=(0.1, 0.1, 0.01), position=(0, 1.9, 0.16))
        
    elif class_type == "Skirmisher":
        # Green Stovepipe
        Entity(parent=parent, model='cube', color=color.hex('#1B5E20'), scale=(0.35, 0.5, 0.35), position=(0, 1.95, 0))
        Entity(parent=parent, model='cube', color=color.white, scale=(0.05, 0.05, 0.05), position=(0.2, 2.0, 0))

    elif class_type == "Cavalry":
        # Helmet
        Entity(parent=parent, model='cube', color=color.gold, scale=0.45, position=(0, 1.9, 0))
        Entity(parent=parent, model='cube', color=color.black, scale=(0.05, 0.4, 0.5), position=(0, 2.2, -0.1)) # Crest
        
    elif class_type == "Artillery":
        # Simple Cap
        Entity(parent=parent, model='cube', color=color.hex('#3E2723'), scale=(0.4, 0.3, 0.4), position=(0, 1.85, 0))

    # Torso
    Entity(parent=parent, model='cube', color=uniform_color, scale=(0.6, 1.0, 0.3), position=(0, 1.0, 0))
    # Crossbelts
    Entity(parent=parent, model='cube', color=color.white, scale=(0.65, 1.0, 0.35), position=(0, 1.0, 0))
    
    # Arms
    left_arm = Entity(parent=parent, model='cube', color=uniform_color, scale=(0.2, 0.9, 0.2), position=(-0.4, 1.0, 0))
    right_arm = Entity(parent=parent, model='cube', color=uniform_color, scale=(0.2, 0.9, 0.2), position=(0.4, 1.0, 0))
    
    # Weapon Mount
    weapon_mount = Entity(parent=right_arm, position=(0, -0.4, 0.2), rotation=(90, 0, 0))
    parent.weapon_mount = weapon_mount 
    
    # Legs
    Entity(parent=parent, model='cube', color=color.white, scale=(0.25, 1.0, 0.25), position=(-0.15, 0.0, 0))
    Entity(parent=parent, model='cube', color=color.white, scale=(0.25, 1.0, 0.25), position=(0.15, 0.0, 0))
    
    return parent

def build_rifle_model(parent):
    if try_load_external(parent, 'rifle'): return parent
    Entity(parent=parent, model='cube', color=color.hex('#3e2723'), scale=(0.05, 0.09, 1.1), position=(0, 0, 0))
    Entity(parent=parent, model='cube', color=color.hex('#3e2723'), scale=(0.05, 0.11, 0.6), position=(0, -0.08, -0.8), rotation=(10, 0, 0))
    # Barrel
    Entity(parent=parent, model='cube', color=color.hex('#000000'), scale=(0.035, 1.3, 0.035), position=(0, 0.06, 0.6), rotation=(90, 0, 0))
    # Brass fittings
    Entity(parent=parent, model='cube', color=color.gold, scale=(0.055, 0.1, 0.05), position=(0, 0.03, 0.8))
    # Lock
    lock = Entity(parent=parent, position=(0.04, 0.05, -0.2))
    Entity(parent=lock, model='cube', color=color.gray, scale=(0.01, 0.08, 0.12)) 
    return parent

def build_pistol_model(parent):
    if try_load_external(parent, 'pistol'): return parent
    Entity(parent=parent, model='cube', color=color.hex('#5D4037'), scale=(0.05, 0.08, 0.6), position=(0, 0, 0))
    Entity(parent=parent, model='cube', color=color.hex('#5D4037'), scale=(0.05, 0.1, 0.25), position=(0, -0.12, -0.25), rotation=(45, 0, 0))
    # Barrel
    Entity(parent=parent, model='cube', color=color.hex('#CFD8DC'), scale=(0.02, 0.5, 0.02), position=(0, 0.06, 0.2), rotation=(90, 0, 0))
    # Lock
    lock = Entity(parent=parent, position=(0.04, 0.05, -0.1))
    Entity(parent=lock, model='cube', color=color.gray, scale=(0.01, 0.06, 0.08))
    return parent

def build_sword_model(parent):
    if try_load_external(parent, 'sword') or try_load_external(parent, 'saber'): return parent
    # Blade
    Entity(parent=parent, model='cube', color=color.hex('#E0E0E0'), scale=(0.01, 1.0, 0.03), position=(0, 0.6, 0))
    # Tip
    Entity(parent=parent, model='cube', color=color.hex('#E0E0E0'), scale=(0.01, 0.1, 0.02), position=(0.005, 1.1, 0), rotation=(0,0, -20))
    # Guard
    Entity(parent=parent, model='cube', color=color.gold, scale=(0.12, 0.02, 0.12), position=(0, 0.1, 0))
    Entity(parent=parent, model='cube', color=color.gold, scale=(0.02, 0.25, 0.08), position=(-0.05, 0.22, 0), rotation=(0,0, 20))
    # Handle
    Entity(parent=parent, model='cube', color=color.hex('#3E2723'), scale=(0.04, 0.2, 0.04), position=(0, 0, 0))
    return parent

def build_flag_model(parent, flag_color=color.red):
    if try_load_external(parent, 'flag'): return parent
    # Pole
    Entity(parent=parent, model='cube', color=color.hex('#3E2723'), scale=(0.04, 3.0, 0.04), position=(0, 0.5, 0))
    # Cloth
    cloth = Entity(parent=parent, model='cube', color=flag_color, scale=(0.02, 1.2, 1.5), position=(0, 1.5, 0.8))
    # Finial
    Entity(parent=parent, model='cube', color=color.gold, scale=0.1, position=(0, 2.0, 0))
    return parent
