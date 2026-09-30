from ursina import *
from vehicle import Horse, Cannon

def create_plains():
    # Standard Green Map
    ground = Entity(model='plane', scale=(100, 1, 100), color=color.hex('#4CAF50'), texture='grass', texture_scale=(100,100), collider='box')
    # Walls
    Entity(model='cube', scale=(100, 5, 1), position=(0, 2.5, 50), color=color.rgba(0,0,0,0.1), collider='box')
    Entity(model='cube', scale=(100, 5, 1), position=(0, 2.5, -50), color=color.rgba(0,0,0,0.1), collider='box')
    Entity(model='cube', scale=(1, 5, 100), position=(50, 2.5, 0), color=color.rgba(0,0,0,0.1), collider='box')
    Entity(model='cube', scale=(1, 5, 100), position=(-50, 2.5, 0), color=color.rgba(0,0,0,0.1), collider='box')
    
    # Trees
    for i in range(20):
        Entity(model='cube', color=color.hex('#3E2723'), scale=(0.5, 4, 0.5), position=(random.randint(-40,40), 2, random.randint(-40,40)), collider='box')

    # Safety Floor
    Entity(model='cube', scale=(500, 1, 500), position=(0, -10, 0), visible=False, collider='box')
    
    # Spawns
    Horse(position=(5, 1, -5))
    Cannon(position=(10, 1, 10))

def create_desert():
    # Sand Map
    ground = Entity(model='plane', scale=(100, 1, 100), color=color.hex('#F4A460'), texture='white_cube', texture_scale=(50,50), collider='box')
    
    # Cactus / Rocks
    for i in range(15):
        Entity(model='cube', color=color.hex('#2E8B57'), scale=(0.4, 3, 0.4), position=(random.randint(-40,40), 1.5, random.randint(-40,40)), collider='box')
        
    # Safety Floor
    Entity(model='cube', scale=(500, 1, 500), position=(0, -10, 0), visible=False, collider='box')
    
    # Spawns
    Horse(position=(0, 1, 10))
    Cannon(position=(10, 1, -10))
    
def create_forest():
    # Dark Ground
    ground = Entity(model='plane', scale=(100, 1, 100), color=color.hex('#1B5E20'), texture='grass', texture_scale=(100,100), collider='box')
    scene.fog_color = color.hex('#263238')
    scene.fog_density = 0.05
    
    # Dense Trees
    for i in range(60):
        Entity(model='cube', color=color.hex('#3E2723'), scale=(0.8, 6, 0.8), position=(random.randint(-45,45), 3, random.randint(-45,45)), collider='box')
        
    # Safety Floor
    Entity(model='cube', scale=(500, 1, 500), position=(0, -10, 0), visible=False, collider='box')
    
    # Spawns
    Horse(position=(5, 1, 5))
    Cannon(position=(-5, 1, -5))

def create_map(map_name="Plains"):
    # Clear existing map props if needed (complex in Ursina without grouping, but simple scene.clear() might wipe UI)
    # Simple strategy: Just spawn. In full game, would destroy old world entity.
    
    if map_name == "Desert":
        create_desert()
    elif map_name == "Forest":
        create_forest()
    else:
        create_plains()
