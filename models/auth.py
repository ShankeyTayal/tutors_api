from . import db
import datetime
import enum


class LoginType(enum.Enum):
    student = '1'
    tutor = '2'

    @staticmethod
    def members():
        return [e.value for e in LoginType]


class User(db.Model):

    __bind_key__ = 'default'
    __tablename__ = 'user'

    id = db.Column(db.Integer(), primary_key=True)
    phone = db.Column(db.String(length=10), nullable=False)
    login_type = db.Column(db.Enum(*LoginType.members(),
                                   name="login_type"), nullable=False)
    blocked = db.Column(db.Boolean(), default=False)
    created_ts = db.Column(db.DateTime(), default=datetime.datetime.now)
    update_ts = db.Column(db.DateTime(), default=datetime.datetime.now,
                          onupdate=datetime.datetime.now)

    __table_args__ = (
        db.UniqueConstraint('phone', 'login_type',
                            name='user_phone_login_type_key'),
    )

    @staticmethod
    def get_user_properties(conditions_dict):
        return User.query.filter_by(**conditions_dict).one_or_none()

    @staticmethod
    def get_or_create(conditions_dict):
        instance = User.get_user_properties(conditions_dict)
        if instance:
            return instance
        else:
            instance = User(**conditions_dict)
            db.session.add(instance)
            db.session.commit()
            return instance


# class AuthOtpStatus(enum.Enum):
#     otp_generated = 'OTP_GENERATED'
#     otp_sent = 'OTP_SENT'
#     otp_sending_failed = 'OTP_SENDING_FAILED'
#     otp_verified = 'OTP_VERIFIED'
#     otp_timed_out = 'OTP_TIMED_OUT'
#     otp_auth_failed = 'OTP_AUTH_FAILED'

#     @staticmethod
#     def members():
#         return [e.value for e in AuthOtpStatus]


class AuthOtp(db.Model):

    __bind_key__ = 'default'
    __tablename__ = 'auth_otp'

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.BigInteger, index=True)
    retry_counter = db.Column(db.Integer(), default=0)
    otp_counter = db.Column(db.Integer(), default=0)
    otp = db.Column(db.Text())
    created_ts = db.Column(db.DateTime(), default=datetime.datetime.now)
    update_ts = db.Column(db.DateTime(), default=datetime.datetime.now,
                          onupdate=datetime.datetime.now)
    expiry = db.Column(db.DateTime())
    # status = db.Column(db.Enum(*AuthOtpStatus.members(),
    #                            name="otp_status_type"), nullable=False)
    login_ip = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)

    @staticmethod
    def get_auth_otp_obj(conditions_dict):
        return AuthOtp.query.filter_by(**conditions_dict).first()

    @staticmethod
    def create_otp_obj(conditions_dict, login_ip=None):
        instance = AuthOtp(**conditions_dict)
        instance.login_ip = login_ip
        db.session.add(instance)
        db.session.commit()
        return instance

    @staticmethod
    def get_or_create(conditions_dict, login_ip=None):
        instance = AuthOtp.get_auth_otp_obj(conditions_dict)
        if instance:
            return instance
        else:
            return AuthOtp.create_otp_obj(conditions_dict, login_ip)

    def update_otp_obj(self, *args, **kwargs):
        """
            Update otp properties
        """
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.add(self)
        db.session.commit()
