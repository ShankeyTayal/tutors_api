from marshmallow import Schema, fields, validate
from constants import OTP_LENGTH


class BaseOTPSchema(Schema):
    phone = fields.String(required=True, validate=validate.Length(equal=10))
    login_type = fields.Int(required=True,
                            validate=validate.Range(min=1, max=2))


class GenerateOTPSchema(BaseOTPSchema):
    pass


class OTPHeadersSchema(Schema):
    sign_up_ip = fields.String(required=False, load_from='X-Forwarded-For',
                               dump_to='sign_up_ip')
    x_real_ip = fields.String(required=False, load_from='X-Real-Ip',
                              dump_to='x_real_ip')


class GenerateTokenSchema(BaseOTPSchema):
    otp = fields.String(required=True,
                        validate=validate.Length(equal=OTP_LENGTH))


class LogoutHeadersSchema(Schema):
    pass


class LogoutSchema(Schema):
    access_token = fields.String(required=True,
                                 validate=validate.Length(equal=64))
