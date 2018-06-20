import logging
import secrets


class Config(object):
    LOGGING_FORMAT = (
        '[%(asctime)s] [%(levelname)-8s] [%(name)s:%(lineno)s] -- %(message)s'
    )
    LOGGING_LOCATION = './logfile.log'
    LOGGING_LEVEL = logging.CRITICAL

    DEFAULT_DB_URI = "postgresql://%s:%s@%s:%s/%s" % (
        secrets.db["default"]['user'],
        secrets.db["default"]['password'],
        secrets.db["default"]['host'],
        secrets.db["default"]['port'],
        secrets.db["default"]['name'],
    )
    SQLALCHEMY_DATABASE_URI = DEFAULT_DB_URI

    SQLALCHEMY_BINDS = {
        'default': DEFAULT_DB_URI
    }
