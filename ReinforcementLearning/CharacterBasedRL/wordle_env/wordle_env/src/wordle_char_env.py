import warnings
from typing import Dict
from typing import Optional
from typing import Tuple

from colorama import Fore, Style
from colorama import Back

import random
import numpy as np
import gym
from gym import spaces

from ReinforcementLearning.CharacterBasedRL.constants import OBS_SHAPE, SAME_GUESS_REWARD, GREEN_REWARD, YELLOW_REWARD, \
    GREY_REWARD, WIN_REWARD, WIN_BONUS, LOSE_REWARD, OBS_DTYPE
from ReinforcementLearning.CharacterBasedRL.wordle_env.wordle_env.src.helpers import find_matches
from ReinforcementLearning.CharacterBasedRL.wordle_env.wordle_env.src.letter_mask import LetterMask
from ReinforcementLearning.CharacterBasedRL.wordle_env.wordle_env.words.valid_answers import valid_answers


class WordleCharEnv(gym.Env):
    """OpenAI Gym environment for wordle, where the action is 5 characters in order for the word.

    Inherits the base OpenAI Gym environment

    Attributes
    ----------
    metadata : Dict[str, List[str]]
        The available render modes for the environment.
    """

    metadata = {"render.modes": ["human"]}

    def __init__(self):
        """Constructor for the environment."""
        super().__init__()
        self.action_space = spaces.Discrete(26)
        self.observation_space = spaces.Box(
            low=0, high=27, shape=OBS_SHAPE, dtype=OBS_DTYPE
        )
        self.words = valid_answers
        self._answer = None
        self.state = None
        self.step_num = 0
        self._curr_guess = ""
        self._masker = LetterMask()
        self.won = False

        self._prev_step = None

    def step(
            self, action: int, check: Optional[bool] = False
    ) -> Tuple[np.ndarray, float, bool, Dict[str, np.ndarray]]:
        """The step function for the environment.

        This environment will take in letters until a word of length OBS_SPACE[1] is guessed. At
        which point, it will compare the word to the answer and check if the game is over, and get
        the score.

        Parameters
        ----------
        action : int
            Integer in the range [0, 26) representing the character that the player would like to
            guess.
        check : Optional[bool]
            Whether or not to check that the action is valid.

        Raises
        ------
        RuntimeError
            If the action is not within the range [0, 26)

        Returns
        -------
        Tuple[np.ndarray, float, bool, Dict[str, np.ndarray]
            The observation, reward, done flag, and a dictionary containing the action mask for the
            current step.
        """
        if action < 0 or action > 25:
            raise RuntimeError(
                f"Action must be between 0 and 25, got {action}."
            )

        reward = 0
        self._curr_guess += chr(ord("a") + action)

        # Insert the new letter into the right space to get the observation
        row = self.step_num // OBS_SHAPE[1]
        col = self.step_num % OBS_SHAPE[1]
        self.state[row, col, 0] = action + 1

        self.step_num += 1

        # Determine done condition
        done = self.step_num == OBS_SHAPE[0] * OBS_SHAPE[1]

        # Calculate reward
        if len(self._curr_guess) == OBS_SHAPE[1]:
            if self._curr_guess in self.guesses:
                reward += SAME_GUESS_REWARD
            self.guesses.append(self._curr_guess)
            answer_check = find_matches(self._curr_guess, self._answer)
            self.state[row, :, 1] = answer_check
            reward += sum([1 for x in answer_check if x == 2]) * GREEN_REWARD
            reward += sum([1 for x in answer_check if x == 1]) * YELLOW_REWARD
            reward += sum([1 for x in answer_check if x == 0]) * GREY_REWARD

            if done:
                if reward == WIN_REWARD:
                    self.won = True
                    reward += WIN_BONUS
                else:
                    reward += LOSE_REWARD
            self._curr_guess = ""
        else:
            reward = 0

        self._prev_step = (
            self.state,
            reward,
            done,
            {"mask": self._masker(self._curr_guess) if check else np.ones(26)},
        )

        return self._prev_step

    def reset(self) -> np.ndarray:
        """The reset function for the environment.

        Returns
        -------
        self.state : np.ndarray
            The current (new) state of the environment.
        """

        self._answer = np.random.choice(self.words)
        self.state = np.zeros(OBS_SHAPE, dtype=OBS_DTYPE)
        self.step_num = 0
        self.guesses = []
        self._masker.reset()
        self.won = False
        return self.state

    def render(
            self, mode: Optional[str] = "human", close: Optional[bool] = False
    ):
        """Function for rendering the environment in a human-viewable way.

        Parameters
        ----------
        mode : Optional[str]
            Which mode to render in. Only option is human.
        close : Optional[bool]
            Flag for closing the environment. Unused.
        """
        print(f"Guess {self.step_num // OBS_SHAPE[1]} | Solution = {self._answer}")
        for row in self.state:
            for col in row:
                if col[0] == 0:
                    print(Fore.WHITE + Back.BLACK + " ", end="")
                else:
                    if col[1] == 0:
                        print(
                            Fore.WHITE
                            + Back.BLACK
                            + chr(int(col[0]) + ord("a") - 1),
                            end="",
                        )
                    elif col[1] == 1:
                        print(
                            Fore.BLACK
                            + Back.YELLOW
                            + chr(int(col[0]) + ord("a") - 1),
                            end="",
                        )
                    else:
                        print(
                            Fore.BLACK
                            + Back.GREEN
                            + chr(int(col[0]) + ord("a") - 1),
                            end="",
                        )
                print(Style.RESET_ALL, end="")
            print()


    def seed(self, seed: Optional[int] = 0):
        """Function to seed the random number generation.

        Parameters
        ----------
        seed : Optional[int]
            Seed for RNG
        """
        np.random.seed(seed)
