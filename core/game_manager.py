from ursina import *
from core.entities import BaseEntity

class GameManager(Entity):
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GameManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__()
        self.state = "MENU" # MENU, LOBBY, GAME, END
        self.players = []
        
        # Game Rules
        self.team_1_tickets = 100
        self.team_2_tickets = 100
        self.score_limit = 0 # 0 = use tickets
        
    def start_game(self):
        print("Starting Game...")
        self.state = "GAME"
        # Reset Tickets
        self.team_1_tickets = 100
        self.team_2_tickets = 100
        
    def end_game(self, winner_team):
        print(f"Game Over! Team {winner_team} Wins!")
        self.state = "END"
        # Show End ScreenUI
        
    def register_player(self, player):
        self.players.append(player)
        
    def check_win_condition(self):
        if self.state != "GAME": return
        
        if self.team_1_tickets <= 0:
            self.end_game(2)
        elif self.team_2_tickets <= 0:
            self.end_game(1)

game_manager = GameManager()
