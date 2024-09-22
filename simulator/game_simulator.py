import json
from simulator.apply_rules import *


def determine_pitch_result(batter, pitcher, pitch_count):
    # Calculate relevant statistics
    batter_single_rate = batter.single / batter.ab
    batter_double_rate = batter.double / batter.ab
    batter_triple_rate = batter.triple / batter.ab
    batter_home_run_rate = batter.home_run / batter.ab
    pitcher_single_rate = pitcher.single / pitcher.ab
    pitcher_double_rate = pitcher.double / pitcher.ab
    pitcher_triple_rate = pitcher.triple / pitcher.ab
    pitcher_home_run_rate = pitcher.home_run / pitcher.ab

    # Calculate probabilities based on statistics
    strikeout_prob = (pitcher.k_percent + batter.k_percent) / 200
    walk_prob = (pitcher.bb_percent + batter.bb_percent) / 200
    hit_prob = (batter.avg + pitcher.avg) / 2
    if pitch_count > 70:
        hit_prob *= 1.1  # Increase hit probability if pitch count is high

    single_prob = (batter_single_rate + pitcher_single_rate) / 2
    double_prob = (batter_double_rate + pitcher_double_rate) / 2
    triple_prob = (batter_triple_rate + pitcher_triple_rate) / 2
    home_run_prob = (batter_home_run_rate + pitcher_home_run_rate) / 2
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
        self.no_batting_actions = ['bunt_rule', 'hit_and_run_rule']
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

    def simulate_inning(self):
        # Example inning simulation logic
        self.game_state.outs = 0
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
                result = determine_pitch_result(batter, pitcher, self.game_state.pitch_count)

            self.update_log(batter, pitcher, action, result, action_result)
            if self.update_game_state(result):
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
                else:
                    self.h_pitcher = new_pitcher
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

        elif decision == "No action":
            return None, 'No action taken.'
        # Add more decision handling as needed
        else:
            return None, "Decision not recognized or not implemented yet."

    def update_game_state(self, result):
        self.game_state.update(pitch_count=self.game_state.pitch_count + 1)
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
            'inning': self.game_state.inning,
            'batting_team': self.game_state.batting_team,
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
