from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from core.entities import LivingEntity
from core.assets import get_model, get_texture
from model_builder import build_character_model
try:
    from game_classes import Classes
except ImportError:
    # Handle circular import or if game_classes isn't updated yet
    pass

class GamePlayer(LivingEntity):
    def __init__(self, position=(0,1,0), team=1, **kwargs):
        super().__init__(team=team, health=100, speed=5, position=position, **kwargs)
        
        # We need to wrap Ursina's controller logic or reimplement it
        # Ideally, we'd write a custom controller for "High Quality" movement (Momentum, etc.)
        # For now, we will add the FPC components to this entity manually or inherit FPC?
        # Multiple inheritance is tricky with Entity.
        # Let's encapsulate the FPC logic or use Ursina's Input handling directly.
        
        self.camera_pivot = Entity(parent=self, y=2)
        camera.parent = self.camera_pivot
        camera.position = (0,0,0)
        camera.rotation = (0,0,0)
        camera.fov = 90
        
        self.cursor = Entity(parent=camera.ui, model='quad', color=color.white, scale=.008, rotation_z=45)
        mouse.locked = True
        
        # Movement State
        self.is_grounded = False
        self.jump_height = 2 # Retained as it's used in update()
        self.gravity = 1 # Retained as it's used in update()
        # Stats
        self.kills = 0
        self.deaths = 0
        self.assists = 0
        self.score = 0
        
        # Appearance (Character Model)
        self.character_visuals = Entity(parent=self, position=(0, -1, 0), rotation=(0, 180, 0))
        # Important: this will be set by build_character
        self.weapon_mount = None 
        
        self.build_character(color.blue, "Infantry")
        self.character_visuals.visible = False 
        
        # Camera State
        self.is_third_person = False
        
        self.weapon_inventory = []
        self.current_weapon_index = 0
        self.current_weapon = None
        self.held_weapon_model = None # The visual model held in 3rd person
        
        # Default Class
        self.set_class(Classes.LineInfantry)

    def update(self):
        # Movement Physics (Custom Implementation for "High Quality" feel)
        # Rotation
        self.rotation_y += mouse.velocity[0] * 40
        self.camera_pivot.rotation_x -= mouse.velocity[1] * 40
        self.camera_pivot.rotation_x = clamp(self.camera_pivot.rotation_x, -90, 90)
        
        # Movement
        direction = Vec3(
            self.forward * (held_keys['w'] - held_keys['s'])
            + self.right * (held_keys['d'] - held_keys['a'])
        ).normalized()
        
        # Gravity
        ray = raycast(self.position + Vec3(0,0.1,0), self.down, distance=1.1, ignore=(self,))
        self.is_grounded = ray.hit
        
        if self.is_grounded:
            self.velocity = direction * self.speed * time.dt
            if held_keys['space']:
                self.y += 0.1 # Unstick
                self.velocity.y = self.jump_height * time.dt # Jump impusle
        else:
            self.velocity.y -= self.gravity * time.dt # Gravity
            self.velocity.x = direction.x * self.speed * time.dt * 0.5 # Air control reduced
            self.velocity.z = direction.z * self.speed * time.dt * 0.5
            
        self.position += self.velocity
        
    def build_character(self, uniform_color, class_type):
        for child in self.character_visuals.children: destroy(child)
        build_character_model(self.character_visuals, uniform_color, class_type)
        # Re-find the weapon mount that was created in build_character_model
        # It's attached to Right Arm -> Weapon Mount
        # But we don't have direct ref unless we crawl or return it.
        # model_builder sets 'parent.weapon_mount' to the entity, so self.character_visuals.weapon_mount should exist?
        if hasattr(self.character_visuals, 'weapon_mount'):
            self.weapon_mount = self.character_visuals.weapon_mount

    def set_class(self, game_class):
        self.current_class = game_class
        self.speed = game_class.speed
        self.health = game_class.health
        
        # Unique Uniforms
        c = color.blue
        c_type = "Infantry"
        
        if game_class.name == "Line Infantry": 
            c = color.blue
            c_type = "Line Infantry"
        elif game_class.name == "Officer": 
            c = color.hex('#1A237E')
            c_type = "Officer"
        elif game_class.name == "Standard Bearer": 
            c = color.hex('#0D47A1')
            c_type = "Infantry"
        elif game_class.name == "Skirmisher": 
            c = color.hex('#33691E')
            c_type = "Skirmisher"
        elif game_class.name == "Artillery": 
            c = color.hex('#3E2723')
            c_type = "Artillery"
        elif game_class.name == "Cavalry": 
            c = color.hex('#BF360C')
            c_type = "Cavalry"
        
        self.build_character(c, c_type)

        # Clear old weapons
        for w in self.weapon_inventory:
            destroy(w)
        self.weapon_inventory = []
        
        # Equip new weapons
        for weapon_factory in game_class.weapons:
            w = weapon_factory(self)
            w.enabled = False
            self.weapon_inventory.append(w)
            
        if self.weapon_inventory:
            self.equip_weapon(0)

    def equip_weapon(self, index):
        if 0 <= index < len(self.weapon_inventory):
            if self.current_weapon:
                self.current_weapon.enabled = False
                
            self.current_weapon = self.weapon_inventory[index]
            self.current_weapon.enabled = True
            self.current_weapon_index = index
            print(f"Equipped {self.current_weapon.__class__.__name__}")
            
            # Update 3rd Person Held Model
            if self.held_weapon_model: destroy(self.held_weapon_model)
            
            if self.weapon_mount and hasattr(self.current_weapon, 'create_tps_model'):
                self.held_weapon_model = self.current_weapon.create_tps_model(self.weapon_mount)
    
    def special_ability(self):
        c_name = self.current_class.name
        
        if c_name == "Officer":
            print("Officer: Form Line!")
            # Place Line Marker
            hit = raycast(camera.world_position, camera.forward, distance=15)
            if hit.hit:
                if hasattr(self, 'officer_line') and self.officer_line:
                    destroy(self.officer_line)
                
                # Create a long yellow line on the ground
                self.officer_line = Entity(
                    model='quad', 
                    scale=(10, 1), 
                    color=color.rgba(255, 215, 0, 150), 
                    position=hit.world_point + Vec3(0, 0.1, 0),
                    rotation=(90, self.rotation_y, 0), # Flat and aligned with Officer
                    texture='white_cube'
                )
                destroy(self.officer_line, delay=30) # Lasts 30 seconds
            
        elif c_name == "Skirmisher" or c_name == "Line Infantry":
             pass # No special ability yet
             
        elif "Musician" in c_name or "Drummer" in c_name or "Fifer" in c_name:
            print("Playing Music...")
            # Ideally play sound
            # Buff nearby
            kill = boxcast(self.position, thickness=(10,10), distance=10, ignore=[self])
            # Just a visual for now
            e = Entity(parent=self, model='circle', scale=5, color=color.rgba(0, 255, 0, 100), rotation=(90,0,0))
            destroy(e, delay=2)

        elif c_name == "Sapper":
            print("Building Sandbag...")
            # Spawn Sandbag
            from ursina import Entity, color
            pos = self.position + self.forward * 2 + Vec3(0, 0.5, 0)
            Entity(model='cube', scale=(2, 1, 0.5), color=color.hex('#D7CCC8'), position=pos, collider='box')

        elif c_name == "Medic" or c_name == "Surgeon":
            print("Healing...")
            hit = raycast(camera.world_position, camera.forward, distance=3)
            if hit.hit and hasattr(hit.entity, 'health'):
                hit.entity.health = min(hit.entity.health + 50, hit.entity.max_health)
                hit.entity.blink(color.green)

    def input(self, key):
        if key == 'q':
            self.special_ability()
            
        if key == 'f': # Interaction / Mounting
            from vehicle import Horse
            hit_info = boxcast(self.position, thickness=(2,2), distance=3, ignore=[self])
            if hit_info.hit:
                if isinstance(hit_info.entity.parent, Horse): # Hit visuals
                    hit_info.entity.parent.mount(self)
                elif isinstance(hit_info.entity, Horse):
                    hit_info.entity.mount(self)
        
        if key == 'v':
            self.is_third_person = not self.is_third_person
            if self.is_third_person:
                camera.position = (0, 2, -5)
                self.character_visuals.visible = True
                if self.current_weapon and hasattr(self.current_weapon, 'visuals'):
                    self.current_weapon.visuals.visible = False
            else:
                camera.position = (0, 0, 0)
                self.character_visuals.visible = False
                if self.current_weapon and hasattr(self.current_weapon, 'visuals'):
                    self.current_weapon.visuals.visible = True
        
        if key == 'left mouse down':
            if self.current_weapon:
                self.current_weapon.attack()
                # TPS Animation Hook
                if self.is_third_person and self.held_weapon_model:
                     # Simple recoil/attack animation for held model
                     self.held_weapon_model.animate_rotation((self.held_weapon_model.rotation_x - 30, self.held_weapon_model.rotation_y, self.held_weapon_model.rotation_z), duration=0.1)
                     self.held_weapon_model.animate_rotation((self.held_weapon_model.rotation_x, self.held_weapon_model.rotation_y, self.held_weapon_model.rotation_z), duration=0.2, delay=0.1)
                
        if key == 'r':
            if self.current_weapon:
                self.current_weapon.reload()
                if self.is_third_person and self.held_weapon_model:
                     self.held_weapon_model.animate_rotation((self.held_weapon_model.rotation_x + 60, self.held_weapon_model.rotation_y, self.held_weapon_model.rotation_z), duration=0.5)
                     self.held_weapon_model.animate_rotation((self.held_weapon_model.rotation_x, self.held_weapon_model.rotation_y, self.held_weapon_model.rotation_z), duration=0.5, delay=0.5)
        
        if key == 'scroll up':
            self.equip_weapon( (self.current_weapon_index + 1) % len(self.weapon_inventory) )
        if key == 'scroll down':
            self.equip_weapon( (self.current_weapon_index - 1) % len(self.weapon_inventory) )
            
        if key == '1' and len(self.weapon_inventory) > 0: self.equip_weapon(0)
        if key == '2' and len(self.weapon_inventory) > 1: self.equip_weapon(1)
        if key == '3' and len(self.weapon_inventory) > 2: self.equip_weapon(2)

# Representation of other players on the network
class RemotePlayer(Entity):
    def __init__(self, **kwargs):
        super().__init__(
            model='cube',
            color=color.red,
            collider='box',
            **kwargs
        )
