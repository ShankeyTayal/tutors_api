from . import db
import datetime


class Tutor(db.Model):

    __bind_key__ = 'default'
    __tablename__ = 'tutor'

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.BigInteger, nullable=False)
    created_ts = db.Column(db.DateTime(), default=datetime.datetime.now)
    update_ts = db.Column(db.DateTime(), default=datetime.datetime.now,
                          onupdate=datetime.datetime.now)
    @staticmethod
    def get_tutor_properties(conditions_dict):
        return Tutor.query.filter_by(**conditions_dict).one_or_none()

    @staticmethod
    def get_or_create(conditions_dict):
        instance = Tutor.get_tutor_properties(conditions_dict)
        if instance:
            return instance
        else:
            instance = Tutor(**conditions_dict)
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
