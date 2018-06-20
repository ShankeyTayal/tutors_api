from marshmallow import Schema, fields, validate


class GenerateOTPSchema(Schema):
    phone = fields.String(required=True, validate=validate.Length(equal=10))
    login_type = fields.Int(required=True,
                            validate=validate.Range(min=1, max=2))


class OTPHeadersSchema(Schema):
    sign_up_ip = fields.String(required=False, load_from='X-Forwarded-For',
                               dump_to='sign_up_ip')
    x_real_ip = fields.String(required=False, load_from='X-Real-Ip',
                              dump_to='x_real_ip')
