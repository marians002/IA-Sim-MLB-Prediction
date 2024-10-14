class Team:
    def __init__(self, team_name, players=None, id=0):
        if players is None:
            players = []
        self.team_name = team_name
        self.players = players
        self.id = id
        self.league, self.division = self.get_league(team_name)

    def add_player(self, player):
        self.players.append(player)
    
    def get_league(self, team_name):
         # Define the divisions
        if team_name in ["Baltimore Orioles", "Boston Red Sox", "New York Yankees", "Tampa Bay Rays", "Toronto Blue Jays"]:
            return "AL", "AL East"
        elif team_name in ["Chicago White Sox", "Cleveland Guardians", "Detroit Tigers", "Kansas City Royals", "Minnesota Twins"]:
            return "AL", "AL Central"
        elif team_name in ["Houston Astros", "Los Angeles Angels", "Oakland Athletics", "Seattle Mariners", "Texas Rangers"]:
            return "AL", "AL West"
        elif team_name in ["Atlanta Braves", "Miami Marlins", "New York Mets", "Philadelphia Phillies", "Washington Nationals"]:
            return "NL", "NL East"
        elif team_name in ["Chicago Cubs", "Cincinnati Reds", "Milwaukee Brewers", "Pittsburgh Pirates", "St. Louis Cardinals"]:
            return "NL", "NL Central"
        elif team_name in ["Arizona Diamondbacks", "Colorado Rockies", "Los Angeles Dodgers", "San Diego Padres", "San Francisco Giants"]:
            return "NL", "NL West"
        else:
            raise Exception("Team not found in any division")
        
        
    def __str__(self):
        return self.team_name

