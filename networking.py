from ursinanetworking import *
from ursina import *

import random

class NetworkManager:
    def __init__(self, app, is_server=False, ip='localhost', port=25565, room_code=None):
        self.app = app
        self.is_server = is_server
        self.client = None
        self.server = None
        self.room_code = room_code
        
        if self.is_server:
            # Generate Code if hosting
            if not self.room_code:
                self.room_code = self.generate_room_code()
            
            self.server = UrsinaNetworkingServer(ip, port)
            self.setup_server_events()
            print(f"Server started. Room Code: {self.room_code} (IP: {ip}:{port})")
        else:
            # Joining
            target_ip = ip
            target_port = port
            
            if self.room_code:
                target_ip = self.resolve_room_code(self.room_code)
                print(f"Resolved Room Code {self.room_code} to {target_ip}")
                
            self.client = UrsinaNetworkingClient(target_ip, target_port)
            self.setup_client_events()
            print(f"Connecting to {target_ip}:{target_port}...")

    def generate_room_code(self):
        # 6-digit code
        return str(random.randint(100000, 999999))

    def resolve_room_code(self, code):
        # In a real game, this would query a Master Server API.
        # For this standalone version, we will perform a 'magic' resolution.
        # If code matches our known active server (local), return localhost.
        # Otherwise default to localhost for testing or ask user.
        
        # Simulating external resolution:
        print(f"[MasterServer] Resolving {code}...")
        return 'localhost' # Force local for now, but infrastructure is there.

    def setup_server_events(self):
        @self.server.event
        def onClientConnected(client):
            print(f"{client.id} connected!")
            self.server.broadcast("player_joined", client.id)

        @self.server.event
        def onClientDisconnected(client):
            print(f"{client.id} disconnected!")
            self.server.broadcast("player_left", client.id)

    def setup_client_events(self):
        @self.client.event
        def onConnectionEstablished():
            print("Connected to server!")

        @self.client.event
        def onConnectionError(reason):
            print(f"Connection error: {reason}")
            
    def update(self):
        if self.is_server:
            self.server.process_net_events()
        elif self.client:
            self.client.process_net_events()
