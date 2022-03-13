import pickle

import gym
from stable_baselines3 import PPO

import wordle_env


def evaluate_character_model(env, model, episodes=1000, verbose=False):
    outcomes = (0, 0, 0)
    for i in range(episodes):
        obs = env.reset()
        done = False

        while not done:
            action, _states = model.predict(obs)
            obs, rewards, done, info = env.step(action)
            outcomes = [sum(x) for x in zip(outcomes, (env.outcomes[0], env.outcomes[1], env.outcomes[2]))]
            if verbose:
                env.render()

    return outcomes


f = lambda x: (x[1] + x[2]) / sum(x)
if __name__ == "__main__":
    env = gym.make("wordle-v0")
    model1 = PPO.load("models/best_model.zip")
    model8 = PPO.load("models8/best_model.zip")

    a = evaluate_character_model(env, model8)
    b = evaluate_character_model(env, model1)

    print(f"Model 1 : {f(b)}")
    print(f"Model 8 : {f(a)}")
