import gym
import gym_everwing

import random

from pynput import keyboard

running = True
def on_press(key):
    global running
    if str(key) == 'Key.cmd':
        running = False

try:
    with keyboard.Listener(on_press) as kl:
        env = gym.make('everwing-v0')

        print(dir(env))
        print(env.action_space)

        obs = env.reset()
        while running:

            action = random.randint(0, 6)
            print(action)

            obs, reward, done, info = env.step(action)
            env.render(close=done)

            if done: running = False

except Exception as e:
    print(e)

