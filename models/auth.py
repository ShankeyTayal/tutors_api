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


class AccessToken(db.Model):

    __bind_key__ = 'default'
    __tablename__ = 'access_token'

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.BigInteger, nullable=False)
    token = db.Column(db.Text(), index=True)
    created_ts = db.Column(db.DateTime(), default=datetime.datetime.now)
    update_ts = db.Column(db.DateTime(), default=datetime.datetime.now,
                          onupdate=datetime.datetime.now)
    is_active = db.Column(db.Boolean, default=True)

    @staticmethod
    def get_token_obj(conditions_dict):
        return AccessToken.query.filter_by(**conditions_dict).one_or_none()

    @staticmethod
    def create_token_obj(conditions_dict):
        instance = AccessToken(**conditions_dict)
        db.session.add(instance)
        db.session.commit()
        return instance

    def update_token_obj(self, *args, **kwargs):
        """
            Update token properties
        """
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.add(self)
        db.session.commit()
