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

""" 
1er bateador: OBP
2do bateador: OBP + AVE
3ero: AVE
4to: HR
5to: AVE + HR
6to: AVE
7mo: AVE
8vo: AVE
9no: AVE
"""

def fitness_line_up(line_up):
    val = 0
    val += line_up[0].on_base_percent
    val += 0.5*line_up[2].on_base_percent + 0.5*line_up[2].batting_avg
    val += line_up[3].batting_avg
    val += line_up[4].home_run
    val += 0.5*line_up[5].batting_avg + 0.5*line_up[5].home_run
    val += 0.3*line_up[6].batting_avg + 0.7*line_up[6].oaa
    val += 0.3*line_up[7].batting_avg + 0.7*line_up[7].oaa
    val += line_up[8].oaa
    val += line_up[9].oaa