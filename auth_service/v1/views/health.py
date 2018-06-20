from flask import make_response
import flask_restful as restful
import json


class HealthCheck(restful.Resource):

    def get(self):
        message = {"message": 'I am good. How are you?'}
        return make_response(json.dumps(message),
                             200,
                             {'Content-Type': 'application/json'}
                             )
