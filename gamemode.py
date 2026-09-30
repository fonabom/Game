from ursina import *

class BattleManager(Entity):
    def __init__(self):
        super().__init__()
        self.team_1_tickets = 100 # e.g. British
        self.team_2_tickets = 100 # e.g. French
        self.game_time = 600 # 10 Minutes
        self.game_active = True
        
    def update(self):
        if self.game_active:
            self.game_time -= time.dt
            if self.game_time <= 0:
                self.end_round("Time Limit Reached")
                
            if self.team_1_tickets <= 0:
                self.end_round("Team 2 Wins!")
            elif self.team_2_tickets <= 0:
                self.end_round("Team 1 Wins!")
                
    def reduce_ticket(self, team_id, amount=1):
        if team_id == 1:
            self.team_1_tickets -= amount
        else:
            self.team_2_tickets -= amount
            
    def end_round(self, reason):
        self.game_active = False
        print(f"Game Over: {reason}")
        # Signal UI to show end screen