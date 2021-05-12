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
    client = docker.from_env()
    # try:
    #     img = client.images.get(tag)
    #     print('image'*100)
    # except docker.errors.NotFound as e:
    #     print('no such image'*100)
    # img = build_image()
    # TODO: manually build/rmi for now(by Docker CLI)

    print('before'*100)
    r = remote_rollout(tag, os.path.abspath(checkpoint_dir))
    print('after' * 100)
    assert r.ok

    # img.remove(force=True)
