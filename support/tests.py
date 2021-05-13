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


@pytest.fixture
def agent_image():
    client = docker.from_env()

    repotag = 'test-repo/test-image'
    base_dir = Path(__file__).absolute().parent.parent
    dockerfile_dir = os.path.join(base_dir, 'Dockerfile')
    assert os.path.exists(dockerfile_dir)
    image, logs = client.images.build(path='.', tag=repotag, rm=True)

    yield image

    for c in image.attrs['Container']:
        c_ = client.containers.get(c)
        c_.kill(force=True)
    client.images.remove(image.id, force=True)


def server_alive(url, interval=1):
    cnt = 1
    limit = 60
    endpoint = '/ping'
    url = url + endpoint
    while True:
        if cnt % 10 == 0:
            print(f'pinging {cnt} times...')
        if cnt == limit:
            return False
        r = requests.get(url)

        if r.ok:
            break
        sleep(interval)
        cnt += 1

    return True


@pytest.fixture
def agent_container(agent_image):
    container_name = 'test-container'

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 0))
    port = s.getsockname()[1]

    client = docker.from_env()
    try:
        container = client.containers.get(container_name)
    except docker.errors.NotFound as e:
        container = client.containers.run(
            agent_image.id,
            detach=True,
            name=container_name,
            ports={f'5000/tcp': port},
            # auto_remove=True,
        )
    if server_alive(f'http://localhost:{port}') is False:
        s.close()
        container.remove(force=True)
        raise RuntimeError('running agent server failed')
    print(id(container), '*'*100)
    yield container

    s.close()
    container.remove(force=True)


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


def test_remote(agent_container):
    print(id(agent_container), '*' * 100)
    port = agent_container.ports['5000/tcp'][0]['HostPort']
    url = f'http://localhost:{port}/act'

    r = sample_request(url)
    assert r.ok
