import json

import numpy as np
from flask import Flask, request, make_response, current_app


class AgentServer(Flask):
    """
    minimal stateful server
    """
    def __init__(self, agent):
        super(AgentServer, self).__init__(__name__)
        self.agent = agent


from src import algo

assert hasattr(algo, 'agent_factory'), ("'agent_factory' method "
                                        "must be defined in algo.py")
assert callable(algo.agent_factory), "agent_factory must be callable"

agent_ = algo.agent_factory()
app = AgentServer(agent_)


@app.route('/act', methods=['POST'])
def act():
    agent = current_app.agent
    obs = request.json['obs']

    action = agent.act(obs)

    # possibility of other type? e.g. np.niter
    if isinstance(action, np.ndarray):
        action = action.tolist()

    res = make_response({'ac': action})

    return res, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0')
