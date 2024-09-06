# class Player:
#     def __init__(self, last_name_first_name, player_id, year, p_game, pa, ab, hit, single, double, triple, home_run,
#                  strikeout, walk, k_percent, bb_percent, batting_avg, slg_percent, on_base_percent, on_base_plus_slg,
#                  woba, xwoba, sweet_spot_percent, barrel_batted_rate, hard_hit_percent, avg_best_speed, avg_hyper_speed,
#                  whiff_percent, swing_percent, pitch_hand):
#         self.last_name_first_name = last_name_first_name
#         self.player_id = player_id
#         self.year = year
#         self.p_game = p_game
#         self.pa = pa
#         self.ab = ab
#         self.hit = hit
#         self.single = single
#         self.double = double
#         self.triple = triple
#         self.home_run = home_run
#         self.strikeout = strikeout
#         self.walk = walk
#         self.k_percent = k_percent
#         self.bb_percent = bb_percent
#         self.batting_avg = batting_avg
#         self.slg_percent = slg_percent
#         self.on_base_percent = on_base_percent
#         self.on_base_plus_slg = on_base_plus_slg
#         self.woba = woba
#         self.xwoba = xwoba
#         self.sweet_spot_percent = sweet_spot_percent
#         self.barrel_batted_rate = barrel_batted_rate
#         self.hard_hit_percent = hard_hit_percent
#         self.avg_best_speed = avg_best_speed
#         self.avg_hyper_speed = avg_hyper_speed
#         self.whiff_percent = whiff_percent
#         self.swing_percent = swing_percent
#         self.pitch_hand = pitch_hand

class Player:
    def __init__(self, last_name_first_name, player_id, year, p_game, pitch_hand):
        self.last_name_first_name = last_name_first_name
        self.player_id = player_id
        self.year = year
        self.p_game = p_game
        self.pitch_hand = pitch_hand


class Batter(Player):
    def __init__(self, last_name_first_name, player_id, year, p_game, pitch_hand, pa, ab, hit, single, double, triple,
                 home_run,
                 strikeout, walk, k_percent, bb_percent, batting_avg, slg_percent, on_base_percent, on_base_plus_slg,
                 woba, xwoba, sweet_spot_percent, barrel_batted_rate, hard_hit_percent, avg_best_speed, avg_hyper_speed,
                 whiff_percent, swing_percent):
        super().__init__(last_name_first_name, player_id, year, p_game, pitch_hand)
        self.pa = pa
        self.ab = ab
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


class Pitcher(Player):
    def __init__(self, last_name_first_name, player_id, year, p_game, pitch_hand, ip, era, whip, k_9, bb_9, hr_9, fip,
                 xfip,
                 k_percent, bb_percent, ground_ball_percent, fly_ball_percent, line_drive_percent, soft_contact_percent,
                 medium_contact_percent, hard_contact_percent):
        super().__init__(last_name_first_name, player_id, year, p_game, pitch_hand)
        self.ip = ip
        self.era = era
        self.whip = whip
        self.k_9 = k_9
        self.bb_9 = bb_9
        self.hr_9 = hr_9
        self.fip = fip
        self.xfip = xfip
        self.k_percent = k_percent
        self.bb_percent = bb_percent
        self.ground_ball_percent = ground_ball_percent
        self.fly_ball_percent = fly_ball_percent
        self.line_drive_percent = line_drive_percent
        self.soft_contact_percent = soft_contact_percent
        self.medium_contact_percent = medium_contact_percent
        self.hard_contact_percent = hard_contact_percent
