class TinyHRError(Exception):
    DEFAULT_STATUS_CODE = 400

    def __init__(self, error, status_code=DEFAULT_STATUS_CODE):
        Exception.__init__(self)
        self.error = error
        self.status_code = status_code

    def serialize(self):
        return {"error": self.error}
