import os

import docker

from support.validations import local_rollout, remote_rollout

tag = 'test_repo/test_agent'
checkpoint_dir = './src/ckpt'

# def build_image():
#     client = docker.from_env()
#     # dockerfile_dir = './Dockerfile'
#     # print(os.getcwd())
#     # dockerfile_dir = os.path.abspath(dockerfile_dir)
#     # print(dockerfile_dir)
#     # with open(dockerfile_dir, 'rb') as fp:
#     image = client.images.build(
#         path='.', tag=tag, rm=True
#     )
#     return image


def test_local():
    local_rollout()


def test_remote():
    # TODO: manually build/rmi for now(by Docker CLI)

    r = remote_rollout(tag, os.path.abspath(checkpoint_dir))

    assert r.ok
