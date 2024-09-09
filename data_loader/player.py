import math


class Player:
    def __init__(self, first_name, last_name, player_id, pa, ab, hit,
                 single, double, triple, home_run, strikeout, walk,
                 k_percent, bb_percent, avg, slg_percent, on_base_percent,
                 on_base_plus_slg, woba, xwoba, sweet_spot_percent,
                 barrel_batted_rate, hard_hit_percent, avg_best_speed,
                 avg_hyper_speed, whiff_percent, swing_percent, pos):
        self.first_name = first_name
        self.last_name = last_name
        self.player_id = player_id
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
        self.avg = avg
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
        self.pos = pos


class Batter(Player):
    def __init__(self, data, pos=None):
        super().__init__(data[0], data[1], data[2], data[4], data[3], data[5],
                         data[6], data[7], data[8], data[9], data[10], data[11],
                         data[12], data[13], data[14], data[15], data[16], data[17], data[18],
                         data[19], data[20], data[21], data[22], data[23], data[24],
                         data[25], data[26], pos)

        if math.isnan(data[27]):
            self.arm_strength = None
        else:
            self.arm_strength = data[27]

        if math.isnan(data[28]):
            self.oaa = None
        else:
            self.oaa = data[28]
        self.sprint_speed = data[29]


class Pitcher(Player):
    def __init__(self, data, pos=None):
        super().__init__(data[0], data[1], data[2], data[6], data[7], data[8],
                         data[9], data[10], data[11], data[12], data[13], data[14],
                         data[15], data[16], data[17], data[18], data[19], data[20],
                         data[21], data[22], data[23], data[24], data[25], data[26],
                         data[27], data[28], data[29], pos)
        self.p_game = data[4]
        self.p_formatted_ip = data[5]
        self.pitch_hand = data[30]
