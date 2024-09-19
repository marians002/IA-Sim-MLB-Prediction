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


def steal_base_rule(runner):
    steal_probability = runner.sprint_speed / 100  # Assuming sprint_speed is a percentage
    if random.random() < steal_probability:
        return f"{runner.first_name} {runner.last_name} successfully stole the base!"
    else:
        return f"{runner.first_name} {runner.last_name} was caught stealing."


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
        self.batting_team = 1  # Home team bats first
        self.h_pitcher = h_lineup[0]  # El primero en la rotación
        self.a_pitcher = a_lineup[0]  # El primero en la rotación
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
            # Get current batter and pitcher and update it in the game_state
            batter = self.get_next_batter()
            pitcher = self.get_current_pitcher()
            self.game_state.update(pitcher=pitcher, batter=batter)
            # Evaluate the rules and make decisions
            action = self.manager.evaluate_rules(self.game_state)
            action_result = self.apply_manager_decision(action)
            result = self.simulate_pitch(batter, pitcher)
            self.update_log(batter, pitcher, action, result, action_result)
            if self.update_game_state(result):
                break

    def get_next_batter(self):
        if (self.current_batter + 1) < 10:
            self.current_batter += 1
        else:
            self.current_batter = 1

        if self.batting_team == 1:
            return self.home_team_lineup[self.current_batter]
        return self.away_team_lineup[self.current_batter]

    def get_current_pitcher(self):
        if self.batting_team == 1:
            return self.a_pitcher
        return self.h_pitcher

    def swap_teams(self):
        if self.batting_team == 1:
            self.batting_team = 0
        else:
            self.batting_team = 1

    def change_pitcher(self):
        bullpen = self.pitchers_t2 if self.batting_team == 1 else self.pitchers_t1
        if len(bullpen) > 1:
            new_pitcher = bullpen.pop(random.randint(1, len(bullpen) - 1))
            if self.batting_team == 1:
                self.a_pitcher = new_pitcher
            else:
                self.h_pitcher = new_pitcher
            self.game_state.update(pitch_count=0)
            return f"New pitcher is now {new_pitcher.first_name} {new_pitcher.last_name}"
        return 'No more pitchers available.'

    def apply_manager_decision(self, decision):
        # Handle decisions
        if decision == "change_pitcher_rule":
            return self.change_pitcher()
        elif decision == "steal_base_rule":
            return steal_base_rule(runner=self.game_state.batter)
        # Add more decision handling as needed
        else:
            return "Decision not recognized or not implemented yet."

    def simulate_pitch(self, batter, pitcher):
        # Update the game state with the batter's and pitcher's statistics
        self.game_state.update(
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
        self.game_state.update(pitch_count=self.game_state.pitch_count + 1)
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
            self.game_state.update(outs=0)
            self.reset_bases()
            self.swap_teams()
            if self.batting_team == 1:
                self.game_state.update(inning=self.game_state.inning + 1)
                return True
        return False

    def runner_on_third_update(self, current_score):
        if self.game_state.runner_on_third:
            if self.batting_team == 1:
                self.game_state.update(home_score=current_score + 1, runner_on_third=False)
            else:
                self.game_state.update(away_score=current_score + 1, runner_on_third=False)

    def runner_on_second_update(self, current_score):
        if self.game_state.runner_on_second:
            if self.batting_team == 1:
                self.game_state.update(home_score=current_score + 1, runner_on_second=False)
            else:
                self.game_state.update(away_score=current_score + 1, runner_on_second=False)

    def advance_runners(self, bases=0, walk=False, home_run=False):
        if self.batting_team == 1:
            current_score = self.game_state.home_score
        else:
            current_score = self.game_state.away_score

        if home_run:
            new_score = current_score + 1
            if self.game_state.runner_on_first:
                new_score += 1
            if self.game_state.runner_on_second:
                new_score += 1
            if self.game_state.runner_on_third:
                new_score += 1
            if self.batting_team == 1:
                self.game_state.update(home_score=new_score)
            else:
                self.game_state.update(away_score=new_score)
            self.reset_bases()
        elif walk:
            if not self.game_state.runner_on_first:
                self.game_state.update(runner_on_first=True)
            elif not self.game_state.runner_on_second:
                self.game_state.update(runner_on_second=True)
            elif not self.game_state.runner_on_third:
                self.game_state.update(runner_on_third=True)
            else:
                if self.batting_team == 1:
                    self.game_state.update(home_score=current_score + 1)
                else:
                    self.game_state.update(away_score=current_score + 1)
        else:
            if bases == 1:
                if self.game_state.runner_on_third:
                    if self.batting_team == 1:
                        self.game_state.update(home_score=current_score + 1, runner_on_third=False)
                    else:
                        self.game_state.update(away_score=current_score + 1, runner_on_third=False)
                if self.game_state.runner_on_second:
                    self.game_state.update(runner_on_third=True, runner_on_second=False)
                if self.game_state.runner_on_first:
                    self.game_state.update(runner_on_second=True, runner_on_first=False)
                self.game_state.update(runner_on_first=True)
            elif bases == 2:
                self.runner_on_third_update(current_score)
                self.runner_on_second_update(current_score)

                if self.game_state.runner_on_first:
                    self.game_state.update(runner_on_third=True, runner_on_first=False)
                self.game_state.update(runner_on_second=True)
            elif bases == 3:
                self.runner_on_third_update(current_score)
                self.runner_on_second_update(current_score)

                if self.game_state.runner_on_first:
                    if self.batting_team == 1:
                        self.game_state.update(home_score=current_score + 1, runner_on_first=False)
                    else:
                        self.game_state.update(away_score=current_score + 1, runner_on_first=False)
                self.game_state.update(runner_on_third=True)

    def reset_bases(self):
        self.game_state.update(runner_on_first=False,
                               runner_on_second=False,
                               runner_on_third=False)

    def update_log(self, batter, pitcher, action, result, action_result):
        self.log.append({
            'inning': self.game_state.inning,
            'batting_team': self.batting_team,
            'home_score': self.game_state.home_score,
            'away_score': self.game_state.away_score,
            'pitch_count': self.game_state.pitch_count,
            'outs': self.game_state.outs,
            'batter': f"{batter.first_name} {batter.last_name}",
            'pitcher': f"{pitcher.first_name} {pitcher.last_name}",
            'runner_on_first': self.game_state.runner_on_first,
            'runner_on_second': self.game_state.runner_on_second,
            'runner_on_third': self.game_state.runner_on_third,
            'action': action,
            'action_result': action_result,
            'result': result
        })

    def save_log(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.log, f, indent=4)
