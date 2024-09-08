class Team:
    def __init__(self, team_name):
        # self.team_id = team_id
        self.team_name = team_name
        self.players = []

    def add_player(self, player):
        self.players.append(player)

    def to_dict(self):
        return {
            'team_name': self.team_name,
            'players': [player.to_dict() for player in self.players]
        }
