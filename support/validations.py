import json
import os
from time import sleep

import docker
import requests
from marlenv.envs.snake_env import SnakeEnv
from marlenv.wrappers import make_snake

from support.utils import find_agent_module, NumpyEncoder

action_list = list(SnakeEnv.default_action_dict.values())

VISION_RANGE = 5
FRAME_STACK = 2


# def build_image():
#     client = docker.from_env()
#     tag = 'test_repo/test_agent'
#     # dockerfile_dir = './Dockerfile'
#     # print(os.getcwd())
#     # dockerfile_dir = os.path.abspath(dockerfile_dir)
#     # print(dockerfile_dir)
#     # with open(dockerfile_dir, 'rb') as fp:
#     image = client.images.build(
#         path='..', tag=tag, rm=True
#     )
# client = docker.from_env()
# tag = 'test_repo/test_agent'
#
# image = client.images.build(
#     path='..', tag=tag, rm=True
# )

def dummy_env():
    _, _, _, props = make_snake(
        n_env=1, num_snakes=1, vision_range=5, frame_stack=2
    )

    return props


def sample_request(url='http://localhost:5000/act'):
    props = dummy_env()
    obs = props['high']

    print('sending request')
    r = requests.post(
        url, json=json.dumps(obs, cls=NumpyEncoder)
    )

    return r

def remote_rollout(image_name, checkpoint_dir):
    port = 5000
    container_name = 'test_agent'

    # checkpoint_dir = '../src/ckpt'
    # checkpoint_dir = os.path.abspath(checkpoint_dir)
    print('*'*100, checkpoint_dir)

    client = docker.from_env()
    # try:
    #     img = client.images.get(image_name)
    # except docker.errors.NotFound:
    #     build_image()

    try:
        cont = client.containers.get(container_name)
        cont.remove(force=True)
    except docker.errors.NotFound as e:
        pass
    finally:
        print('running server')
        cont = client.containers.run(
            image_name,
            detach=True,
            name=container_name,
            ports={f'{port}/tcp': port},
            # auto_remove=True,
            volumes={
                checkpoint_dir: {'bind': '/agent/ckpt', 'mode': 'rw'}
            },
            environment=['FLASK_APP=support/server', 'FLASK_ENV=development'],
            command=f'flask run --port {port} --host=0.0.0.0',
        )
    sleep(10)
    r = sample_request()
    # img.remove(force=True)

    return r


def local_rollout():
    algo = find_agent_module()
    agent = algo.agent_factory()
    props = dummy_env()
    sample_obs = props['high']
    ac = agent.act(sample_obs)
