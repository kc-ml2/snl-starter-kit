import json

import numpy as np
from flask import Flask, request, logging

from support.utils import find_agent_module, NumpyEncoder, NumpyDecoder


class AgentServer(Flask):
    """
    minimal stateful server
    """

    def __init__(self, agent, import_name=__name__, **kwargs):
        super().__init__(import_name, **kwargs)
        self.json_encoder = NumpyEncoder
        self.json_decoder = NumpyDecoder
        self.agent = agent
        self.add_url_rule(
            rule='/act',
            endpoint='act',
            view_func=self.act_view,
            methods=['POST'],
        )

        self.logger = logging.create_logger(self)

    def act_view(self):
        obs = json.loads(request.get_json())
        self.logger.debug('got request: ' + str(obs))
        obs = np.asarray(obs)
        action = self.agent.act(obs)
        self.logger.debug('action: ' + str(action))

        return action


def create_app():
    algo = find_agent_module()
    agent = algo.agent_factory()

    app = AgentServer(agent)

    return app
