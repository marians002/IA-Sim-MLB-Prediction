class Team:
    def __init__(self, team_name, players=None, id=0):
        if players is None:
            players = []
        self.team_name = team_name
        self.players = players
        self.id = id
        self.league, self.division = self.get_league(team_name)
        self.geographic_rival = self.get_geographic_rival(team_name)

    def add_player(self, player):
        self.players.append(player)

    def get_league(self, team_name):
        # Define the divisions
        if team_name in ["Baltimore Orioles", "Boston Red Sox", "New York Yankees", "Tampa Bay Rays",
                         "Toronto Blue Jays"]:
            return "AL", "AL East"
        elif team_name in ["Chicago White Sox", "Cleveland Guardians", "Detroit Tigers", "Kansas City Royals",
                           "Minnesota Twins"]:
            return "AL", "AL Central"
        elif team_name in ["Houston Astros", "Los Angeles Angels", "Oakland Athletics", "Seattle Mariners",
                           "Texas Rangers"]:
            return "AL", "AL West"
        elif team_name in ["Atlanta Braves", "Miami Marlins", "New York Mets", "Philadelphia Phillies",
                           "Washington Nationals"]:
            return "NL", "NL East"
        elif team_name in ["Chicago Cubs", "Cincinnati Reds", "Milwaukee Brewers", "Pittsburgh Pirates",
                           "St. Louis Cardinals"]:
            return "NL", "NL Central"
        elif team_name in ["Arizona Diamondbacks", "Colorado Rockies", "Los Angeles Dodgers", "San Diego Padres",
                           "San Francisco Giants"]:
            return "NL", "NL West"
        else:
            raise Exception("Team not found in any division")

    def get_geographic_rival(self, team_name):
        # Define the geographic rivals
        geographic_rivals = {
            "New York Yankees": "New York Mets",
            "Boston Red Sox": "Atlanta Braves",
            "Toronto Blue Jays": "Philadelphia Phillies",
            "Tampa Bay Rays": "Miami Marlins",
            "Baltimore Orioles": "Washington Nationals",
            "Cleveland Guardians": "Cincinnati Reds",
            "Chicago White Sox": "Chicago Cubs",
            "Minnesota Twins": "Milwaukee Brewers",
            "Detroit Tigers": "Pittsburgh Pirates",
            "Kansas City Royals": "St. Louis Cardinals",
            "Houston Astros": "Colorado Rockies",
            "Seattle Mariners": "San Diego Padres",
            "Los Angeles Angels": "Los Angeles Dodgers",
            "Texas Rangers": "Arizona Diamondbacks",
            "Oakland Athletics": "San Francisco Giants",
            "New York Mets": "New York Yankees",
            "Atlanta Braves": "Boston Red Sox",
            "Philadelphia Phillies": "Toronto Blue Jays",
            "Miami Marlins": "Tampa Bay Rays",
            "Washington Nationals": "Baltimore Orioles",
            "Cincinnati Reds": "Cleveland Guardians",
            "Chicago Cubs": "Chicago White Sox",
            "Milwaukee Brewers": "Minnesota Twins",
            "Pittsburgh Pirates": "Detroit Tigers",
            "St. Louis Cardinals": "Kansas City Royals",
            "Colorado Rockies": "Houston Astros",
            "San Diego Padres": "Seattle Mariners",
            "Los Angeles Dodgers": "Los Angeles Angels",
            "Arizona Diamondbacks": "Texas Rangers",
            "San Francisco Giants": "Oakland Athletics"
        }
        return geographic_rivals.get(team_name, None)

    def __str__(self):
        return self.team_name