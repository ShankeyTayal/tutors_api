from flask import make_response, request
import flask_restful as restful
import json
from ..schema import LogoutSchema, LogoutHeadersSchema
from utils.schema_utils import SchemaValidatorMixin, authorize
from ..controllers.logout_controller import LogoutController


class Logout(SchemaValidatorMixin, restful.Resource):
    decorators = [authorize()]
    schema_validator_class = LogoutHeadersSchema
    controller_class = LogoutController

    def post(self):
        body_schema = LogoutSchema(strict=True)
        request_data = request.json if request.json else {}
        body_schema.validate(request_data)
        data = body_schema.dump(request.json).data
        controller = self.controller_class(data=data, metadata=self.metadata)
        succcess = controller._write()
        return make_response(
            json.dumps(controller.serialize(succcess)),
            controller.status(succcess),
            {'Content-Type': 'application/json'}
        )
