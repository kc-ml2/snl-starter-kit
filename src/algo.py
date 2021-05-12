# import random
# import marlenv
#
# """brief explanation of env
# for details of Snake-v1, refer to
# https://github.com/kc-ml2/marlenv
#
# env_id = Snake-v1
#
# observation_space.shape == (VISION_RANGE*2 + 1, VISION_RANGE*2 + 1, FRAME_STACK*NUM_CELL_TYPES)
#
# VISION_RANGE * 2 + 1 : imagine a square where snake's head is in the center of it.
# the area of square is the vision area, and vision_range*2 + 1 represents a side of square.
#
# FRAME_STACK : how many steps to stack
# this feature is necessary because, in some edge cases(snake moving in circle),
# snake is actually moving but, state does not seem to change.
#
# NUM_CELL_TYPE : the features. each represents
# wall, fruit, my head, my body, my tail, others head, others body, others tail
# """
#
#
# class Agent:
#     def act(self, obs):
#         raise NotImplementedError
#
#
#
# def agent_factory():
#     # initialize agent with arguments for test(inference) time
#     agent = Agent()
#
#     # load your saved model
#
#     return agent
# import os
#
# import gym
# import marlenv
# from easydict import EasyDict
# from marlenv.wrappers import SingleAgent
# from rl2.agents.ppo import PPOModel, PPOAgent
#
# custom_reward = {
#     'fruit': 1.0,
#     'kill': 0.0,
#     'lose': 0.0,
#     'win': 0.0,
#     'time': 0.1
# }
#
#
# def make_snake():
#     def _make():
#         env = gym.make("Snake-v1",
#                        num_snakes=1, width=20, height=20,
#                        vision_range=5, frame_stack=2,
#                        reward_dict=custom_reward)
#         env = SingleAgent(env)
#         return env
#
#     return _make
#
#
# def make_single():
#     n_env = 1
#     env = make_snake()()
#     observation_shape = env.observation_space.shape
#     action_shape = (env.action_space.n,)
#     high = env.observation_space.high
#     return n_env, env, observation_shape, action_shape, high
#
#
# n_env, env, observation_shape, action_shape, high = make_single()
# reorder = True
#
# myconfig = {
#     'tag': 'TUTORIAL_PPO/',
#     'log_level': 10,
#     'log_interval': 20000
# }
# config = EasyDict(myconfig)
#
# from pathlib import Path
#
#
# def agent_factory():
#     model = PPOModel(observation_shape,
#                      action_shape,
#                      recurrent=True,
#                      discrete=True,
#                      reorder=reorder,
#                      optimizer='torch.optim.RMSprop',
#                      high=high)
#     train_interval = 128
#     num_env = n_env
#     epoch = 4
#     batch_size = 512
#     project_dir = Path(__file__).absolute().parent
#     model_dir = os.path.join(project_dir, 'ckpt/5000k/PPOModel.pt')
#     model.load(model_dir)
#     agent = PPOAgent(model,
#                      train_interval=train_interval,
#                      n_env=n_env,
#                      batch_size=batch_size,
#                      num_epochs=epoch,
#                      buffer_kwargs={'size': train_interval,
#                                     'n_env': num_env})
#
#     return agent
import os
from pathlib import Path

from rl2.agents.ppo import PPOModel, PPOAgent


def agent_factory():
    config = dict(
        batch_size=512,
        epoch=4,
        train_interval=128,
        log_level=10,
        log_interval=5e4,
        save_interval=1e2,
        lr=1e-4,
        gamma=0.99,
        grad_clip=10,
    )

    from marlenv.wrappers import make_snake
    env_config = dict(
        num_snakes=1,
        n_env=1,
        height=20,
        width=20,
        frame_stack=2,
        vision_range=5,
    )
    env, obs_shape, ac_shape, props = make_snake(**env_config)

    model = PPOModel(
        obs_shape,
        ac_shape,
        recurrent=False,
        discrete=True,
        reorder=props['reorder'],
        optimizer='torch.optim.RMSprop',
        high=props['high']
    )
    project_dir = Path(__file__).absolute().parent
    model_dir = os.path.join(project_dir, 'ckpt/agent0/1k/PPOModel.pt')
    model.load(model_dir)
    print(model)

    agent = PPOAgent(
        model,
        train_interval=config['train_interval'],
        n_env=env_config['n_env'],
        batch_size=config['batch_size'],
        num_epochs=config['epoch'],
        buffer_kwargs={
            'size': config['train_interval'],
            'n_env': env_config['n_env'],
        }
    )

    return agent