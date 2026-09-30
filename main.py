from ursina import *
from core.game_manager import game_manager
from core.assets import AssetManager

app = Ursina()

# High Quality Setup (Applied after Ursina init)
window.title = "Nations At War: Reforged"
window.borderless = False
window.exit_button.visible = False
window.fps_counter.enabled = True

# Graphics Settings
window.cog_button.enabled = False 

# Shadows & Lighting
# Note: Ursina's shadow system requires specific shader setup on entities
# We will enable a directional light with shadows
sun = DirectionalLight()
sun.look_at(Vec3(1, -1, -1))
sun.shadow_map_resolution = Vec2(2048, 2048) # High Res Shadows

# Ambient Light
AmbientLight(color=color.rgba(100, 100, 100, 0.5))

# Sky
Sky(texture='sky_default') # Ursina default or load custom if available

# Fog
scene.fog_density = .02
scene.fog_color = color.light_gray

# Networking & Menu
from networking import NetworkManager
from ui import MainMenu
from map import create_map
from player import GamePlayer

net_manager = None
local_player = None

def start_host(map_name="Plains"):
    global net_manager, local_player
    net_manager = NetworkManager(app, is_server=True)
    start_gameplay(map_name)
    print_on_screen(f"HOSTING - CODE: {net_manager.room_code}", position=(-0.8, 0.45), scale=2, duration=100)

def start_join(code):
    global net_manager, local_player
    net_manager = NetworkManager(app, is_server=False, room_code=code)
    start_gameplay("Plains") # Syncing map is Phase 5 (Networking Polish)
    
def start_gameplay(map_name="Plains"):
    global local_player
    create_map(map_name)
    local_player = GamePlayer(position=(0, 2, 0))
    # UI Setup
    from gamemode import BattleManager
    from ui import GameUI
    bm = BattleManager()
    ui = GameUI(local_player, bm)
    game_manager.start_game()
    
# Show Menu
menu = MainMenu(on_host=start_host, on_join=start_join)

# Update Loop
def update():
    if net_manager:
        net_manager.update()
    if local_player:
        local_player.update()

def input(key):
    if key == 'escape':
        mouse.locked = not mouse.locked

app.run()
