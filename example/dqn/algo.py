import os
from pathlib import Path

from easydict import EasyDict
from marlenv.wrappers import make_snake
from rl2.agents.dqn import DQNModel, DQNAgent


def agent_factory():
    config = {"width": 20, "height": 20, "vision_range": 5, "frame_stack": 2,
              "buffer_size": 100000, "batch_size": 32, "num_epochs": 1, "max_step": 500000,
              "update_interval": 10000, "train_interval": 1, "log_interval": 20000, "save_interval": 100000,
              "optimizer": "torch.optim.Adam", "lr": 0.001, "recurrent": True,
              "gamma": 0.99, "eps": 0.001, "polyak": 0, "decay_step": 100000,
              "grad_clip": 10, "tag": "DDQN", "double": True, "log_level": 10, "log_dir": "./DQN"}
    config = EasyDict(config)
    env, obs_shape, ac_shape, props = make_snake(
        n_env=1,
        num_snakes=1,
        width=config.width,
        height=config.height,
        vision_range=config.vision_range,
        frame_stack=config.frame_stack
    )

    model = DQNModel(
        observation_shape=obs_shape,
        action_shape=ac_shape,
        double=config.double,
        recurrent=config.recurrent,
        optim=config.optimizer,
        lr=config.lr,
        grad_clip=config.grad_clip,
        polyak=config.polyak,
        reorder=True,
        discrete=props.discrete,
        high=props.high
    )
    project_dir = Path(__file__).absolute().parent
    model_dir = os.path.join(project_dir, 'ckpt/500k/DQNModel.pt')
    model.load(model_dir)

    agent = DQNAgent(
        model,
        update_interval=config.update_interval,
        train_interval=config.train_interval,
        num_epochs=config.num_epochs,
        buffer_size=config.buffer_size,
        batch_size=config.batch_size,
        decay_step=config.decay_step,
        eps=config.eps,
        gamma=config.gamma,
        log_interval=config.log_interval,
    )

    return agent
