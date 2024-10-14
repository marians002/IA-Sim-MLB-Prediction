class Team:
    def __init__(self, team_name, players=None, id=0):
        if players is None:
            players = []
        self.team_name = team_name
        self.players = players
        self.id = id

    def add_player(self, player):
        self.players.append(player)
        
    def __str__(self):
        return self.team_name

