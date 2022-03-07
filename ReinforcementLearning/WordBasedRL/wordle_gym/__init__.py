from gym.envs.registration import register

register(
    id="WordleWord-v0", entry_point="ReinforcementLearning.WordBasedRL.wordle_gym.envs.wordle_word_env:WordleWordEnv",
)
