class StpmexException(Exception):
    pass


class InvalidPassphrase(StpmexException):
    """El passphrase es incorrecto"""
