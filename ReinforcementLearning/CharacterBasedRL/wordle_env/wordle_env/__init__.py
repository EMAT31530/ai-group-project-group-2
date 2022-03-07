from ReinforcementLearning.CharacterBasedRL.wordle_env.wordle_env.src.wordle_char_env import WordleCharEnv


from gym.envs.registration import register

register(
    id="WordleChar-v0", entry_point="ReinforcementLearning.wordle_env.src.wordle_char_env:WordleCharEnv",
)
