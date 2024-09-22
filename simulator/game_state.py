class GameState:
    def __init__(self):
        self.batting_team = 1  # Home team bats first
        self.pitch_count = 0
        self.batter = None
        self.pitcher = None
        self.runner_on_first = False
        self.runner_on_second = False
        self.runner_on_third = False
        self.outs = 0
        self.inning = 1
        self.close_play = False
        self.challenges_left = 2
        self.score_difference = 0
        self.runs_allowed_last_2_innings = 0
        self.home_score = 0
        self.away_score = 0

    def advance_runners(self, bases=0, walk=False, home_run=False):
        if self.batting_team == 1:
            current_score = self.home_score
        else:
            current_score = self.away_score

        if home_run:
            new_score = current_score + 1
            if self.runner_on_first:
                new_score += 1
            if self.runner_on_second:
                new_score += 1
            if self.runner_on_third:
                new_score += 1
            if self.batting_team == 1:
                self.home_score = new_score
            else:
                self.away_score = new_score
            self.reset_bases()
        elif walk:
            if not self.runner_on_first:
                self.runner_on_first = True
            elif not self.runner_on_second:
                self.runner_on_second = True
            elif not self.runner_on_third:
                self.runner_on_third = True
            else:
                if self.batting_team == 1:
                    self.home_score += 1
                else:
                    self.away_score += 1
        else:
            if bases == 1:
                if self.runner_on_third:
                    if self.batting_team == 1:
                        self.home_score += 1
                    else:
                        self.away_score += 1
                    self.runner_on_third = False
                if self.runner_on_second:
                    self.runner_on_third = True
                    self.runner_on_second = False
                if self.runner_on_first:
                    self.runner_on_second = True
                    self.runner_on_first = False
                self.runner_on_first = True
            elif bases == 2:
                if self.runner_on_third:
                    if self.batting_team == 1:
                        self.home_score += 1
                    else:
                        self.away_score += 1
                    self.runner_on_third = False
                if self.runner_on_second:
                    if self.batting_team == 1:
                        self.home_score += 1
                    else:
                        self.away_score += 1
                    self.runner_on_second = False
                if self.runner_on_first:
                    self.runner_on_third = True
                    self.runner_on_first = False
                self.runner_on_second = True
            elif bases == 3:
                if self.runner_on_third:
                    if self.batting_team == 1:
                        self.home_score += 1
                    else:
                        self.away_score += 1
                    self.runner_on_third = False
                if self.runner_on_second:
                    if self.batting_team == 1:
                        self.home_score += 1
                    else:
                        self.away_score += 1
                    self.runner_on_second = False
                if self.runner_on_first:
                    if self.batting_team == 1:
                        self.home_score += 1
                    else:
                        self.away_score += 1
                    self.runner_on_first = False
                self.runner_on_third = True

    def runner_on_third_update(self, current_score):
        if self.runner_on_third:
            if self.batting_team == 1:
                self.update(home_score=current_score + 1, runner_on_third=False)
            else:
                self.update(away_score=current_score + 1, runner_on_third=False)

    def runner_on_second_update(self, current_score):
        if self.runner_on_second:
            if self.batting_team == 1:
                self.update(home_score=current_score + 1, runner_on_second=False)
            else:
                self.update(away_score=current_score + 1, runner_on_second=False)

    def remove_runners(self, bases=0):
        if bases == 1:
            self.runner_on_first = False
        elif bases == 2:
            self.runner_on_second = False
        elif bases == 3:
            self.runner_on_third = False
        elif bases == 4:
            self.reset_bases()

    def reset_bases(self):
        self.update(runner_on_first=False,
                    runner_on_second=False,
                    runner_on_third=False)

    def reset(self):
        self.__init__()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def __str__(self):
        return (f"GameState:\n"
                f"Batting team={self.batting_team}\n"
                f"Pitch count={self.pitch_count}\n"
                f"Batter={self.batter.first_name} {self.batter.last_name}\n"
                f"Pitcher={self.pitcher.first_name} {self.pitcher.last_name}\n"
                f"Runner on first={self.runner_on_first}\n"
                f"Runner on second={self.runner_on_second}\n"
                f"Runner on third={self.runner_on_third}\n"
                f"Outs={self.outs}\n"
                f"Inning={self.inning}\n"
                f"Close play={self.close_play}\n"
                f"Challenges left={self.challenges_left}\n"
                f"Score difference={self.score_difference}\n"
                f"Runs allowed last 2 innings={self.runs_allowed_last_2_innings}\n"
                f"Home score={self.home_score}\n"
                f"Away score={self.away_score}")
