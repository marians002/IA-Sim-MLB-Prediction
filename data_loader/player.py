class Player:
    def __init__(self, first_name, last_name, player_id, year, ab, pa, hit,
                 single, double, triple, home_run, strikeout, walk,
                 k_percent, bb_percent, batting_avg, slg_percent, on_base_percent,
                 on_base_plus_slg, woba, xwoba, sweet_spot_percent,
                 barrel_batted_rate, hard_hit_percent, avg_best_speed,
                 avg_hyper_speed, whiff_percent, swing_percent, pos):
        self.first_name = first_name
        self.last_name = last_name
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
        self.batting_avg = batting_avg
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

    def to_dict(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'player_id': self.player_id,
            'year': self.year,
            'ab': self.ab,
            'pa': self.pa,
            'hit': self.hit,
            'single': self.single,
            'double': self.double,
            'triple': self.triple,
            'home_run': self.home_run,
            'strikeout': self.strikeout,
            'walk': self.walk,
            'k_percent': self.k_percent,
            'bb_percent': self.bb_percent,
            'batting_avg': self.batting_avg,
            'slg_percent': self.slg_percent,
            'on_base_percent': self.on_base_percent,
            'on_base_plus_slg': self.on_base_plus_slg,
            'woba': self.woba,
            'xwoba': self.xwoba,
            'sweet_spot_percent': self.sweet_spot_percent,
            'barrel_batted_rate': self.barrel_batted_rate,
            'hard_hit_percent': self.hard_hit_percent,
            'avg_best_speed': self.avg_best_speed,
            'avg_hyper_speed': self.avg_hyper_speed,
            'whiff_percent': self.whiff_percent,
            'swing_percent': self.swing_percent,
            'pos': self.pos
        }


class Batter(Player):
    def __init__(self, data, pos=None):
        super().__init__(data[0], data[1], data[2], data[3], data[4], data[5],
                         data[6], data[7], data[8], data[9], data[10], data[11],
                         data[12], data[13], data[14], data[15], data[16], data[17], data[18],
                         data[19], data[20], data[21], data[22], data[23], data[24],
                         data[25], data[26], data[27], pos)

    def to_dict(self):
        return super().to_dict()


class Pitcher(Player):
    def __init__(self, data, pos=None):
        super().__init__(data[0], data[1], data[2], data[6], data[7], data[8],
                         data[9], data[10], data[11], data[12], data[13], data[14],
                         data[15], data[16], data[17], data[18], data[19], data[20],
                         data[21], data[22], data[23], data[24], data[25], data[26],
                         data[27], data[28], data[29], data[30], pos)
        self.player_age = data[4]
        self.p_game = data[5]
        self.p_formatted_ip = data[6]
        self.pitch_hand = data[31]

    def to_dict(self):
        player_dict = super().to_dict()
        player_dict.update({
            'player_age': self.player_age,
            'p_game': self.p_game,
            'p_formatted_ip': self.p_formatted_ip,
            'pitch_hand': self.pitch_hand
        })
        return player_dict
