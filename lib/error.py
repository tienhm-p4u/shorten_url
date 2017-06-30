"""Definition of error

All error in this system should be define in here. Error must have its own
error message to represent about error cause, and should be map to a HTTP error
code to response.
"""


class BaseError(Exception):
    """
    BaseError class

    New error will be define here by extend this class, then add
    ERROR_STATUS_MAP from error to error's HTTP status code.

    Eg, create a BadRequest error:
        ```
        class BadRequest(BaseError):
            pass
        ```
        then add this `BadRequest: 400` to ERROR_STATUS_MAP
    """
    message = ""

    def __init__(self, message):
        """
        Set error message for debug or display purpose
        """
        self.message = message

    def to_dict(self):
        """
        Represent error to dict for display purpose
        """
        return {"message": self.message}


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
    """Raise when input URL is invalid"""

    def __init__(self, url):
        msg = "Your url <%s> is invalid" % url
        super(InvalidURL, self).__init__(msg)


class NotFound(BaseError):
    """Raise when URL hashid is not found"""

    def __init__(self, hashid):
        msg = "URL <%s> is not found" % hashid
        super(NotFound, self).__init__(msg)


ERROR_STATUS_MAP = {InvalidURL: 400, NotFound: 404}
