from ursina import *
from core.entities import LivingEntity, DestructibleEntity
from model_builder import build_horse_model, build_cannon_model

class Horse(LivingEntity):
    def __init__(self, position=(0,0,0), team=0):
        super().__init__(speed=15, health=50, position=position, team=team, collider='box', scale=(1,1,1))
        self.visuals = Entity(parent=self)
        build_horse_model(self.visuals)
        
        self.rider = None
        
    def mount(self, player):
        if self.rider: return
        self.rider = player
        player.parent = self
        player.position = (0, 1.5, 0) # Sit on top
        player.speed = 0 # Disable player movement
        
    def dismount(self):
        if not self.rider: return
        self.rider.parent = scene
        self.rider.position = self.position + Vec3(2, 0, 0)
        self.rider.speed = self.rider.default_speed if hasattr(self.rider, 'default_speed') else 5
        self.rider = None

    def input(self, key):
        if self.rider and key == 'space':
            self.animate_y(2, duration=0.2, curve=curve.out_sine)
            self.animate_y(0, duration=0.2, delay=0.2, curve=curve.in_sine)

class Cannon(DestructibleEntity):
    def __init__(self, position=(0,0,0), rotation=(0,0,0), team=0):
        super().__init__(health=200, position=position, rotation=rotation, team=team, collider='box', scale=1.5)
        self.visuals = Entity(parent=self)
        build_cannon_model(self.visuals)
        
        self.cooldown = 0
        self.ammo = 1
        
    def interact(self):
        if self.cooldown <= 0:
            self.fire()
            
    def fire(self):
        print("CANNON FIRE!")
        self.cooldown = 5
        # Visuals
        self.animate_position(self.position + self.back * 0.5, duration=0.1) # Recoil
        self.animate_position(self.position, duration=1.0, delay=0.1)
        
        # Projectile
        ball = Entity(model='sphere', color=color.black, scale=0.2, position=self.position + self.forward*2 + self.up*1, collider='sphere')
        ball.animate_position(ball.position + self.forward * 50 + self.down * 5, duration=2, curve=curve.linear)
        destroy(ball, delay=2)
        
        # Explosion logic (simple sphere cast at end)
        invoke(self.explode, ball.position + self.forward * 50, delay=2)
        
    def explode(self, pos):
        # Create explosion effect
        e = Entity(model='sphere', color=color.orange, scale=4, position=pos)
        e.animate_scale(0, duration=0.5)
        destroy(e, delay=0.5)
        
        # Damage
        hit_info = boxcast(pos, thickness=(5,5), distance=1)
        if hit_info.hit:
             if hasattr(hit_info.entity, 'take_damage'):
                hit_info.entity.take_damage(500) # Instakill
    
    def update(self):
        if self.cooldown > 0:
            self.cooldown -= time.dt
