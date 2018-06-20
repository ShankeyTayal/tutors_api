from flask import request, make_response
import json
from models import db
from marshmallow import ValidationError
from .errors import APIException


class MultiItemTypeDict(dict):

    def __init__(self, dicts, *args, **kwargs):
        self.__dicts = dicts
        for d in dicts:
            for k, v in d.iteritems():
                self.__setitem__(k, v)
        super(MultiItemTypeDict, self).__init__(*args, **kwargs)

    def __getattr__(self, name):
        """
        Here we try to see if there is any child dictionary specific attribute
        like getlist and delegate its access to the child dictionary class

        """
        try:
            super(MultiItemTypeDict, self).__getattr__(name)
        except:
            for _dict in self.__dicts:
                if hasattr(_dict, name):
                    return getattr(_dict, name)
        raise AttributeError

    def __getitem__(self, key):
        for _dict in self.__dicts:
            if key in _dict:
                return _dict.__getitem__(key)
        return super(MultiItemTypeDict, self).__getitem__()


class SchemaValidatorMixin(object):
    __schema_args_source__ = ['request_headers']

    def merge_dicts(self, dicts):
        """
        We need MultiItemTypeDict dict here so that we can delegate the
        get access to their respective classes. E.g getlist is only available
        with werkzeug.datastructures.MultiDict
        """
        super_dict = MultiItemTypeDict(dicts)
        return super_dict

    def get_request_headers(self):
        return request.headers

    def get_request_args(self):
        return request.args

    def get_request_data_dict(self):
        """
        This function returns the data to be fed to the Schemavalidator.
        By default it receives value from request.headers. Another source
        could be request.args. To change the default data source we need to
        modify __schema_args_source__ variable. For each item in
        __schema_args_source__ a "get_(item_name)" method needs to be present
        in the class. If more than one data source is present it merges both
        into a single MultiItemTypeDict dictionary using merge_dicts method

        """
        len_arg_data_prop = len(self.__schema_args_source__)

        """
        Next check shouldn't be required ideally since Multidict is taking
        care of the item access. However its safer to use the original object
        if there is just one type of dictionary

        """
        if len_arg_data_prop == 1:
            func = getattr(self, "get_%s" % self.__schema_args_source__[0])
            request_data = func()
        elif len_arg_data_prop > 1:
            dicts = []
            for fname in self.__schema_args_source__:
                func = getattr(self, "get_%s" % fname)
                _dict = func()
                dicts.append(_dict)
            request_data = self.merge_dicts(dicts)
        else:
            request_data = {}
        return request_data

    def __init__(self, *args, **kwargs):
        self.schema = self.schema_validator_class(strict=True)
        request_data = self.get_request_data_dict()
        self.schema.validate(request_data)
        result = self.schema.dump(request_data)
        self.metadata = result.data
        super(SchemaValidatorMixin, self).__init__(*args, **kwargs)

    def dispatch_request(self, *args, **kwargs):
        IGNORE_EXCEPTION = [404]
        try:
            return super(SchemaValidatorMixin,
                         self).dispatch_request(*args, **kwargs)
        except APIException as exc:
            if exc.status_code not in IGNORE_EXCEPTION:
                db.session.rollback()
                request.logger.exception('API Exception',
                                         message=str(exc),
                                         exc=exc,
                                         status=exc.status_code
                                         )
            return make_response(
                json.dumps(exc.message), exc.status_code,
                {'Content-Type': 'application/json'}
            )
        except ValidationError as error:
            db.session.rollback()
            request.logger.exception(str(error),
                                     message=str(error),
                                     error=error,
                                     status=400
                                     )
            return make_response(
                json.dumps({'message': error.message}), 400,
                {'Content-Type': 'application/json'}
            )
        except Exception as error:
            db.session.rollback()
            request.logger.exception(str(error),
                                     message=str(error),
                                     error=error,
                                     status=500
                                     )
            return make_response(
                json.dumps({'message': 'Internal server error'}), 500,
                {'Content-Type': 'application/json'}
            )
        finally:
            db.session.close()
