from flask import make_response, request
import flask_restful as restful
import json
from ..schema import GenerateTokenSchema, OTPHeadersSchema
from utils.schema_utils import SchemaValidatorMixin
from ..controllers.generate_token import GenerateTokenController


class GenerateToken(SchemaValidatorMixin, restful.Resource):
    schema_validator_class = OTPHeadersSchema
    controller_class = GenerateTokenController

    def post(self):
        body_schema = GenerateTokenSchema(strict=True)
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
