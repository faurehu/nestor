import json

HTTP_BAD_REQUEST = 400

class NestorException(Exception):
    def __init__(self, message, error_code):
        self.message = message
        self.error_code = error_code

    def unpack(self):
        payload = {'ok': False, 'error': self.message}
        return json.dumps(payload), self.error_code

class RouteException(NestorException):
    pass

class InvalidAttribute(Exception):
    pass

class MissingAttribute(Exception):
    pass
