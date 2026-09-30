from ursina import *

# BaseEntity: The root of all interactive game objects (Players, Vehicles, Props)
class BaseEntity(Entity):
    def __init__(self, team=0, health=100, max_health=100, **kwargs):
        super().__init__(**kwargs)
        self.team = team
        self.health = health
        self.max_health = max_health
        self.is_dead = False
        
        # Shader hook (will apply shadow shader later)
        # self.shader = lit_with_shadows_shader 

    def take_damage(self, amount, source=None):
        if self.is_dead: return
        
        # Team check (Friendly Fire)
        if source and hasattr(source, 'team') and source.team == self.team and source.team != 0:
            return # No friendly fire
            
        self.health -= amount
        print(f"{self.name} took {amount} damage from {source.name if source else 'Unknown'}. HP: {self.health}")
        
        # Visual feedback (flash red)
        self.blink(color.red, duration=0.1)

        if self.health <= 0:
            self.die(source)

    def die(self, killer=None):
        self.is_dead = True
        print(f"{self.name} died.")
        if killer and hasattr(killer, 'on_kill'):
            killer.on_kill(self)
        
        self.disable()
        # Optional: Spawn ragdoll or explosion
        destroy(self, delay=2) # Cleanup

    def on_kill(self, victim):
        # Override this in Player/AI
        pass

# LivingEntity: Things that move and act
class LivingEntity(BaseEntity):
    def __init__(self, speed=5, **kwargs):
        super().__init__(**kwargs)
        self.speed = speed
        self.velocity = Vec3(0,0,0)

# DestructibleEntity: Static props that break
class DestructibleEntity(BaseEntity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.collider = 'box'
