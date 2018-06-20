from flask import Flask
from auth_service.v1.urls import auth_service_blueprint
from logging import handlers, Formatter
from structlog import configure, processors
from structlog.threadlocal import wrap_dict
from . import config
from models import db


def logging_setup(app):
    # Add file handler

    file_handler = handlers.RotatingFileHandler(
        app.config['LOGGING_LOCATION'],
        maxBytes=4 * 1024 * 1024,  # 4 MB
        backupCount=10
    )
    file_handler.setLevel(app.config['LOGGING_LEVEL'])
    file_handler_formatter = Formatter(app.config['LOGGING_FORMAT'])
    file_handler.setFormatter(file_handler_formatter)
    app.logger.addHandler(file_handler)

    # Configure structlog
    configure(
        context_class=wrap_dict(dict),
        logger_factory=lambda: app.logger,
        processors=[processors.JSONRenderer()]
    )


def create_app():
    app = Flask(__name__)
    app.config.from_object(config.Config)
    app.register_blueprint(auth_service_blueprint, url_prefix='/v1/auth')
    db.init_app(app)
    logging_setup(app)
    return app
