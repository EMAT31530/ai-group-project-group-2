from wordle import Wordle

w = Wordle("abide")
for i in range(w.max_attempts):
    result, Win_state = w.blind_play_game('abide')

