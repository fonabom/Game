from ursina import *

class Horse(Entity):
    def __init__(self, position=(0,0,0), **kwargs):
        super().__init__(
            model='cube', # Placeholder
            color=color.brown,
            scale=(1, 2, 3),
            position=position,
            collider='box',
            **kwargs
        )
        
        # Visuals
        self.head = Entity(parent=self, model='cube', color=color.brown, scale=(0.5, 0.5, 0.8), position=(0, 0.8, 1))
        
        self.rider = None
        self.speed = 15 # Fast
        
    def input(self, key):
        if self.hovered and key == 'e':
            if not self.rider:
                # Need to find player instance. For now assume scene.player exists
                # In robust engine, we'd pass player or use a manager
                 for e in scene.entities:
                    if hasattr(e, 'current_class'): # Duck typing for Player
                         if distance(e, self) < 5:
                             self.mount(e)
                             break
                             
        if self.rider and key == 'e':
            self.dismount()
            
    def update(self):
        if self.rider:
            # Movement logic attached to rider inputs? 
            # Or we hijack controls.
            
            move_vector = Vec3(0,0,0)
            if held_keys['w']: move_vector += self.forward
            if held_keys['s']: move_vector -= self.forward
            if held_keys['a']: self.rotation_y -= 100 * time.dt
            if held_keys['d']: self.rotation_y += 100 * time.dt
            
            # Simple movement
            
            # Ground check
            ray = raycast(self.position+Vec3(0,1,0), Vec3(0,-1,0), ignore=(self,))
            if ray.hit and ray.distance < 1.1:
                self.y = ray.world_point.y
                self.position += move_vector * self.speed * time.dt
            else:
                 self.y -= 9.8 * time.dt # Gravity
                 
            # Sync rider pos
            self.rider.position = self.position + Vec3(0, 1.5, 0)
            self.rider.rotation = self.rotation

    def mount(self, player):
        print("Mounting Horse")
        self.rider = player
        player.enabled = False # Disable player physics/controller
        # We need to manually handle camera or keep player enabled but attached
        # Simplest: Disable player controller, parent camera to horse
        
        # If player is FirstPersonController, disabling it stops input handling
        player.ignore_input = True
        player.visible = True 
        # But we want player to look around?
        # Let's just parent the player to the horse?
        
    def dismount(self):
        print("Dismounting Horse")
        if self.rider:
            self.rider.ignore_input = False
            self.rider.position = self.position + Vec3(2, 0, 0)
            self.rider = None
