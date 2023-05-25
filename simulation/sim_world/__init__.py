from gym.envs.registration import register

register(
    id='Robot_Simulation_Pygame-v2',
    entry_point='sim_world.envs:CustomEnv',
    max_episode_steps=10000,
)
