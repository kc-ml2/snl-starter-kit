import json

import numpy as np
from flask import Flask, request, logging, jsonify

from support.utils import find_algo_module, NumpyEncoder, NumpyDecoder


class AgentServer(Flask):
    """
    minimal stateful server
    """

    def __init__(self, agent, import_name=__name__, **kwargs):
        super().__init__(import_name, **kwargs)
        self.json_encoder = NumpyEncoder
        # self.json_decoder = NumpyDecoder
        self.agent = agent
        self.add_url_rule(
            rule='/act',
            endpoint='act',
            view_func=self.act_view,
            methods=['POST'],
        )
        self.add_url_rule(
            rule='/ping',
            endpoint='ping',
            view_func=self.ping_view,
            methods=['GET'],
        )

        self.logger = logging.create_logger(self)

    def ping_view(self):
        return '{}'

    def act_view(self):
        obs = json.loads(request.get_json())

        self.logger.debug('got request: ' + str(obs))

        obs = np.asarray(obs)
        action = self.agent.act(obs)

        self.logger.debug('action: ' + str(action))

        return jsonify(action)


def create_app():
    algo = find_algo_module()
    agent = algo.agent_factory()

    app = AgentServer(agent)

    return app
