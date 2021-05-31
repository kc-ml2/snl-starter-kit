import json
import os
import socket
from pathlib import Path
from time import sleep

import docker
import pytest
import requests
from marlenv.envs.snake_env import SnakeEnv
from marlenv.wrappers import make_snake

from support.utils import NumpyEncoder, find_algo_module, server_alive

VISION_RANGE = 5
FRAME_STACK = 2
ACTIONS = list(SnakeEnv.default_action_dict.values())


def dummy_env():
    env, _, _, props = make_snake(
        n_env=1, num_snakes=1, vision_range=VISION_RANGE,
        frame_stack=FRAME_STACK
    )
    obs = env.reset()

    return env, obs


def safe_rmi(client, image_id):
    image = client.images.get(image_id)
    for c in image.attrs['Container']:
        try:
            c_ = client.containers.get(c)
            c_.kill(force=True)
        except:
            pass
    client.images.remove(image_id, force=True)


@pytest.fixture
def agent_image():
    print('\nbuilding test image...')
    rmi = False

    client = docker.from_env()

    repotag = 'test-repo/test-image'
    base_dir = Path(__file__).absolute().parent.parent
    dockerfile_dir = os.path.join(base_dir, 'Dockerfile')
    assert os.path.exists(dockerfile_dir)
    image, logs = client.images.build(path='.', tag=repotag, rm=True)
    image_id = image.id

    yield image_id

    if rmi:
        safe_rmi(client, image_id)


@pytest.fixture
def agent_container(agent_image):
    print('\nrunning test container...')
    rm = True
    container_name = 'test-container'

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 0))
    port = s.getsockname()[1]

    client = docker.from_env()
    try:
        container = client.containers.get(container_name)
        container.remove(force=True)
    except docker.errors.NotFound as e:
        pass
    finally:
        container_id = client.containers.run(
            agent_image,
            detach=True,
            name=container_name,
            ports={f'5000/tcp': port},
            # auto_remove=True,
        ).id
        if not server_alive(f'http://localhost:{port}'):
            raise RuntimeError('running server failed')
    # container instance MUST be retrieved again by id
    # else, container instance is not updated and you won't be able to see port

    yield container_id

    s.close()
    if rm:
        container = client.containers.get(container_id)
        container.remove(force=True)


def test_local():
    print('\ntesting local rollout...')
    algo = find_algo_module()
    agent = algo.agent_factory()
    env, obs = dummy_env()
    ac = agent.act(obs)
    env.step(ac)


def sample_request(url, endpoint='/act'):
    env, obs = dummy_env()

    print('\nsending request')
    r = requests.post(
        url + endpoint,
        json=json.dumps(obs, cls=NumpyEncoder)
    )

    return r


def test_remote(agent_container):
    print('\ntesting remote rollout...')
    client = docker.from_env()
    container = client.containers.get(agent_container)
    port = container.ports['5000/tcp'][0]['HostPort']

    url = f'http://localhost:{port}'
    endpoint = '/act'

    r = sample_request(url, endpoint)
    assert r.ok
