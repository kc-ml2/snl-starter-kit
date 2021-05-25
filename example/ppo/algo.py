import json
import os
from pathlib import Path

from easydict import EasyDict
from marlenv.wrappers import make_snake
from rl2.agents.ppo import PPOModel, PPOAgent
from rl2.examples.temp_logger import Logger


def ppo(obs_shape, ac_shape, config, props, load_dir=None):
    model = PPOModel(
        obs_shape,
        ac_shape,
        recurrent=config.recurrent,
        discrete=True,
        reorder=props.reorder,
        optimizer=config.optimizer,
        high=props.high
    )
    if load_dir is not None:
        model.load(load_dir)
    agent = PPOAgent(
        model,
        train_interval=config.train_interval,
        n_env=props.n_env,
        batch_size=config.batch_size,
        num_epochs=config.epoch,
        buffer_kwargs={
            'size': config.train_interval,
            'n_env': props.n_env}
    )
    return agent


def agent_factory():
    config = {
        'n_env': 64,
        'num_snakes': 1,
        'width': 20,
        'height': 20,
        'vision_range': 5,
        'frame_stack': 2,
        'train_interval': 128,
        'epoch': 4,
        'batch_size': 512,
        'max_step': int(5e6),
        'optimizer': 'torch.optim.RMSprop',
        'recurrent': True,
        'log_interval': 20000,
        'log_level': 10,
        'save_interval': 1000000,
        'tag': 'PPO',
    }
    config = EasyDict(config)
    base_dir = Path(__file__).absolute().parent
    model_file = os.path.join(base_dir, "ckpt", "5000k", "PPOModel.pt")

    env, observation_shape, action_shape, props = make_snake(
        n_env=1,
        num_snakes=config.num_snakes,
        width=config.width,
        height=config.height,
        vision_range=config.vision_range,
        frame_stack=config.frame_stack
    )
    agent = ppo(
        observation_shape,
        action_shape,
        config,
        props,
        load_dir=model_file
    )
    return agent