class BaseError(Exception):
    message = ""

    def __init__(self, message):
        self.message = message

    def to_dict(self):
        return {
            "message": self.message
        }


def to_status_code(error: BaseError) -> int:
    """
    Get HTTP status code mapped with specified error
    :param error: error to get status code
    >>> assert to_status_code(InvalidURL("debug")) == 400
    >>> class InvalidErrorError(BaseError):
    ...     code = "InvalidError"
    ...     description = "This Error is invalid"
    >>> assert to_status_code(InvalidErrorError("debug")) == 500
    """
    return ERROR_STATUS_MAP.get(error.__class__, 500)


class InvalidURL(BaseError):
    def __init__(self, url):
        msg = "Your url <%s> is invalid" % url
        super(InvalidURL, self).__init__(msg)


class NotFound(BaseError):
    def __init__(self, hashid):
        msg = "URL <%s> is not found" % hashid
        super(NotFound, self).__init__(msg)


ERROR_STATUS_MAP = {
    InvalidURL: 400,
    NotFound: 404
}
