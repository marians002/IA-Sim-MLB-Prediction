class Player:
    def __init__(self, last_name_first_name, player_id, year, ab, pa, hit,
                 single, double, triple, home_run, strikeout, walk,
                 k_percent, bb_percent, batting_avg, slg_percent, on_base_percent,
                 on_base_plus_slg, woba, xwoba, sweet_spot_percent,
                 barrel_batted_rate, hard_hit_percent, avg_best_speed,
                 avg_hyper_speed, whiff_percent, swing_percent):
        self.last_name_first_name = last_name_first_name
        self.player_id = player_id
        self.year = year
        self.ab = ab
        self.pa = pa
        self.hit = hit
        self.single = single
        self.double = double
        self.triple = triple
        self.home_run = home_run
        self.strikeout = strikeout
        self.walk = walk
        self.k_percent = k_percent
        self.bb_percent = bb_percent
        self.batting_avg =  batting_avg
        self.slg_percent = slg_percent
        self.on_base_percent = on_base_percent
        self.on_base_plus_slg = on_base_plus_slg
        self.woba = woba
        self.xwoba = xwoba
        self.sweet_spot_percent = sweet_spot_percent
        self.barrel_batted_rate = barrel_batted_rate
        self.hard_hit_percent = hard_hit_percent
        self.avg_best_speed = avg_best_speed
        self.avg_hyper_speed = avg_hyper_speed
        self.whiff_percent = whiff_percent
        self.swing_percent = swing_percent

#tested
class Batter(Player):
    def __init__(self,data):
        super().__init__(data[0], data[1], data[2], data[3], data[4], data[5],
                         data[6], data[7], data[8], data[9], data[10], data[11],
                         data[12], data[13], data[14],data[15], data[16], data[17], data[18], 
                         data[19], data[20],data[21], data[22], data[23], data[24], 
                         data[25], data[26])


#tested
class Pitcher(Player):
    def __init__(self, data):
        super().__init__(data[0], data[1], data[2], data[8], data[6], data[7],
                         data[9], data[10], data[11], data[12], data[13], data[14],
                         data[15], data[16], data[17],data[18], data[19], data[20],
                         data[21], data[22], data[23], data[24], data[25], data[26])
        self.player_age = data[3]
        self.p_game = data[4]
        self.p_formatted_ip = data[5]
        """ self.batting_avg = data[17] """
        self.pitch_hand = data[27]
