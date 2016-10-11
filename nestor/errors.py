HTTP_BAD_REQUEST = 400

class InvalidAttribute(Exception):
    def unpack(self):
        return str(self), HTTP_BAD_REQUEST

class MissingAttribute(Exception):
    pass
