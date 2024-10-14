class Team:
    def __init__(self, team_name, players=None):
        if players is None:
            players = []
        self.team_name = team_name
        self.players = players

    def add_player(self, player):
        self.players.append(player)
        
    def __str__(self):
        print(self.team_name)

