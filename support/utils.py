import json
from importlib import import_module
from time import sleep

import numpy as np
import requests


def find_algo_module(
        folder: str = 'src.algo',
        factory_name: str = 'agent_factory'
):
    module = import_module(folder)
    factory_method = getattr(module, factory_name)
    assert callable(factory_method)

    return module


class NumpyEncoder(json.JSONEncoder):
    """ Special json encoder for numpy types """
    """https://stackoverflow.com/questions/26646362/numpy-array-is-not-json-serializables"""

    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


class NumpyDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(
            self, object_hook=self.object_hook, *args, **kwargs
        )

    def object_hook(self, obj):
        if '_kind_' not in obj:
            return obj
        kind = obj['_kind_']
        if kind == 'ndarray':
            return np.array(obj['_value_'])
        elif kind == 'range':
            value = obj['_value_']
            return range(value[0], value[-1])

        return obj


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

        r = None
        try:
            r = requests.get(url)
        except:
            pass

        if r is not None and r.ok:
            break
        sleep(interval)
        cnt += 1

    return True
