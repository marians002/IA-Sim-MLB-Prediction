class GameState:
    def __init__(self):
        self.pitch_count = 0
        self.opponent_batter = 'right'
        self.runner_on_first = False
        self.runner_on_second = False
        self.runner_on_third = False
        self.outs = 0
        self.inning = 1
        self.close_play = False
        self.challenges_left = 2
        self.pitcher_hand = 'right'
        self.score_difference = 0
        self.runs_allowed_last_2_innings = 0
        self.current_batter_avg = 0.250
        self.opponent_batter_tendency = 'right'
        self.home_score = 0
        self.away_score = 0

    def reset(self):
        self.__init__()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def __str__(self):
        return (f"GameState:\n"
                f"Pitch count={self.pitch_count}\n"
                f"Opponent batter={self.opponent_batter}\n"
                f"Runner on first={self.runner_on_first}\n"
                f"Runner on second={self.runner_on_second}\n"
                f"Runner on third={self.runner_on_third}\n"
                f"Outs={self.outs}\n"
                f"Inning={self.inning}\n"
                f"Close play={self.close_play}\n"
                f"Challenges left={self.challenges_left}\n"
                f"Pitcher Handedness={self.pitcher_hand}\n"
                f"Score difference={self.score_difference}\n"
                f"Runs allowed last 2 innings={self.runs_allowed_last_2_innings}\n"
                f"Current batter avg={self.current_batter_avg}\n"
                f"Opponent batter tendency={self.opponent_batter_tendency}\n"
                f"Home score={self.home_score}\n"
                f"Away score={self.away_score}")

