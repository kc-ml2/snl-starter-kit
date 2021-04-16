import gym
import marlenv

from algo import Agent

N_STEPS = 10
if __name__ == '__main__':
    # TODO: validate icc? or just local sample rollouts
    agent = Agent()
    env = gym.make('Snake-v1', num_snakes=1)
    obs = env.reset()
    for _ in range(N_STEPS):
        ac = agent.act(obs)
        obs, dones, rew, info = env.step(ac)
        env.render('ascii')
