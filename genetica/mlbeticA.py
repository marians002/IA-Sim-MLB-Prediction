import random
from genetica import geneticA

""" 
1er bateador: OBP   Modified: OBP + Sprint Speed
2do bateador: OBP + AVE
3ero: AVE
4to: HR             Modified: SLG
5to: AVE + HR       
6to: AVE + OAA              
7mo: AVE + OAA
8vo: OAA else AVE
9no: OAA else AVE   Modified: OAA + Speed + AVE
"""


def fitness_lineup(lineup):
    val = 0
    val += lineup[0].on_base_percent + lineup[0].avg_best_speed
    val += 0.5 * lineup[1].on_base_percent + 0.5 * lineup[1].avg
    val += lineup[2].avg
    val += lineup[3].slg_percent
    val += 0.5 * lineup[4].avg + 0.5 * lineup[4].home_run
    # 6th player
    if lineup[5].oaa is not None:
        val += 0.3 * lineup[5].avg + 0.7 * lineup[5].oaa
    else:
        val += lineup[5].avg
    # 7th player
    if lineup[6].oaa is not None:
        val += 0.3 * lineup[6].avg + 0.7 * lineup[6].oaa
    else:
        val += lineup[6].avg
    # 8th player
    if lineup[7].oaa is not None:
        val += lineup[7].oaa
    else:
        val += lineup[7].avg
    # 9th player
    if lineup[8].oaa is not None:
        val += lineup[8].oaa
    else:
        val += lineup[8].avg_best_speed + lineup[8].avg
    return val


def initial_population(pitchers, batters, n=20):
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
    OF = []
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
        elif batter.pos[0] == 'OF':
            OF.append(batter)
        else:
            DH.append(batter)
    
    base_replacement = [p for p in batters if p.pos[0] in ['1B','2B','3B','SS']]
    field_replacement = [p for p in batters if p.pos[0] in ['LF','CF','RF','OF']]
    DH_replacement = base_replacement + field_replacement 
         
    for idx in range(len(rols)):
        if rols[idx] == []:
            if idx == 1:
                B1.append(random.choice(base_replacement))
                B1[0].pos[0] = '1B'
                base_replacement.remove(B1[0])
                DH_replacement.remove(B1[0])
                if B1[0] in B2:
                    B2.remove(B1[0])
                elif B1[0] in SS:
                    SS.remove(B1[0])
                else:
                    B3.remove(B1[0])
                DH_replacement.remove(B1[0])
            elif idx == 2:
                B2.append(random.choice(base_replacement))
                B2[0].pos[0] = '2B'
                base_replacement.remove(B2[0])
                DH_replacement.remove(B2[0])
                if B2[0] in B1:
                    B1.remove(B2[0])
                elif B2[0] in SS:
                    SS.remove(B2[0])
                else:
                    B3.remove(B2[0])
            elif idx == 3:
                B3.append(random.choice(base_replacement))
                B3[0].pos[0] = '3B'
                base_replacement.remove(B3[0])
                DH_replacement.remove(B3[0])
                if B3[0] in B1:
                    B1.remove(B3[0])
                elif B3[0] in SS:
                    SS.remove(B3[0])
                else:
                    B2.remove(B3[0])
                DH_replacement.remove(B1[0])
            elif idx == 4:
                LF.append(random.choice(field_replacement))
                LF[0].pos[0] = 'LF'
                field_replacement.remove(LF[0])
                DH_replacement.remove(LF[0])
                if LF[0] in CF:
                    CF.remove(LF[0])
                else:
                    RF.remove(LF[0])
                DH_replacement.remove(LF[0])
            elif idx == 5:
                CF.append(random.choice(field_replacement))
                CF[0].pos[0] = 'CF'
                field_replacement.remove(CF[0])
                DH_replacement.remove(CF[0])
                if CF[0] in LF:
                    LF.remove(CF[0])
                else:
                    RF.remove(CF[0])
                DH_replacement.remove(CF[0])
            elif idx == 6:
                RF.append(random.choice(field_replacement))
                RF[0].pos[0] = 'RF'
                field_replacement.remove(RF[0])
                DH_replacement.remove(RF[0])
                if RF[0] in LF:
                    LF.remove(RF[0])
                else:
                    CF.remove(RF[0])
                DH_replacement.remove(RF[0])
            elif idx == 7:
                SS.append(random.choice(base_replacement))
                SS[0].pos[0] = 'SS'
                base_replacement.remove(SS[0])
                DH_replacement.remove(SS[0])
                if SS[0] in B1:
                    B1.remove(SS[0])
                elif SS[0] in B2:
                    B2.remove(SS[0])
                else:
                    B3.remove(SS[0])                    
            elif idx == 8:
                DH.append(random.choice(DH_replacement))
                DH_replacement.remove(DH[0])
                if DH[0] in base_replacement:
                    base_replacement.remove(DH[0])
                    if DH[0] in B1:
                        B1.remove(DH[0])
                    elif DH[0] in B2:
                        B2.remove(DH[0])
                    elif DH[0] in B3:
                        B3.remove(DH[0])
                    else:
                        SS.remove(DH[0])
                else:
                    field_replacement.remove(DH[0])
                    if DH[0] in LF:
                        LF.remove(DH[0])
                    elif DH[0] in CF:
                        CF.remove(DH[0])
                    else:
                        RF.remove(DH[0])
                
                DH[0].pos[0] = 'DH'
                
    # region TO CHANGE
    for _ in range(n):
        lineup = [None] * 10
        lineup[9] = random.choice(pitchers)

        for idx in range(len(rols)):
            lineup[idx] = random.choice(rols[idx])
        population.append(lineup) 
    """ a = []
    for individual in population:
        a.append([p.pos[0] for p in individual])
    print(a)
    print(len(a)) """
    
    return population


def get_lineup(pitchers, batters):
    population = initial_population(pitchers, batters)
    pool = list(batters)
    pool.extend(pitchers)
    return shift(geneticA.genetic_algo(population, fitness_lineup, pool, search_t=10))

def shift(iterable:list):
    next_e = iterable[-1]
    for i in range(len(iterable)):
        iterable[i], next_e = next_e, iterable[i]
    return iterable
