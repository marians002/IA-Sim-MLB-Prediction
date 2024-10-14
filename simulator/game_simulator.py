import json
from manager.BDI import *
from simulator.calculate_probs import *


class GameSimulator:
    def __init__(self, manager, t1, t2, batters_t1, batters_t2, h_lineup,
                 a_lineup, h_bullpen, a_bullpen):
        self.manager = manager
        self.home_team = t1.team_name
        self.away_team = t2.team_name
        self.batters_t1 = batters_t1
        self.batters_t2 = batters_t2
        self.bullpen_h = h_bullpen
        self.bullpen_a = a_bullpen
        self.game_state = GameState()
        self.log = []
        self.home_team_lineup = h_lineup
        self.away_team_lineup = a_lineup
        self.h_pitcher = h_lineup[0]  # El primero en la rotación
        self.a_pitcher = a_lineup[0]  # El primero en la rotación
        self.defensive_rate_home = calculate_defensive_rate(h_lineup)
        self.defensive_rate_away = calculate_defensive_rate(a_lineup)
        self.current_batter = 0  # Bateadores comienzan en el 1 del lineup y el pitcher en el 0

    def simulate_game(self):
        self.log.append({'Game between: ': f"{self.home_team} and {self.away_team}"})
        for inning in range(1, 10):
            self.game_state.inning = inning
            self.simulate_inning()
            # Super KO
            if self.game_state.score_difference >= 15:
                self.log.append({'Final result': "The game ended by Super KO"})
                break
        self.log.append({'Final result': f"{self.home_team}: {self.game_state.home_score}  "
                                         f"{self.away_team}: {self.game_state.away_score}"})

    def simulate_inning(self):
        while self.game_state.outs < 3:
            # Get current batter and pitcher and update it in the game_state
            batter = self.get_next_batter()
            pitcher = self.get_current_pitcher()
            self.game_state.update(pitcher=pitcher, batter=batter)

            # Evaluate the rules and make decisions
            intention = self.manager.run(self.game_state)

            # result: string['out', 'single', 'double', 'triple', 'home_run', 'walk', 'strikeout', 'bunt']
            # action_result: string explaining result
            result, action_result = self.apply_manager_decision(intention)

            # Si la acción del manager permite que el bateador batee, efectuar el pitcheo
            if result is None:
                result, pitches = determine_pitch_result(batter, pitcher, self.game_state.runner_on_first,
                                                         self.get_pitch_count(), self.get_def_rate())
                self.update_pitch_count(pitches)
            else:
                self.update_pitch_count()

            self.update_log(batter, pitcher, intention.name, result, action_result)
            self.update_game_state(result)
            if self.reset_inning():
                self.update_log(self.game_state.batter, self.game_state.pitcher, 'No action', 'Change teams',
                                'Change teams')
                break

    def get_next_batter(self):
        if (self.current_batter + 1) < 10:
            self.current_batter += 1
        else:
            self.current_batter = 1

        if self.game_state.home_team_batting:
            return self.home_team_lineup[self.current_batter]
        return self.away_team_lineup[self.current_batter]

    def get_current_pitcher(self):
        if self.game_state.home_team_batting:
            return self.a_pitcher
        return self.h_pitcher

    def get_def_rate(self):
        if self.game_state.home_team_batting:
            return self.defensive_rate_away
        return self.defensive_rate_home

    def update_pitcher(self, new_pitcher):
        if new_pitcher:
            if self.game_state.home_team_batting:
                self.a_pitcher = new_pitcher
                self.game_state.pitch_count_away = 0
            else:
                self.h_pitcher = new_pitcher
                self.game_state.pitch_count_home = 0

    def swap_teams(self):
        if self.game_state.home_team_batting:
            self.game_state.update(home_team_batting=False)
        else:
            self.game_state.update(home_team_batting=True)

    def apply_manager_decision(self, decision: Intention):
        if decision.name == "Change Pitcher":
            bullpen = self.bullpen_a if self.game_state.home_team_batting else self.bullpen_h
            new_pitcher, action_result = decision.action(self.game_state, bullpen)
            self.update_pitcher(new_pitcher)
            return None, action_result

        elif decision.name == "Pinch Hitter":
            if self.game_state.home_team_batting:
                text = decision.action(self.game_state, self.batters_t1, self.home_team_lineup,
                                       self.current_batter)
                # Como hubo un cambio en el line-up, hay que recalcular la defensa
                self.defensive_rate_home = calculate_defensive_rate(self.home_team_lineup)
                return None, text
            else:
                text = decision.action(self.game_state, self.batters_t2, self.away_team_lineup,
                                       self.current_batter)
                # Como hubo un cambio en el line-up, hay que recalcular la defensa
                self.defensive_rate_away = calculate_defensive_rate(self.away_team_lineup)
                return None, text

        elif decision.name == "Infield In":
            result, text = decision.action(self.game_state, self.get_pitch_count(), self.get_def_rate())
            return result, text

        elif (decision.name == "Steal Base" or decision.name == "Bunt" or decision.name == "Pickoff"
              or decision.name == "Intentional Walk" or decision.name == "Hit and Run"
              or decision.name == "No action"):
            return decision.action(self.game_state)

        # elif decision.name == "No action":
        #     return None, 'No action taken.'
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
        elif result == 'double_play':
            self.game_state.update(outs=self.game_state.outs + 2)
            self.game_state.remove_runners(1)
        elif result == 'bunt':
            self.game_state.advance_runners(bases=1)
            self.game_state.remove_runners(1)  # Porque al avanzar a los corredores una base, se queda uno en primera
            self.game_state.update(outs=self.game_state.outs + 1)
        elif result == 'hitrun':
            self.game_state.update(runner_on_third=self.game_state.runner_on_first,
                                   runner_on_first=self.game_state.batter)
        elif result == 'pickoff_1':
            self.game_state.update(outs=self.game_state.outs + 1)
            self.game_state.remove_runners(1)
        elif result == 'pickoff_3':
            self.game_state.update(outs=self.game_state.outs + 1)
            self.game_state.remove_runners(3)
        self.game_state.update(score_difference=abs(self.game_state.home_score - self.game_state.away_score))

    def get_pitch_count(self):
        if self.game_state.home_team_batting:
            return self.game_state.pitch_count_away
        return self.game_state.pitch_count_home

    def update_pitch_count(self, pitches=1):
        if self.game_state.home_team_batting:
            self.game_state.update(pitch_count_away=self.game_state.pitch_count_away + pitches)
        else:
            self.game_state.update(pitch_count_home=self.game_state.pitch_count_home + pitches)

    def reset_inning(self):
        # Reset inning if 3 outs
        if self.game_state.outs >= 3:
            self.game_state.update(outs=0)
            self.game_state.reset_bases()
            self.swap_teams()
            if self.game_state.home_team_batting:
                self.game_state.update(inning=self.game_state.inning + 1)
                return True
        return False

    def update_log(self, batter, pitcher, action, result, action_result):
        if self.game_state.home_team_batting:
            batting_team = self.home_team
        else:
            batting_team = self.away_team

        runner_on_first = (f"{self.game_state.runner_on_first.first_name} {self.game_state.runner_on_first.last_name}"
                           if self.game_state.runner_on_first else None)
        runner_on_second = (
            f"{self.game_state.runner_on_second.first_name} {self.game_state.runner_on_second.last_name}"
            if self.game_state.runner_on_second else None)
        runner_on_third = (f"{self.game_state.runner_on_third.first_name} {self.game_state.runner_on_third.last_name}"
                           if self.game_state.runner_on_third else None)

        self.log.append({
            'Inning': self.game_state.inning,
            'Batting Team': batting_team,
            'Home Score': self.game_state.home_score,
            'Away Score': self.game_state.away_score,
            'Pitch Count Home': self.game_state.pitch_count_home,
            'Pitch Count Away': self.game_state.pitch_count_away,
            'Outs': self.game_state.outs,
            'Batter': f"{batter.first_name} {batter.last_name}",
            'Pitcher': f"{pitcher.first_name} {pitcher.last_name}",
            'Runner on First': runner_on_first,
            'Runner on Second': runner_on_second,
            'Runner on Third': runner_on_third,
            'Manager Action': action,
            'Action Result': action_result,
            'Result': result
        })

    def save_log(self, filename):
        # print(self.log)
        with open(filename, 'w') as f:
            json.dump(self.log, f, indent=4)
