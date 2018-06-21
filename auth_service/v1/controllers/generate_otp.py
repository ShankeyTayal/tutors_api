from utils.otp_utils import get_client_ip, get_random_otp
from flask import request
from models.auth import User, AuthOtp
from sqlalchemy.orm.exc import MultipleResultsFound
from utils.errors import APIException
import datetime
from auth_service.services.sms import send_sms
from threading import Thread

MAX_OTP_COUNT = 5

OTP_EXPIRY_TIME = 3 * 60  # 3 mins
REQUEST_OTP_DELAY = 15 * 60  # 15 mins

MAX_RETRY_TEXT = "Max OTP limit has been reached."
USER_BLOCKED_TEXT = "This user is blocked."
MAX_OTP_REACHED_TEXT = ("You have reached to max otp request."
                        "Please retry after 15 minutes")
SENT_OTP_TEXT = "Verification code has been sent"
OTP_SMS = "OTP is {otp} to verify on Tutors"


class GenerateOTPController(object):
    def __init__(self, data, metadata=None):
        self.phone = data.get('phone')
        self.login_type = data.get('login_type')
        self.sign_up_ip = metadata.get('sign_up_ip')
        self.x_real_ip = metadata.get('x_real_ip')

    def send_otp(self):
        sms_text = OTP_SMS.format(otp=self.otp)
        # Async operation to send sms
        t = Thread(target=send_sms,
                   args=(self.phone, sms_text,)
                   )
        t.start()

    def is_valid_otp_request(self):
        if self.otp_obj.otp_counter < MAX_OTP_COUNT:
            return True
        now = datetime.datetime.now(datetime.timezone.utc)
        if (now - self.otp_obj.created_ts).total_seconds() < REQUEST_OTP_DELAY:
            self.message = MAX_OTP_REACHED_TEXT
            return False
        self.otp_obj.update_otp_obj(is_active=False)
        self.otp_obj = AuthOtp.create_otp_obj({'user_id': self.user.id,
                                               'is_active': True},
                                              self.sign_up_ip)
        return True

    def generate_otp(self):
        # Block users marked as blocked
        try:
            self.user = User.get_or_create(
                {'phone': self.phone, 'login_type': str(self.login_type)})
        except MultipleResultsFound as error:
            APIException(500, str(error))

        if self.user and self.user.blocked:
            self.message = USER_BLOCKED_TEXT
            return False

        self.otp_obj = AuthOtp.get_or_create({'user_id': self.user.id,
                                              'is_active': True},
                                             self.sign_up_ip)

        if not self.is_valid_otp_request():
            return False

        self.otp = get_random_otp()
        self.otp_obj.update_otp_obj(otp=self.otp,
                                    otp_counter=self.otp_obj.otp_counter + 1,
                                    retry_counter=0,
                                    expiry=(datetime.datetime.now() +
                                            datetime.timedelta(
                                                seconds=OTP_EXPIRY_TIME))
                                    )
        return True

    def accounts_login(self):
        self.message = None
        success = self.generate_otp()

        if not success:
            return False, self.message

        self.send_otp()

        return True, SENT_OTP_TEXT

    def _write(self):
        self.sign_up_ip = get_client_ip(self.sign_up_ip, self.x_real_ip)
        try:
            return self.accounts_login()
        except Exception as err:
            request.logger.exception("Unexpected error while trying to login",
                                     phone=self.phone,
                                     error_message=str(err),
                                     )
            return False, "Something went wrong"

    def serialize(self, success, message):
        resp = {
            'success': success,
            'message': message,
        }
        return resp

    def status(self, success):
        return (201 if success else 200)
