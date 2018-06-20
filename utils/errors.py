class APIException(Exception):
    def __init__(self, status_code, *args, **kwargs):
        self.status_code = status_code
        super(APIException, self).__init__(*args, **kwargs)
