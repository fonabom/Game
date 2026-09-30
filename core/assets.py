from ursina import *
import os

# Centralized Asset Manager
# Handles loading models (including external OBJs) and textures safely.

class AssetManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AssetManager, cls).__new__(cls)
            cls._instance.model_cache = {}
            cls._instance.texture_cache = {}
        return cls._instance

    @staticmethod
    def get_model(name):
        # 1. Try Cache
        if name in AssetManager().model_cache:
            return AssetManager().model_cache[name]
        
        # 2. Try External Model (d:/NW/models/)
        external_path = f'models/{name}'
        # Ursina load_model checks multiple extensions (.ursinamesh, .obj, .glb, .blend)
        m = load_model(name) 
        
        # Note: Ursina's load_model already caches, but we might want custom logic
        # If not found, use a fallback
        if not m:
            print(f"[AssetManager] Warning: Model '{name}' not found. Using 'cube'.")
            m = 'cube'
            
        AssetManager().model_cache[name] = m
        return m

    @staticmethod
    def get_texture(name):
        return load_texture(name)

# Helper for global access
def get_model(name): return AssetManager.get_model(name)
def get_texture(name): return AssetManager.get_texture(name)
