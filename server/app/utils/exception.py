class BusinessException(Exception):
    def __init__(self, message):
        super().__init__(message)


class CredentialsException(Exception):
    def __init__(self, message):
        super().__init__(message)
