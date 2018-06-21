from models.auth import AccessToken

LOGOUT_FAILED_TEXT = 'Logout Failed'
LOGOUT_TEXT = 'Logged out successfully'


class LogoutController(object):
    def __init__(self, data, metadata=None):
        self.access_token = data.get('access_token')

    def _write(self):
        token_obj = AccessToken.get_token_obj({"token": self.access_token,
                                               "is_active": True})
        if token_obj:
            token_obj.update_token_obj(is_active=False)
        return True

    def serialize(self, success):
        resp = {
            'success': success,
            'message': None
        }
        if not success:
            resp['message'] = LOGOUT_FAILED_TEXT
            return resp
        resp['message'] = LOGOUT_TEXT
        return resp

    def status(self, success):
        return 200
