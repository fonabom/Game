from ursina import *
from model_builder import build_musket_model, build_pistol_model, build_sword_model, build_flag_model, build_rifle_model

class Weapon(Entity):
    def __init__(self, owner, **kwargs):
        # Default settings if not provided in kwargs
        if 'parent' not in kwargs: kwargs['parent'] = camera
        if 'scale' not in kwargs: kwargs['scale'] = (1, 1, 1)
        if 'position' not in kwargs: kwargs['position'] = (0.5, -0.5, 1) # Down and right, forward
        if 'rotation' not in kwargs: kwargs['rotation'] = (0, 0, 0)
        
        super().__init__(**kwargs)
        self.owner = owner
        self.cooldown = 0
        
    def attack(self): pass
    def reload(self): pass
    def create_tps_model(self, parent): 
        # Default behavior: generic block or None
        return None

class Musket(Weapon):
    # ... (existing init) ...
    def create_tps_model(self, parent):
        tps = Entity(parent=parent)
        build_musket_model(tps)
        tps.scale = 1 # Already roughly correct size
        tps.position = (0, 0, 0)
        tps.rotation = (0, 90, 90) # Adjust to fit hand
        return tps
    def __init__(self, owner):
        super().__init__(owner, model=None, color=color.clear, rotation=(0, 0, 0)) 
        
        self.visuals = Entity(parent=self)
        build_musket_model(self.visuals)
        self.visuals.position = (0.2, -0.2, 0.5)
        self.visuals.rotation = (0, -5, 0)
        
        self.damage = 100
        self.melee_damage = 50
        self.reload_time = 5
        self.is_reloading = False
        self.ammo = 1
        
        self.bayonet_mode = False

    def attack(self):
        if self.bayonet_mode:
            self.stab()
        elif self.ammo > 0 and not self.is_reloading:
            self.fire()
        elif self.ammo <= 0:
            print("Click!")
            
    def input(self, key):
        if key == 'x' or key == 'middle mouse down': 
            self.bayonet_mode = not self.bayonet_mode
            if self.bayonet_mode:
                self.visuals.animate_position((0.5, -0.4, 0.8), duration=0.2) # Melee stance
                print("Bayonet Ready")
            else:
                self.visuals.animate_position((0.2, -0.2, 0.5), duration=0.2) # Shooting stance
                print("Shooting Ready")

    def fire(self):
        print("Bang!")
        self.ammo -= 1
        self.animate_recoil()
        
        hit_info = raycast(camera.world_position, camera.forward, distance=1000)
        if hit_info.hit:
            if hasattr(hit_info.entity, 'take_damage'):
                hit_info.entity.take_damage(self.damage)
        
    def stab(self):
        print("Stab!")
        self.visuals.animate_position(self.visuals.position + Vec3(0, 0, 0.5), duration=0.1)
        self.visuals.animate_position(self.visuals.position, duration=0.2, delay=0.1)
        
        hit_info = raycast(camera.world_position, camera.forward, distance=2.5)
        if hit_info.hit:
             if hasattr(hit_info.entity, 'take_damage'):
                hit_info.entity.take_damage(self.melee_damage)

    def animate_recoil(self):
        self.visuals.animate_rotation((-10, -5, 0), duration=0.1)
        self.visuals.animate_rotation((0, -5, 0), duration=0.2, delay=0.1)
        
    def reload(self):
        if not self.is_reloading and self.ammo == 0 and not self.bayonet_mode:
            self.is_reloading = True
            invoke(self.finish_reload, delay=self.reload_time)
            self.animate_reload()
            
    def animate_reload(self):
        self.visuals.animate_rotation((60, -20, 0), duration=0.5)
        self.visuals.animate_rotation((0, -5, 0), duration=0.5, delay=self.reload_time-0.5)
            
    def finish_reload(self):
        self.is_reloading = False
        self.ammo = 1

class Rifle(Weapon):
    def create_tps_model(self, parent):
        tps = Entity(parent=parent)
        build_rifle_model(tps)
        tps.rotation = (0, 90, 90)
        return tps
    def __init__(self, owner):
        super().__init__(owner, model=None, color=color.clear, rotation=(0, 0, 0))
        self.visuals = Entity(parent=self)
        build_rifle_model(self.visuals)
        self.visuals.position = (0.2, -0.2, 0.5)
        self.visuals.rotation = (0, -5, 0)
        
        self.damage = 100
        self.reload_time = 7 
        self.is_reloading = False
        self.ammo = 1

    def attack(self):
        if self.ammo > 0 and not self.is_reloading:
            self.fire()
            
    def fire(self):
        print("Rifle Bang!")
        self.ammo -= 1
        self.animate_recoil()
        
    def animate_recoil(self):
        self.visuals.animate_position((0.2, -0.2, 0.3), duration=0.05)
        self.visuals.animate_rotation((-10, -5, 0), duration=0.05)
        self.visuals.animate_position((0.2, -0.2, 0.5), duration=0.3, delay=0.05)
        self.visuals.animate_rotation((0, -5, 0), duration=0.3, delay=0.05)
        
    def reload(self):
        if not self.is_reloading and self.ammo == 0:
            self.is_reloading = True
            invoke(self.finish_reload, delay=self.reload_time)
            self.animate_reload()
    
    def animate_reload(self):
        self.visuals.animate_rotation((80, -30, 0), duration=0.5)
        self.visuals.animate_rotation((0, -5, 0), duration=0.5, delay=self.reload_time-0.5)
        
    def finish_reload(self):
        self.is_reloading = False
        self.ammo = 1

class Pistol(Weapon): # ... 
    def create_tps_model(self, parent):
        tps = Entity(parent=parent)
        build_pistol_model(tps)
        tps.rotation = (0, 90, 90)
        return tps
    def __init__(self, owner):
        super().__init__(owner, model=None, color=color.clear, rotation=(0, 0, 0)) 
        self.visuals = Entity(parent=self)
        build_pistol_model(self.visuals)
        self.visuals.position = (0.2, -0.2, 0.5)
        self.visuals.rotation = (0, -5, 0)
        
        self.damage = 50
        self.reload_time = 3
        self.is_reloading = False
        self.ammo = 1

    def attack(self):
        if self.ammo > 0 and not self.is_reloading: self.fire()
            
    def fire(self):
        self.ammo -= 1
        self.animate_recoil()
        
    def animate_recoil(self):
        self.visuals.animate_rotation((-30, -5, 0), duration=0.05) 
        self.visuals.animate_rotation((0, -5, 0), duration=0.2, delay=0.05)
        
    def reload(self):
        if not self.is_reloading and self.ammo == 0:
            self.is_reloading = True
            invoke(self.finish_reload, delay=self.reload_time)
            self.visuals.animate_rotation((45, -10, 0), duration=0.3)
            self.visuals.animate_rotation((0, -5, 0), duration=0.3, delay=self.reload_time-0.3)

    def finish_reload(self):
        self.is_reloading = False
        self.ammo = 1

class Bayonet(Weapon): # Standalone bayonet
    def __init__(self, owner):
        super().__init__(owner, model='cube', scale=(0.1, 0.1, 0.8), color=color.light_gray, position=(0.5,-0.4))
    def attack(self):
        self.animate_position(self.position + Vec3(0, 0, 0.5), duration=0.1)
        self.animate_position(self.position, duration=0.2, delay=0.1)

class Sword(Weapon):
    def create_tps_model(self, parent):
        tps = Entity(parent=parent)
        build_sword_model(tps)
        tps.rotation = (0, 0, 0)
        tps.position = (0, -0.2, 0)
        return tps
    def __init__(self, owner):
        super().__init__(owner, model=None, color=color.clear, position=(0.5,-0.6, 0.8)) 
        self.visuals = Entity(parent=self)
        build_sword_model(self.visuals)
        self.visuals.rotation = (-20, -10, -10) 
        
    def attack(self):
        self.visuals.animate_rotation((60, 20, 0), duration=0.15) 
        self.visuals.animate_rotation((-20, -10, -10), duration=0.3, delay=0.15) 
        # Better Hitbox: Boxcast
        hit_info = boxcast(camera.world_position, thickness=(2,2), distance=2)
        if hit_info.hit:
             if hasattr(hit_info.entity, 'take_damage'):
                hit_info.entity.take_damage(35)

class Flag(Weapon):
    def create_tps_model(self, parent):
        tps = Entity(parent=parent)
        build_flag_model(tps)
        tps.rotation = (0, 0, 0)
        return tps
    def __init__(self, owner):
        super().__init__(owner, model=None, color=color.clear, position=(0.5, -0.5, 0.5))
        self.visuals = Entity(parent=self)
        build_flag_model(self.visuals, color.red)
        self.visuals.rotation = (0, 0, 0)
        
    def attack(self):
        self.visuals.animate_rotation((10, 0, 10), duration=0.5, loop=True) # Wave
        # Flag Damage!
        hit_info = boxcast(camera.world_position, thickness=(2,2), distance=2)
        if hit_info.hit:
             if hasattr(hit_info.entity, 'take_damage'):
                hit_info.entity.take_damage(20) # Weak but can kill

    def reload(self): pass

class Lance(Weapon):
    def __init__(self, owner):
        super().__init__(owner, model=None, color=color.clear, rotation=(0, 0, 0)) 
        self.visuals = Entity(parent=self)
        from model_builder import build_lance_model
        build_lance_model(self.visuals)
        self.visuals.position = (0.2, -0.5, 1.5)
        self.visuals.rotation = (0, 0, 0) # Pointing forward
        
    def attack(self):
        # Thrust
        self.visuals.animate_position(self.visuals.position + Vec3(0, 0, 1.0), duration=0.1)
        self.visuals.animate_position(self.visuals.position, duration=0.3, delay=0.1)
        hit_info = raycast(camera.world_position, camera.forward, distance=4)
        if hit_info.hit and hasattr(hit_info.entity, 'take_damage'):
             hit_info.entity.take_damage(100) # One shot
             
    def create_tps_model(self, parent):
        tps = Entity(parent=parent)
        from model_builder import build_lance_model
        build_lance_model(tps)
        tps.rotation = (0, 0, 90) 
        return tps

class Ramrod(Weapon):
    def __init__(self, owner):
        super().__init__(owner, model=None, color=color.clear, rotation=(0, 0, 0))
        self.visuals = Entity(parent=self)
        from model_builder import build_ramrod_model
        build_ramrod_model(self.visuals)
        self.visuals.position = (0.3, -0.4, 0.5)
        
    def attack(self):
        self.visuals.animate_rotation((30, 0, 0), duration=0.2)
        self.visuals.animate_rotation((0, 0, 0), duration=0.2, delay=0.2)
        # Low damage
        hit_info = boxcast(camera.world_position, thickness=(2,2), distance=2)
        if hit_info.hit and hasattr(hit_info.entity, 'take_damage'):
            hit_info.entity.take_damage(10)
            
    def create_tps_model(self, parent):
        tps = Entity(parent=parent)
        from model_builder import build_ramrod_model
        build_ramrod_model(tps)
        return tps
