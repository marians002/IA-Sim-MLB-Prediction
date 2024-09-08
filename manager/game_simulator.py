import json
import random


def determine_pitch_result(batter, pitcher):
    # Simular el resultado del pitcheo basado en las estadísticas del bateador y lanzador
    outcomes = ['strikeout', 'walk', 'single', 'double', 'triple', 'home_run', 'out']
    probabilities = [0.2, 0.1, 0.3, 0.1, 0.05, 0.1, 0.15]  # Ejemplo de probabilidades
    result = random.choices(outcomes, probabilities)[0]
    return result


class GameSimulator:
    def __init__(self, manager, batters_df, pitchers_df):
        self.manager = manager
        self.batters_df = batters_df
        self.pitchers_df = pitchers_df
        self.game_state = {
            'pitch_count': 0,
            'opponent_batter': 'right',
            'runner_on_first': False,
            'runner_on_second': False,
            'runner_on_third': False,
            'outs': 0,
            'inning': 1,
            'close_play': False,
            'challenges_left': 2,
            'pitcher': 'right',
            'score_difference': 0,
            'runs_allowed_last_2_innings': 0,
            'current_batter_avg': 0.250,
            'opponent_batter_tendency': 'right',
            'home_score': 0,
            'away_score': 0
        }
        self.log = []

    def simulate_pitch(self):
        # Seleccionar un bateador y un lanzador aleatoriamente
        batter = self.batters_df.sample().iloc[0]
        pitcher = self.pitchers_df.sample().iloc[0]

        # Actualizar el estado del juego con las estadísticas del bateador y lanzador
        self.game_state['pitch_count'] += 1
        self.game_state['opponent_batter'] = '1'
        # self.game_state['opponent_batter'] = batter['handedness']
        self.game_state['pitcher'] = pitcher['pitch_hand']
        self.game_state['current_batter_avg'] = batter['avg']
        # self.game_state['opponent_batter_tendency'] = batter['tendency']
        self.game_state['opponent_batter_tendency'] = 'right'

        # Determinar el resultado del pitcheo
        result = determine_pitch_result(batter, pitcher)
        self.update_game_state(result)

        # Evaluar las reglas y tomar decisiones
        action = self.manager.evaluate_rules(self.game_state)
        self.log.append({
            'pitch_count': self.game_state['pitch_count'],
            'action': action,
            'result': result,
            'game_state': self.game_state.copy()
        })

    def update_game_state(self, result):
        if result == 'strikeout':
            self.game_state['outs'] += 1
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
            self.game_state['outs'] += 1

        # Reset inning if 3 outs
        if self.game_state['outs'] >= 3:
            self.game_state['outs'] = 0
            self.game_state['inning'] += 1
            self.reset_bases()

    def advance_runners(self, bases=0, walk=False, home_run=False):
        if home_run:
            self.game_state['home_score'] += 1
            if self.game_state['runner_on_first']:
                self.game_state['home_score'] += 1
            if self.game_state['runner_on_second']:
                self.game_state['home_score'] += 1
            if self.game_state['runner_on_third']:
                self.game_state['home_score'] += 1
            self.reset_bases()
        elif walk:
            if not self.game_state['runner_on_first']:
                self.game_state['runner_on_first'] = True
            elif not self.game_state['runner_on_second']:
                self.game_state['runner_on_second'] = True
            elif not self.game_state['runner_on_third']:
                self.game_state['runner_on_third'] = True
            else:
                self.game_state['home_score'] += 1
        else:
            if bases == 1:
                if self.game_state['runner_on_third']:
                    self.game_state['home_score'] += 1
                    self.game_state['runner_on_third'] = False
                if self.game_state['runner_on_second']:
                    self.game_state['runner_on_third'] = True
                    self.game_state['runner_on_second'] = False
                if self.game_state['runner_on_first']:
                    self.game_state['runner_on_second'] = True
                    self.game_state['runner_on_first'] = False
                self.game_state['runner_on_first'] = True
            elif bases == 2:
                if self.game_state['runner_on_third']:
                    self.game_state['home_score'] += 1
                    self.game_state['runner_on_third'] = False
                if self.game_state['runner_on_second']:
                    self.game_state['home_score'] += 1
                    self.game_state['runner_on_second'] = False
                if self.game_state['runner_on_first']:
                    self.game_state['runner_on_third'] = True
                    self.game_state['runner_on_first'] = False
                self.game_state['runner_on_second'] = True
            elif bases == 3:
                if self.game_state['runner_on_third']:
                    self.game_state['home_score'] += 1
                    self.game_state['runner_on_third'] = False
                if self.game_state['runner_on_second']:
                    self.game_state['home_score'] += 1
                    self.game_state['runner_on_second'] = False
                if self.game_state['runner_on_first']:
                    self.game_state['home_score'] += 1
                    self.game_state['runner_on_first'] = False
                self.game_state['runner_on_third'] = True

    def reset_bases(self):
        self.game_state['runner_on_first'] = False
        self.game_state['runner_on_second'] = False
        self.game_state['runner_on_third'] = False

    def simulate_game(self, pitches):
        for _ in range(pitches):
            self.simulate_pitch()

    def save_log(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.log, f, indent=4)

    def __str__(self):
        return (f"\nInning: {self.game_state['inning']}, "
                f"\nPitch Count: {self.game_state['pitch_count']}, "
                f"\nOpponent Batter: {self.game_state['opponent_batter']}, "
                f"\nRunner on First: {self.game_state['runner_on_first']}, "
                f"\nRunner on Second: {self.game_state['runner_on_second']}, "
                f"\nRunner on Third: {self.game_state['runner_on_third']}, "
                f"\nOuts: {self.game_state['outs']}, "
                f"\nClose Play: {self.game_state['close_play']}, "
                f"\nChallenges Left: {self.game_state['challenges_left']}, "
                f"\nPitcher: {self.game_state['pitcher']}, "
                f"\nScore Difference: {self.game_state['score_difference']}, "
                f"\nRuns Allowed Last 2 Innings: {self.game_state['runs_allowed_last_2_innings']}, "
                f"\nCurrent Batter Avg: {self.game_state['current_batter_avg']}, "
                f"\nOpponent Batter Tendency: {self.game_state['opponent_batter_tendency']}, "
                f"\nHome Score: {self.game_state['home_score']}, "
                f"\nAway Score: {self.game_state['away_score']}")
