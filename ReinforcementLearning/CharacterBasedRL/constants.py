import numpy as np

OBS_SHAPE = (6, 5, 2)
OBS_DTYPE = np.float64

GREY_REWARD = - 2
GREEN_REWARD = 5
YELLOW_REWARD = 2
WIN_REWARD = OBS_SHAPE[1] * GREEN_REWARD
WIN_BONUS = 25
LOSE_REWARD = -15
SAME_GUESS_REWARD = - 2
