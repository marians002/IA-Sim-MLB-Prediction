import random

class Pool():
    def __init__(self, pitchers, batters):
        self.pitchers = []
        self.batters = []
        
        for _, row in pitchers.iterrows():
            player = Player(
                name=row['name'],
                age=row['age'],
                team=row['team'],
                goals=row['goals']
            )
        self.pitchers.append(player)
        
        for _, row in batters.iterrows():
            player = Player(
                name=row['name'],
                age=row['age'],
                team=row['team'],
                goals=row['goals']
            )
        self.batters.append(player)
    
    def random_population(self, size):
        population = []
        for  _ in range(size):
            team = random.sample(self.batters, k=8) + random.sample(self.pitchers, k=1)
            population.append(team)
        
        return population
        
class Player:
    def __init__(self, name, age):
        self.name = name
        self.age = age

class Pitcher(Player):
    def __init__(self, name, age):
        super().__init__(name, age)
        


    
def fitness_lineup(team):
    val = 0
    val += team[0].obp*0.5 + team[0].speed*0.3 + team[0].avg*0.2
    val += team[1].obp*0.5 + team[1].speed*0.3 + team[1].avg*0.2
    val += team[2].obp*0.5 + team[2].speed*0.3 + team[2].avg*0.2
    val += team[3].obp*0.5 + team[3].speed*0.3 + team[3].avg*0.2
    val += team[4].obp*0.5 + team[4].speed*0.3 + team[4].avg*0.2
    val += team[5].obp*0.5 + team[5].speed*0.3 + team[5].avg*0.2
    val += team[6].obp*0.5 + team[6].speed*0.3 + team[6].avg*0.2
    val += team[7].obp*0.5 + team[7].speed*0.3 + team[7].avg*0.2
    val += team[8].obp*0.5 + team[8].speed*0.3 + team[8].avg*0.2
    
    return val