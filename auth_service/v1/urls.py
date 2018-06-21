from flask import Blueprint
from flask_restful import Api
from .views.otp import GenerateOTP
from .views.token import GenerateToken
from .views.logout import Logout
from .views.health import HealthCheck
from utils.log_utils import attach_logger

# Create a auth service Flask blueprint
auth_service_blueprint = Blueprint('v1', __name__)

# Register the API (flask-restful) with auht_service blueprint
api = Api(auth_service_blueprint)


@auth_service_blueprint.before_request
@attach_logger
def before_each_request():
    pass


api.add_resource(HealthCheck, '/health')
api.add_resource(GenerateOTP, '/otp')
api.add_resource(GenerateToken, '/token')
api.add_resource(Logout, '/logout')
