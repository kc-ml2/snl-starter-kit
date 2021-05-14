import marlenv

"""brief explanation of env
for details of Snake-v1, refer to
https://github.com/kc-ml2/marlenv

env_id = Snake-v1

observation_space.shape == (VISION_RANGE*2 + 1, VISION_RANGE*2 + 1, FRAME_STACK*NUM_CELL_TYPES)

VISION_RANGE * 2 + 1 : imagine a square where snake's head is in the center of it.
the area of square is the vision area, and vision_range*2 + 1 represents a side of square.

FRAME_STACK : how many steps to stack
this feature is necessary because, in some edge cases(snake moving in circle),
snake is actually moving but, state does not seem to change.

NUM_CELL_TYPE : the features. each represents
wall, fruit, my head, my body, my tail, others head, others body, others tail
"""


class Agent:
    def act(self, obs):
        raise NotImplementedError


def agent_factory():
    # initialize agent with arguments for test(inference) time
    agent = Agent()

    # load your saved model

    return agent
