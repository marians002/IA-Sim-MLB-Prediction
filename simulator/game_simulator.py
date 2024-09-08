import json
import random
from simulator.game_state import *


def determine_pitch_result(batter, pitcher):
    # Extract relevant statistics
    batter_avg = batter.avg
    pitcher_k_percent = pitcher.k_percent
    pitcher_bb_percent = pitcher.bb_percent

    # Calculate probabilities based on statistics
    strikeout_prob = pitcher_k_percent / 100
    walk_prob = pitcher_bb_percent / 100
    hit_prob = batter_avg
    single_prob = hit_prob * 0.6
    double_prob = hit_prob * 0.2
    triple_prob = hit_prob * 0.05
    home_run_prob = hit_prob * 0.15
    out_prob = 1 - (strikeout_prob + walk_prob + hit_prob)

    # Normalize probabilities to sum to 1
    total_prob = (strikeout_prob + walk_prob + single_prob + double_prob + triple_prob + home_run_prob + out_prob)
    probabilities = [strikeout_prob / total_prob, walk_prob / total_prob, single_prob / total_prob,
                     double_prob / total_prob, triple_prob / total_prob, home_run_prob / total_prob,
                     out_prob / total_prob]

    outcomes = ['strikeout', 'walk', 'single', 'double', 'triple', 'home_run', 'out']
    result = random.choices(outcomes, probabilities)[0]
    return result


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
        self.current_batter = 0  # Bateadores comienzan en el 1 del lineup y el pitcher en el 0

    def simulate_game(self):
        # Example simulation logic
        for inning in range(1, 10):
            self.game_state.inning = inning
            self.simulate_inning()

    def simulate_inning(self):
        # Example inning simulation logic
        self.game_state.outs = 0
        while self.game_state.outs < 3:
            batter = self.get_next_batter()
            pitcher = self.get_current_pitcher()
            result = self.simulate_pitch(batter, pitcher)
            # Evaluate the rules and make decisions
            action = self.manager.evaluate_rules(self.game_state)
            self.log.append({
                'pitch_count': self.game_state.pitch_count,
                'action': action,
                'result': result,
                'game_state': self.game_state.__dict__.copy()
            })
            if self.update_game_state(result):
                break

    def get_next_batter(self):
        if (self.current_batter + 1) < 10:
            self.current_batter += 1
        else:
            self.current_batter = 1
        return self.home_team_lineup[self.current_batter]

    def get_current_pitcher(self):
        return self.away_team_lineup[0]

    def simulate_pitch(self, batter, pitcher):
        # Update the game state with the batter's and pitcher's statistics
        self.game_state.update(
            pitch_count=self.game_state.pitch_count + 1,
            opponent_batter=self.current_batter,
            pitcher_hand=pitcher.pitch_hand,
            current_batter_avg=batter.avg,
            opponent_batter_tendency='right'  # Placeholder
            # opponent_batter_tendency=batter['tendency']
            # opponent_batter=batter['handedness'],
        )

        # Determine the result of the pitch
        return determine_pitch_result(batter, pitcher)

    def update_game_state(self, result):
        if result == 'strikeout':
            self.game_state.update(outs=self.game_state.outs + 1)
        elif result == 'walk':
            self.advance_runners(walk=True)
        elif result == 'single':
            self.advance_runners(bases=1)
        elif result == 'double':
            self.advance_runners(bases=2)
        elif result == 'triple':
            self.advance_runners(bases=3)
        elif result == 'home_run':
            self.advance_runners(home_run=True)
        elif result == 'out':
            self.game_state.update(outs=self.game_state.outs + 1)

        # Reset inning if 3 outs
        if self.game_state.outs >= 3:
            self.game_state.update(outs=0, inning=self.game_state.inning + 1)
            self.reset_bases()
            return True
        return False

    def advance_runners(self, bases=0, walk=False, home_run=False):
        if home_run:
            new_home_score = self.game_state.home_score + 1
            if self.game_state.runner_on_first:
                new_home_score += 1
            if self.game_state.runner_on_second:
                new_home_score += 1
            if self.game_state.runner_on_third:
                new_home_score += 1
            self.game_state.update(home_score=new_home_score)
            self.reset_bases()
        elif walk:
            if not self.game_state.runner_on_first:
                self.game_state.update(runner_on_first=True)
            elif not self.game_state.runner_on_second:
                self.game_state.update(runner_on_second=True)
            elif not self.game_state.runner_on_third:
                self.game_state.update(runner_on_third=True)
            else:
                self.game_state.update(home_score=self.game_state.home_score + 1)
        else:
            if bases == 1:
                if self.game_state.runner_on_third:
                    self.game_state.update(home_score=self.game_state.home_score + 1, runner_on_third=False)
                if self.game_state.runner_on_second:
                    self.game_state.update(runner_on_third=True, runner_on_second=False)
                if self.game_state.runner_on_first:
                    self.game_state.update(runner_on_second=True, runner_on_first=False)
                self.game_state.update(runner_on_first=True)
            elif bases == 2:
                if self.game_state.runner_on_third:
                    self.game_state.update(home_score=self.game_state.home_score + 1, runner_on_third=False)
                if self.game_state.runner_on_second:
                    self.game_state.update(home_score=self.game_state.home_score + 1, runner_on_second=False)
                if self.game_state.runner_on_first:
                    self.game_state.update(runner_on_third=True, runner_on_first=False)
                self.game_state.update(runner_on_second=True)
            elif bases == 3:
                if self.game_state.runner_on_third:
                    self.game_state.update(home_score=self.game_state.home_score + 1, runner_on_third=False)
                if self.game_state.runner_on_second:
                    self.game_state.update(home_score=self.game_state.home_score + 1, runner_on_second=False)
                if self.game_state.runner_on_first:
                    self.game_state.update(home_score=self.game_state.home_score + 1, runner_on_first=False)
                self.game_state.update(runner_on_third=True)

    def reset_bases(self):
        self.game_state.update(runner_on_first=False,
                               runner_on_second=False,
                               runner_on_third=False)

    def save_log(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.log, f, indent=4)


