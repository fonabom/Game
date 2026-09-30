from ursina import *
from game_classes import Classes
from core.game_manager import game_manager # Access to state

class MainMenu(Entity):
    def __init__(self, on_host=None, on_join=None):
        super().__init__(parent=camera.ui)
        self.main_panel = Entity(parent=self, model='quad', scale=(0.8, 0.6), color=color.rgba(0,0,0,0.8))
        self.title = Text(parent=self.main_panel, text="Nations At War: Reforged", scale=3, origin=(0,0), position=(0, 0.4))
        
        # Map Selection
        self.maps = ["Plains", "Desert", "Forest"]
        self.current_map_index = 0
        self.map_btn = Button(parent=self.main_panel, text=f"Map: {self.maps[0]}", scale=(0.3, 0.08), position=(-0.2, 0.1))
        self.map_btn.on_click = self.cycle_map

        # Host
        self.host_btn = Button(parent=self.main_panel, text="Host Game", scale=(0.3, 0.1), position=(-0.2, -0.1))
        self.host_btn.on_click = self.host_game
        self.on_host_callback = on_host
        
        # Join
        self.join_input = InputField(parent=self.main_panel, default_value="Enter Code", scale=(0.3, 0.08), position=(0.2, 0.1))
        self.join_btn = Button(parent=self.main_panel, text="Join Game", scale=(0.3, 0.1), position=(0.2, -0.1))
        self.join_btn.on_click = self.join_game
        self.on_join_callback = on_join
        
        self.status_text = Text(parent=self.main_panel, text="", position=(0, -0.3), origin=(0,0))

    def cycle_map(self):
        self.current_map_index = (self.current_map_index + 1) % len(self.maps)
        self.map_btn.text = f"Map: {self.maps[self.current_map_index]}"

    def host_game(self):
        self.status_text.text = "Starting Server..."
        if self.on_host_callback:
            self.on_host_callback(self.maps[self.current_map_index]) # Pass map name
            self.enabled = False 
            
    def join_game(self):
        code = self.join_input.text
        if len(code) != 6:
            self.status_text.text = "Invalid Code! Must be 6 digits."
            return
            
        self.status_text.text = f"Joining Room {code}..."
        if self.on_join_callback:
            self.on_join_callback(code)
            self.enabled = False

class GameUI(Entity):
    def __init__(self, player, battle_manager):
        super().__init__()
        self.player = player
        self.battle_manager = battle_manager
        
        # Battle HUD (Top Bar)
        self.top_bar = Entity(parent=camera.ui, model='quad', scale=(0.6, 0.08), position=(0, 0.45), color=color.rgba(0,0,0,0.5))
        self.team_1_score = Text(parent=self.top_bar, text='100', position=(-0.45, 0), origin=(0,0), scale=2.5, color=color.blue)
        self.team_2_score = Text(parent=self.top_bar, text='100', position=(0.45, 0), origin=(0,0), scale=2.5, color=color.red)
        self.timer_text = Text(parent=self.top_bar, text='10:00', position=(0, 0), origin=(0,0), scale=2.5)
        
        # Player HUD
        self.crosshair = Entity(parent=camera.ui, model='circle', scale=0.005, color=color.rgba(255, 255, 255, 150))
        self.ammo_text = Text(text='Ammo: 1/1', position=(0.7, -0.4), scale=2, origin=(0,0))
        self.health_bar = Entity(parent=camera.ui, model='quad', color=color.red, scale=(0.3, 0.02), position=(-0.7, 0.45), origin=(-0.5, 0))
        
        # Class Selection (Hidden by default)
        self.class_menu = Entity(parent=camera.ui, enabled=False)
        self.bg = Entity(parent=self.class_menu, model='quad', scale=(1, 0.6), color=color.rgba(0,0,0,0.8))
        
        y = 0.2
        for class_name, class_obj in vars(Classes).items():
            if isinstance(class_obj, type): continue # Skip internal types
            if class_name.startswith('__'): continue
            
            # Button for each class
            btn = Button(parent=self.class_menu, text=class_obj.name, scale=(0.3, 0.05), position=(0, y))
            btn.on_click = Func(self.select_class, class_obj)
            y -= 0.1
            
        # Pause Menu
        self.pause_menu = Entity(parent=camera.ui, enabled=False)
        self.pause_bg = Entity(parent=self.pause_menu, model='quad', scale=(10, 10), color=color.rgba(0,0,0,0.8))
        self.resume_btn = Button(parent=self.pause_menu, text='Resume', scale=(0.3, 0.08), position=(0, 0.1), on_click=self.toggle_pause)
        self.quit_btn = Button(parent=self.pause_menu, text='Quit', scale=(0.3, 0.08), position=(0, -0.1), on_click=application.quit)
        
        # Initial State
        self.class_menu_active = False

    def toggle_pause(self):
        self.pause_menu.enabled = not self.pause_menu.enabled
        mouse.locked = not self.pause_menu.enabled
        
    def show_class_menu(self):
        self.class_menu.enabled = True
        self.class_menu_active = True
        mouse.locked = False
        
    def select_class(self, game_class):
        print(f"Selected {game_class.name}")
        self.player.set_class(game_class)
        self.class_menu.enabled = False
        self.class_menu_active = False
        mouse.locked = True
        
    def input(self, key):
        if key == 'escape':
            if self.class_menu.enabled:
                self.class_menu.enabled = False
                self.class_menu_active = False
                mouse.locked = True
            else:
                self.toggle_pause()
                
        if key == 'm':
            if not self.pause_menu.enabled:
                self.show_class_menu()
        
    def update(self):
        # Update Battle HUD
        if self.battle_manager:
            self.team_1_score.text = str(self.battle_manager.team_1_tickets)
            self.team_2_score.text = str(self.battle_manager.team_2_tickets)
            
            minutes = int(self.battle_manager.game_time // 60)
            seconds = int(self.battle_manager.game_time % 60)
            self.timer_text.text = f"{minutes:02d}:{seconds:02d}"
            
        # Update Player HUD
        if self.player.current_weapon:
             cw = self.player.current_weapon
             if hasattr(cw, 'ammo'):
                if cw.is_reloading:
                     self.ammo_text.text = "Reloading..."
                     self.ammo_text.color = color.yellow
                elif cw.ammo > 0:
                     self.ammo_text.text = f"Ready ({cw.ammo})"
                     self.ammo_text.color = color.green
                else:
                     self.ammo_text.text = "Empty (Press R)"
                     self.ammo_text.color = color.red
             else:
                  self.ammo_text.text = "Melee"
                  self.ammo_text.color = color.white
        else:
            self.ammo_text.text = ""
