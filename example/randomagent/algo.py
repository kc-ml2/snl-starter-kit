from random import randint


class Agent:
    """
    define your agent here
    """

    def __init__(self):
        pass

    def act(self, obs):
        ac = randint(0, 4)
        return ac


def agent_factory():
    agent = Agent()

    return agent
