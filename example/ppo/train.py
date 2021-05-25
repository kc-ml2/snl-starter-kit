from easydict import EasyDict
from marlenv.wrappers import make_snake
from rl2.examples.temp_logger import Logger
from rl2.workers import MaxStepWorker

from example.ppo.algo import ppo


def train(config):
    # Train phase
    logger = Logger(name='TUTORIAL', args=config)
    custom_reward = {
        'fruit': 1.0,
        'kill': 0.0,
        'lose': 0.0,
        'win': 0.0,
        'time': 0.0
    }
    env, observation_shape, action_shape, props = make_snake(
        n_env=config.n_env,
        num_snakes=config.num_snakes,
        width=config.width,
        height=config.height,
        vision_range=config.vision_range,
        frame_stack=config.frame_stack,
        reward_dict=custom_reward,
    )
    agent = ppo(observation_shape, action_shape, config, props)
    worker = MaxStepWorker(
        env, props.n_env, agent,
        max_steps=config.max_step,
        training=True,
        log_interval=config.log_interval,
        render=True,
        render_interval=500000,
        is_save=True,
        save_interval=config.save_interval,
        logger=logger
    )
    worker.run()
    return logger.log_dir


if __name__ == "__main__":
    # This can be replaced with argparser, click, etc.
    myconfig = {
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
        'recurrent': False,
        'log_interval': 20000,
        'log_level': 10,
        'save_interval': 1000000,
        'tag': 'PPO',
    }
    config = EasyDict(myconfig)

    log_dir = train(config)

