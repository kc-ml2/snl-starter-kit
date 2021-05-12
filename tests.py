from support.validations import local_rollout, remote_rollout


def test_local():
    local_rollout()


def test_remote():
    r = remote_rollout()
    assert r.ok
