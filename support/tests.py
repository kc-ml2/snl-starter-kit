import json
import os
import socket
from pathlib import Path

import docker
import pytest
import requests
from marlenv.envs.snake_env import SnakeEnv
from marlenv.wrappers import make_snake

from support.utils import NumpyEncoder, find_algo_module

VISION_RANGE = 5
FRAME_STACK = 2
ACTIONS = list(SnakeEnv.default_action_dict.values())


def dummy_env():
    _, _, _, props = make_snake(
        n_env=1, num_snakes=1, vision_range=VISION_RANGE,
        frame_stack=FRAME_STACK
    )

    return props


# @pytest.fixture
# def agent_image():
#     client = docker.from_env()
#
#     repotag = 'test-repo/test-image'
#     base_dir = Path(__file__).absolute().parent.parent
#     dockerfile_dir = os.path.join(base_dir, 'Dockerfile')
#     assert os.path.exists(dockerfile_dir)
#     image, logs = client.images.build(path='.', tag=repotag, rm=True)
#
#     yield image
#     client.images.remove(image.id, force=True)


# @pytest.fixture
# def agent_container(agent_image):
#     container_name = 'test-container'
#
#     # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     # s.bind(('', 0))
#     # port = s.getsockname()[1]
#
#     client = docker.from_env()
#     try:
#         container = client.containers.get(container_name)
#     except docker.errors.NotFound as e:
#         container = client.containers.run(
#             agent_image.id,
#             detach=True,
#             name=container_name,
#             ports={f'5000/tcp': 30000},
#             # auto_remove=True,
#         )
#
#     yield container
    # s.close()
    # container.remove(force=True)


def test_local():
    algo = find_algo_module('example.multippo.algo')
    agent = algo.agent_factory()
    props = dummy_env()
    sample_obs = props['high']
    ac = agent.act(sample_obs)
    assert ac in ACTIONS


def sample_request(url=f'http://localhost:30000/act'):
    props = dummy_env()
    obs = props['high']

    print('sending request')
    r = requests.post(url, json=json.dumps(obs, cls=NumpyEncoder))

    return r


def test_remote():
    repotag = 'test-repo/test-image'
    url = f'http://localhost:30000/act'
    base_dir = Path(__file__).absolute().parent.parent
    dockerfile_dir = os.path.join(base_dir, 'Dockerfile')
    assert os.path.exists(dockerfile_dir)

    client = docker.from_env()
    image, logs = client.images.build(path='.', tag=repotag, rm=True)

    # try:
    container = client.containers.run(
        image.id,
        detach=True,
        ports={f'5000/tcp': 30000},
        auto_remove=True
    )
    r = sample_request(url)
    assert r.ok
    # except Exception as e:
    #     pass
    # finally:
    # container.remove(force=True)
    image.remove(force=True)
