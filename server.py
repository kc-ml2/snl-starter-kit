import json

import numpy as np
from flask import Flask, request, make_response, current_app, jsonify


class AgentServer(Flask):
    """
    minimal stateful server
    """

    def __init__(self, agent):
        super(AgentServer, self).__init__(__name__)
        self.agent = agent


from src import algo
assert hasattr(algo, 'agent_factory') and callable(algo.agent_factory), ("'agent_factory' method must be defined in algo.py and callable")

agent_ = algo.agent_factory()
assert hasattr(agent_, 'act') and callable(agent_.act), ("agent missing 'act' method")

app = AgentServer(agent_)


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


@app.route('/act', methods=['POST'])
def act():
    agent = current_app.agent
    obs = json.loads(request.json)
    obs = np.asarray(obs)
    action = agent.act(obs)

    dumped = json.dumps(action, cls=NumpyEncoder)
    return dumped


if __name__ == '__main__':
    app.run(host='0.0.0.0')
