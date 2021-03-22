import random


class RandomAgent:

    def act(self, obs):
        ac = random.randint(0, 3)
        return ac


def agent_factory():
    agent = RandomAgent()

    return agent
