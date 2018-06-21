from flask import make_response, current_app
import flask_restful as restful
import json
from models import db


class HealthCheck(restful.Resource):

    @staticmethod
    def check_database():
        try:
            binds = current_app.config['SQLALCHEMY_BINDS'].keys()
            for bind in binds:
                engine = db.get_engine(current_app, bind)
                engine.connect()
            return True
        except:
            return False

    def get(self):
        if self.check_database():
            return make_response(
                json.dumps(
                    {'message': 'I am good. How are you?.'}
                ), 200,
                {'Content-Type': 'application/json'}
            )
        else:
            return make_response(
                json.dumps(
                    {'message': 'Health check failed!'}
                ), 503,
                {'Content-Type': 'application/json'}
            )
