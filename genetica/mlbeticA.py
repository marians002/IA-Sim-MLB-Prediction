import random
from genetica import geneticA
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

def fitness_lineup(lineup):
    val = 0
    val += lineup[0].on_base_percent
    val += 0.5*lineup[1].on_base_percent + 0.5*lineup[1].avg
    val += lineup[2].avg
    val += lineup[3].home_run
    val += 0.5*lineup[4].avg + 0.5*lineup[4].home_run
    # 6th player
    if lineup[5].oaa != None:
        val += 0.3*lineup[5].avg + 0.7*lineup[5].oaa
    else :
        val += lineup[5].avg
    # 7th player
    if lineup[6].oaa != None:
        val += 0.3*lineup[6].avg + 0.7*lineup[6].oaa
    else :
        val += lineup[6].avg
    # 8th player
    if lineup[7].oaa != None:
        val += lineup[7].oaa
    else :
        val += lineup[7].avg
    # 9th player
    if lineup[8].oaa != None:
        val += lineup[8].oaa
    else :
        val += lineup[8].avg
    return val
        


def initial_population(pitchers, batters, n =20):
    population = []
    
    C = []
    SS = []
    B1 = []
    B2 = []
    B3 = []
    LF = []
    CF = []
    RF = []
    DH = []
    rols = [C, B1, B2, B3, LF, CF, RF, SS, DH]
    
    for batter in batters:
        if batter.pos[0] == 'C':
            C.append(batter)
        elif batter.pos[0] == '1B':
            B1.append(batter)
        elif batter.pos[0] == '2B':
            B2.append(batter)
        elif batter.pos[0] == '3B':
            B3.append(batter)
        elif batter.pos[0] == 'SS':
            SS.append(batter)
        elif batter.pos[0] == 'LF':
            LF.append(batter)
        elif batter.pos[0] == 'CF':
            CF.append(batter)
        elif batter.pos[0] == 'RF':
            RF.append(batter)
        else:
            DH.append(batter)
    for _ in range(n):   
        lineup = [None]*10
        lineup[9] = random.choice(pitchers)
        
        for idx in range(len(rols)):
            lineup[idx] = random.choice(rols[idx])
        """ for p in lineup:
            print(p.pos) """
        population.append(lineup)
    
    return population
        
def get_lineup(pitchers, batters):
    population = initial_population(pitchers, batters)
    pool = list(batters)
    pool.extend(pitchers)
    return geneticA.genetic_algo(population, fitness_lineup, pool, search_t=10)