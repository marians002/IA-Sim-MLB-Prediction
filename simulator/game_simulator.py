import json
from simulator.apply_rules import *

import random


def determine_pitch_result(batter, pitcher, pitch_count):
    strikes = 0
    balls = 0
    total_pitches = 0

    # Calculate probabilities for each pitch outcome
    strike_prob = (pitcher.k_percent + batter.k_percent) / 200
    ball_prob = (pitcher.bb_percent + batter.bb_percent) / 200
    foul_prob = 0.2  # Initial probability of a foul ball
    hit_prob = (batter.avg + pitcher.avg) / 2
    out_prob = 1 - (strike_prob + ball_prob + foul_prob + hit_prob)
    outcomes = ['strike', 'ball', 'foul', 'hit', 'out']

    # Increase hit probability after 70 pitches
    if pitch_count > 70:
        hit_prob *= 1.1

    batter_single_rate = batter.single / batter.ab
    batter_double_rate = batter.double / batter.ab
    batter_triple_rate = batter.triple / batter.ab
    batter_home_run_rate = batter.home_run / batter.ab
    pitcher_single_rate = pitcher.single / pitcher.ab
    pitcher_double_rate = pitcher.double / pitcher.ab
    pitcher_triple_rate = pitcher.triple / pitcher.ab
    pitcher_home_run_rate = pitcher.home_run / pitcher.ab

    single_prob = (batter_single_rate + pitcher_single_rate) / 2
    double_prob = (batter_double_rate + pitcher_double_rate) / 2
    triple_prob = (batter_triple_rate + pitcher_triple_rate) / 2
    home_run_prob = (batter_home_run_rate + pitcher_home_run_rate) / 2

    # Normalize hit probabilities
    hit_total_prob = single_prob + double_prob + triple_prob + home_run_prob
    hit_probabilities = [single_prob / hit_total_prob, double_prob / hit_total_prob, triple_prob / hit_total_prob,
                         home_run_prob / hit_total_prob]
    while True:
        total_pitches += 1

        # Normalize probabilities to sum to 1
        total_prob = strike_prob + ball_prob + foul_prob + hit_prob + out_prob
        probabilities = [strike_prob / total_prob, ball_prob / total_prob, foul_prob / total_prob,
                         hit_prob / total_prob, out_prob / total_prob]

        pitch_result = random.choices(outcomes, probabilities)[0]

        if pitch_result == 'strike':
            strikes += 1
            if strikes >= 3:
                return 'strikeout', total_pitches
        elif pitch_result == 'ball':
            balls += 1
            if balls >= 4:
                return 'walk', total_pitches
        elif pitch_result == 'foul':
            # Decrease probability of a foul ball each time to prevent infinite at-bats
            foul_prob *= 0.8
            if strikes < 2:
                strikes += 1
        elif pitch_result == 'hit':
            # Determine type of hit
            hit_outcomes = ['single', 'double', 'triple', 'home_run']
            hit_result = random.choices(hit_outcomes, hit_probabilities)[0]
            return hit_result, total_pitches
        elif pitch_result == 'out':
            return 'out', total_pitches


class GameSimulator:
    def __init__(self, manager, batters_t1, pitchers_t1, batters_t2, pitchers_t2, h_lineup, a_lineup):
        self.manager = manager
        self.batters_t1 = batters_t1
        self.pitchers_t1 = pitchers_t1
        self.batters_t2 = batters_t2
        self.pitchers_t2 = pitchers_t2
        self.game_state = GameState()
        self.log = []
        self.home_team_lineup = h_lineup
        self.away_team_lineup = a_lineup
        self.h_pitcher = h_lineup[0]  # El primero en la rotación
        self.a_pitcher = a_lineup[0]  # El primero en la rotación
        self.current_batter = 0  # Bateadores comienzan en el 1 del lineup y el pitcher en el 0

    def simulate_game(self):
        # Example simulation logic
        for inning in range(1, 10):
            self.game_state.inning = inning
            self.simulate_inning()
            # Super KO
            if self.game_state.score_difference >= 15:
                self.log.append({'Final result': "The game ended by Super KO"})
                break

    def simulate_inning(self):
        while self.game_state.outs < 3:
            # Get current batter and pitcher and update it in the game_state
            batter = self.get_next_batter()
            pitcher = self.get_current_pitcher()
            self.game_state.update(pitcher=pitcher, batter=batter)

            # Evaluate the rules and make decisions

            # decision del manager
            action = self.manager.evaluate_rules(self.game_state)

            # result: string['out', 'single', 'double', 'triple', 'home_run', 'walk', 'strikeout', 'bunt']
            # action_result: string explaining result
            result, action_result = self.apply_manager_decision(action)

            # Si la acción del manager permite que el bateador batee, efectuar el pitcheo
            if result is None:
                result, pitches = determine_pitch_result(batter, pitcher, self.get_pitch_count())
                self.update_pitch_count(pitches)
            else:
                self.update_pitch_count()

            self.update_game_state(result)
            self.update_log(batter, pitcher, action, result, action_result)
            if self.reset_inning():
                self.update_log(batter, pitcher, 'No action', 'Change teams', 'Change teams')
                break

    def get_next_batter(self):
        if (self.current_batter + 1) < 10:
            self.current_batter += 1
        else:
            self.current_batter = 1

        if self.game_state.batting_team == 1:
            return self.home_team_lineup[self.current_batter]
        return self.away_team_lineup[self.current_batter]

    def get_current_pitcher(self):
        if self.game_state.batting_team == 1:
            return self.a_pitcher
        return self.h_pitcher

    def swap_teams(self):
        if self.game_state.batting_team == 1:
            self.game_state.update(batting_team=0)
        else:
            self.game_state.update(batting_team=1)

    def apply_manager_decision(self, decision):
        # Handle decisions
        if decision == "change_pitcher_rule":
            bullpen = self.pitchers_t2 if self.game_state.batting_team == 1 else self.pitchers_t1
            new_pitcher, action_result = change_pitcher(self.game_state, bullpen)
            if new_pitcher:
                if self.game_state.batting_team == 1:
                    self.a_pitcher = new_pitcher
                    self.game_state.pitch_count_away = 0
                else:
                    self.h_pitcher = new_pitcher
                    self.game_state.pitch_count_home = 0
            return None, action_result

        elif decision == "steal_base_rule":
            return None, steal_base_rule(self.game_state)

        elif decision == "bunt_rule":
            return bunt_rule(self.game_state)

        elif decision == "pinch_hitter_rule":
            if self.game_state.batting_team == 1:
                return None, pinch_hitter_rule(self.game_state, self.batters_t1, self.home_team_lineup,
                                               self.current_batter)
            else:
                return None, pinch_hitter_rule(self.game_state, self.batters_t2, self.away_team_lineup,
                                               self.current_batter)

        elif decision == "hit_and_run_rule":
            return hit_and_run_rule(self.game_state)

        elif decision == "intentional_walk_rule":
            return intentional_walk_rule(self.game_state)


        elif decision == "No action":
            return None, 'No action taken.'
        # Add more decision handling as needed
        else:
            return None, "Decision not recognized or not implemented yet."

    def update_game_state(self, result):
        if result == 'strikeout':
            self.game_state.update(outs=self.game_state.outs + 1)
        elif result == 'walk':
            self.game_state.advance_runners(walk=True)
        elif result == 'single':
            self.game_state.advance_runners(bases=1)
        elif result == 'double':
            self.game_state.advance_runners(bases=2)
        elif result == 'triple':
            self.game_state.advance_runners(bases=3)
        elif result == 'home_run':
            self.game_state.advance_runners(home_run=True)
        elif result == 'out':
            self.game_state.update(outs=self.game_state.outs + 1)
        elif result == 'bunt':
            self.game_state.advance_runners(bases=1)
            self.game_state.remove_runners(1)  # Porque al avanzar a los corredores una base, se queda uno en primera
            self.game_state.update(outs=self.game_state.outs + 1)
        elif result == 'hitrun':
            self.game_state.update(runner_on_third=True, runner_on_first=True)

        self.game_state.update(score_difference=abs(self.game_state.home_score - self.game_state.away_score))

    def get_pitch_count(self):
        if self.game_state.batting_team == 1:
            return self.game_state.pitch_count_away
        return self.game_state.pitch_count_home

    def update_pitch_count(self, pitches=1):
        if self.game_state.batting_team == 1:
            self.game_state.update(pitch_count_away=self.game_state.pitch_count_away + pitches)
        else:
            self.game_state.update(pitch_count_home=self.game_state.pitch_count_home + pitches)

    def reset_inning(self):
        # Reset inning if 3 outs
        if self.game_state.outs >= 3:
            self.game_state.update(outs=0)
            self.game_state.reset_bases()
            self.swap_teams()
            if self.game_state.batting_team == 1:
                self.game_state.update(inning=self.game_state.inning + 1)
                return True
        return False

    def update_log(self, batter, pitcher, action, result, action_result):
        self.log.append({
            'Inning': self.game_state.inning,
            'Batting Team': self.game_state.batting_team,
            'Home Score': self.game_state.home_score,
            'Away Score': self.game_state.away_score,
            'Pitch Count Home': self.game_state.pitch_count_home,
            'Pitch Count Away': self.game_state.pitch_count_away,
            'Outs': self.game_state.outs,
            'Batter': f"{batter.first_name} {batter.last_name}",
            'Pitcher': f"{pitcher.first_name} {pitcher.last_name}",
            'Runner on First': self.game_state.runner_on_first,
            'Runner on Second': self.game_state.runner_on_second,
            'Runner on Third': self.game_state.runner_on_third,
            'Manager Action': action,
            'Action Result': action_result,
            'Result': result
        })

    def save_log(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.log, f, indent=4)
