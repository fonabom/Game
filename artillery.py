from ursina import *

class Cannon(Entity):
    def __init__(self, position=(0,0,0), **kwargs):
        super().__init__(
            model='cube',
            color=color.black,
            scale=(1.5, 1, 3),
            position=position,
            collider='box',
            **kwargs
        )
        
        # Parts
        self.barrel = Entity(parent=self, model='cylinder', color=color.dark_gray, scale=(0.4, 2.5, 0.4), rotation=(90, 0, 0), position=(0, 0.5, 0.5))
        self.wheel_l = Entity(parent=self, model='cylinder', color=color.brown, scale=(1, 0.2, 1), rotation=(0, 0, 90), position=(-0.8, 0, 0))
        self.wheel_r = Entity(parent=self, model='cylinder', color=color.brown, scale=(1, 0.2, 1), rotation=(0, 0, 90), position=(0.8, 0, 0))
        
        self.operator = None
        self.cooldown = 0
        
    def input(self, key):
        if self.hovered and key == 'e':
            if not self.operator:
                self.mount(scene.player) # Assuming single player local for now
                
        if self.operator and key == 'e':
            self.dismount()
            
        if self.operator:
            if held_keys['a']: self.rotation_y -= 1
            if held_keys['d']: self.rotation_y += 1
            if held_keys['w']: self.barrel.rotation_x -= 0.5
            if held_keys['s']: self.barrel.rotation_x += 0.5
            
            if key == 'left mouse down':
                self.fire()
                
    def mount(self, player):
        print("Mounting Cannon")
        self.operator = player
        player.enabled = False # Hide player or attach to cannon
        player.position = self.position + Vec3(0, 2, -2) # Just behind
        camera.parent = self
        camera.position = (0, 3, -4)
        camera.rotation = (10, 0, 0)
        
    def dismount(self):
        print("Dismounting Cannon")
        p = self.operator
        p.enabled = True
        p.position = self.position + Vec3(-2, 0, 0)
        camera.parent = p
        camera.position = (0, 2, 0) # Reset cam
        camera.rotation = (0, 0, 0)
        self.operator = None
        
    def fire(self):
        if self.cooldown <= 0:
            print("BOOM!")
            self.cooldown = 3
            invoke(self.reset_cooldown, delay=3)
            
            # Projectile
            ball = Entity(model='sphere', color=color.black, scale=0.3, position=self.barrel.world_position + self.barrel.forward * 2, collider='sphere')
            ball.velocity = self.barrel.forward * 50 + Vec3(0, 10, 0) # Upward arc
            ball.gravity = Vec3(0, -20, 0)
            
            # Simple physics loop for ball
            def update_ball():
                ball.position += ball.velocity * time.dt
                ball.velocity += ball.gravity * time.dt
                if ball.y < 0:
                    print("Splash")
                    destroy(ball)
                # Hit check...
                
            ball.update = update_ball
            destroy(ball, delay=5)
            
    def reset_cooldown(self):
        self.cooldown = 0
