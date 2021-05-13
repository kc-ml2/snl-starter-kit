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