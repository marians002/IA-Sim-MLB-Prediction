def get_takeover(closers :list, reliefs :list, inning):
    if inning >=8:
        pitcher = closers.pop(0)
        closers.append(pitcher)
        return pitcher
    pitcher = reliefs.pop(0)
    reliefs.append(pitcher)
    return pitcher

def select_starting_pitcher(rotation : list):
    # Seleccionar el abridor con el mejor rendimiento reciente
    pitcher = rotation.pop()
    rotation.insert(1, pitcher)  # Rotate teams

def pitcher_val(pitcher):
    return pitcher.k_percent * (1-pitcher.bb_percent) * (1-pitcher.avg) * pitcher.pa

def categorize_pitchers(pitchers : list):
    # Categorizar a los pitchers en abridores, cerradores y relevistas
    non_oppeners = list(sorted(pitchers, key=pitcher_val, reverse=True)[4])
    non_oppeners.sort(key=lambda p: categorize_pitchers(p) * p.gf, reverse=True)
    
    return pitchers[:4], non_oppeners[:3], non_oppeners[3:]
