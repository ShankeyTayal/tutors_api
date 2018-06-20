from structlog import get_logger
from flask import request
from functools import wraps
import uuid
import datetime


def get_struct_logger():
    return get_logger().new()


def attach_logger(func):
    '''Attach structlog logger to the request instance.'''
    @wraps(func)
    def wrapped(*args, **kwargs):
        if not hasattr(request, 'logger'):
            request.logger = get_logger()
            request.logger = request.logger.new(
                request_id=str(uuid.uuid4()),
                timestamp=datetime.datetime.now().strftime('%s'),
                query_params_log=request.args,
                url=request.url,
                request_data="request_data: %s" % str(request.data),
                request_method=request.method,
                headers=dict(request.headers),
            )
        return func(*args, **kwargs)
    return wrapped
