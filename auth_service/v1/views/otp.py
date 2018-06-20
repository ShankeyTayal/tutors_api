from flask import make_response, request
import flask_restful as restful
import json
from ..schema import GenerateOTPSchema, OTPHeadersSchema
from utils.schema_utils import SchemaValidatorMixin
from ..controllers.generate_otp import GenerateOTPController


class GenerateOTP(SchemaValidatorMixin, restful.Resource):
    schema_validator_class = OTPHeadersSchema
    controller_class = GenerateOTPController

    def post(self):
        body_schema = GenerateOTPSchema(strict=True)
        request_data = request.json if request.json else {}
        body_schema.validate(request_data)
        data = body_schema.dump(request.json).data
        controller = self.controller_class(data=data, metadata=self.metadata)
        succcess, message = controller._write()
        return make_response(
            json.dumps(controller.serialize(succcess, message)), 200,
            {'Content-Type': 'application/json'}
        )
