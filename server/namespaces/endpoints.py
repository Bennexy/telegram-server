import sys
import json
import requests
from flask_restx import Namespace, Resource, fields
from flask import jsonify, request


sys.path.append('.')

from server.config import ServerUrl

from server import api

from server.logger import get_logger

logger = get_logger('telegram-server-process')

namespace = Namespace("TelegramServerProcess", description="Process requests")

parser_in = api.parser()
parser_out = api.parser()

@namespace.route("input/")
@namespace.expect(parser_in)
class MyApi(Resource):
    def post(self):
        logger.debug(f'got post request')

        payload = request.json

        logger.debug(f'payload recieved: {payload}')

        data = payload['payload']
        
        return jsonify(message="corona server has recieved request and payload")

