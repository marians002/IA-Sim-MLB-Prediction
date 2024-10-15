class GameState:
    """
    A class to represent the state of a baseball game.

    Attributes:
    -----------
    home_team_batting : bool
        Indicates if the home team is currently batting.
    pitch_count_home : int
        The number of pitches thrown by the home team.
    pitch_count_away : int
        The number of pitches thrown by the away team.
    batter : object
        The current batter.
    pitcher : object
        The current pitcher.
    runner_on_first : object
        The runner on first base.
    runner_on_second : object
        The runner on second base.
    runner_on_third : object
        The runner on third base.
    outs : int
        The number of outs in the current inning.
    inning : int
        The current inning.
    close_play : bool
        Indicates if there is a close play.
    challenges_left : int
        The number of challenges left for the team.
    score_difference : int
        The difference in score between the two teams.
    runs_allowed_last_2_innings : int
        The number of runs allowed in the last two innings.
    home_score : int
        The score of the home team.
    away_score : int
        The score of the away team.
    """

    def __init__(self):
        """
        Initializes the GameState with default values.
        """
        self.home_team_batting = True  # Home team bats first
        self.pitch_count_home = 0
        self.pitch_count_away = 0
        self.batter = None
        self.pitcher = None
        self.runner_on_first = None
        self.runner_on_second = None
        self.runner_on_third = None
        self.outs = 0
        self.inning = 1
        self.close_play = False
        self.challenges_left = 2
        self.score_difference = 0
        self.runs_allowed_last_2_innings = 0
        self.home_score = 0
        self.away_score = 0

    def advance_runners(self, bases=0, walk=False, home_run=False):
        """
        Advances the runners on the bases.

        Parameters:
        -----------
        bases : int, optional
            The number of bases to advance (default is 0).
        walk : bool, optional
            Indicates if the batter walked (default is False).
        home_run : bool, optional
            Indicates if the batter hit a home run (default is False).
        """
        batter = self.batter
        if self.home_team_batting:
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
            if self.home_team_batting:
                self.home_score = new_score
            else:
                self.away_score = new_score
            self.reset_bases()
        elif walk:
            if not self.runner_on_first:
                self.runner_on_first = batter
            elif not self.runner_on_second:
                self.runner_on_second = self.runner_on_first
                self.runner_on_first = batter
            elif not self.runner_on_third:
                self.runner_on_third = self.runner_on_second
                self.runner_on_second = self.runner_on_first
                self.runner_on_first = batter
            else:
                if self.home_team_batting:
                    self.home_score += 1
                else:
                    self.away_score += 1
        else:
            if bases == 1:
                if self.runner_on_third:
                    if self.home_team_batting:
                        self.home_score += 1
                    else:
                        self.away_score += 1
                    self.runner_on_third = None
                if self.runner_on_second:
                    self.runner_on_third = self.runner_on_second
                    self.runner_on_second = None
                if self.runner_on_first:
                    self.runner_on_second = self.runner_on_first
                    self.runner_on_first = None
                self.runner_on_first = batter
            elif bases == 2:
                if self.runner_on_third:
                    if self.home_team_batting:
                        self.home_score += 1
                    else:
                        self.away_score += 1
                    self.runner_on_third = None
                if self.runner_on_second:
                    if self.home_team_batting:
                        self.home_score += 1
                    else:
                        self.away_score += 1
                    self.runner_on_second = None
                if self.runner_on_first:
                    self.runner_on_third = self.runner_on_first
                    self.runner_on_first = None
                self.runner_on_second = batter
            elif bases == 3:
                if self.runner_on_third:
                    if self.home_team_batting:
                        self.home_score += 1
                    else:
                        self.away_score += 1
                    self.runner_on_third = None
                if self.runner_on_second:
                    if self.home_team_batting:
                        self.home_score += 1
                    else:
                        self.away_score += 1
                    self.runner_on_second = None
                if self.runner_on_first:
                    if self.home_team_batting:
                        self.home_score += 1
                    else:
                        self.away_score += 1
                    self.runner_on_first = None
                self.runner_on_third = batter

    def remove_runners(self, bases=0):
        """
        Removes the runners from the bases.

        Parameters:
        -----------
        bases : int, optional
            The base from which to remove the runner (default is 0).
            1 for first base, 2 for second base, 3 for third base, 4 for all bases.
        """
        if bases == 1:
            self.runner_on_first = None
        elif bases == 2:
            self.runner_on_second = None
        elif bases == 3:
            self.runner_on_third = None
        elif bases == 4:
            self.reset_bases()

    def reset_bases(self):
        """
        Resets all the bases, removing all runners.
        """
        self.update(runner_on_first=None,
                    runner_on_second=None,
                    runner_on_third=None)

    def reset(self):
        """
        Resets the game state to its initial values.
        """
        self.__init__()

    def update(self, **kwargs):
        """
        Updates the game state with the provided keyword arguments.

        Parameters:
        -----------
        **kwargs : dict
            The attributes to update and their new values.
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def __str__(self):
        """
        Returns a string representation of the game state.

        Returns:
        --------
        str
            A string representation of the current game state.
        """
        if self.home_team_batting:
            batting_team = 'Home'
        else:
            batting_team = 'Away'

        runner_on_first = (f"{self.runner_on_first.first_name} {self.runner_on_first.last_name}"
                           if self.runner_on_first else None)
        runner_on_second = (f"{self.runner_on_second.first_name} {self.runner_on_second.last_name}"
                            if self.runner_on_second else None)
        runner_on_third = (f"{self.runner_on_third.first_name} {self.runner_on_third.last_name}"
                           if self.runner_on_third else None)

        return (f"GameState:\n"
                f"Batting team={batting_team}\n"
                f"Pitch count Home={self.pitch_count_home}\n"
                f"Pitch count Away={self.pitch_count_away}\n"
                f"Batter={self.batter.first_name} {self.batter.last_name}\n"
                f"Pitcher={self.pitcher.first_name} {self.pitcher.last_name}\n"
                f"Runner on first={runner_on_first}\n"
                f"Runner on second={runner_on_second}\n"
                f"Runner on third={runner_on_third}\n"
                f"Outs={self.outs}\n"
                f"Inning={self.inning}\n"
                f"Close play={self.close_play}\n"
                f"Challenges left={self.challenges_left}\n"
                f"Score difference={self.score_difference}\n"
                f"Runs allowed last 2 innings={self.runs_allowed_last_2_innings}\n"
                f"Home score={self.home_score}\n"
                f"Away score={self.away_score}")