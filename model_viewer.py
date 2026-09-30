from ursina import *
import importlib
import model_builder

app = Ursina()

# Camera
EditorCamera()
Sky()

# State
current_model = None
model_name_text = Text(text="Select a Model", position=(-0.85, 0.45), scale=2, origin=(0,0))
instruction_text = Text(text="R to Reload Code | Mouse to Orbit", position=(-0.85, 0.4), scale=1)

def show_model(builder_func_name):
    global current_model
    if current_model:
        destroy(current_model)
        
    print(f"Building: {builder_func_name}")
    model_name_text.text = builder_func_name
    
    # Create valid parent
    current_model = Entity()
    
    # Reload module to get fresh code
    try:
        importlib.reload(model_builder)
        func = getattr(model_builder, builder_func_name)
        func(current_model)
    except Exception as e:
        print(f"Error building model: {e}")
        destroy(current_model)
        current_model = None

def create_ui():
    # List functions starting with 'build_'
    funcs = [f for f in dir(model_builder) if f.startswith('build_')]
    
    y = 0.3
    for f in funcs:
        b = Button(text=f.replace('build_', ''), scale=(0.2, 0.05), position=(-0.7, y))
        b.on_click = Func(show_model, f)
        y -= 0.06

create_ui()

def input(key):
    if key == 'r':
        if current_model:
            # Re-trigger the current model build
            name = model_name_text.text
            show_model(name)

app.run()
