from gym.envs.registration import register

register(
    id='everwing-v0',
    entry_point='gym_everwing.envs:EverWingEnv',
)
