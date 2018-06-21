from models.auth import User, AuthOtp, AccessToken
from models.student import Student
from models.tutor import Tutor
from datetime import datetime, timezone
from utils.otp_utils import generate_access_token

MAX_RETRY_COUNT = 3

VERIFICATION_FAILED_TEXT = 'Verification Failed'
VERIFICATION_TEXT = 'Verified'


class GenerateTokenController(object):

    def __init__(self, data, metadata):
        self.phone = data.get('phone')
        self.login_type = data.get('login_type')
        self.otp = data.get('otp')

    def is_valid_otp(self):
        condition_dict = {
            "user_id": self.user.id,
            "is_active": True
        }
        self.otp_obj = AuthOtp.get_auth_otp_obj(condition_dict)
        if self.otp_obj:
            self.otp_obj.update_otp_obj(
                retry_counter=self.otp_obj.retry_counter + 1
            )
            if (self.otp_obj.otp == self.otp and
                    self.otp_obj.retry_counter < MAX_RETRY_COUNT and
                    datetime.now(timezone.utc) < self.otp_obj.expiry):
                    return True
        return False

    def _write(self):
        self.user = User.get_user_properties(
            {'phone': self.phone, 'login_type': str(self.login_type)})

        if not self.is_valid_otp():
            return False
        access_token = generate_access_token()
        self.token_obj = AccessToken.create_token_obj({'user_id': self.user.id,
                                                       'token': access_token,
                                                       })

        if self.login_type == 1:
            self.profile_obj = Student.get_or_create({"user_id": self.user.id})
        else:
            self.profile_obj = Tutor.get_or_create({"user_id": self.user.id})

        self.otp_obj.update_otp_obj(is_active=False)
        return True

    def serialize(self, success):
        resp = {
            'success': success,
            'message': None
        }
        if not success:
            resp['message'] = VERIFICATION_FAILED_TEXT
            return resp
        resp['message'] = VERIFICATION_TEXT
        resp['access_token'] = self.token_obj.token
        resp['login_type'] = self.login_type
        resp['profile_id'] = self.profile_obj.id
        return resp

    def status(self, success):
        return (201 if success else 200)
