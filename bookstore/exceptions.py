class ExceptionBase(Exception):
    def __init__(self, status_code: int, details: str):
        self.status_code = status_code
        self.details = details


class BadRequestError(ExceptionBase):
    def __init__(self, details: str):
        super().__init__(
            status_code=400,
            details=details
        )
