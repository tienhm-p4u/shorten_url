import re


def is_valid_url(url):
    """
    Check if url is valid or not
    :param url: url to validate
    :return: bool

    >>> assert is_valid_url("http://youtube.com")
    >>> assert is_valid_url("http://youtube.com:8080")
    >>> assert is_valid_url("http://youtube.com/meow")
    >>> assert is_valid_url("http://youtube.com:8080/meow")
    >>> assert is_valid_url("http://52.19.02.20")
    >>> assert is_valid_url("http://52.19.02.20:8080")
    >>> assert is_valid_url("http://52.19.02.20/meow")
    >>> assert is_valid_url("http://52.19.02.20:8080/meow")
    >>> assert not is_valid_url("http://meow")
    >>> assert not is_valid_url("meow")
    >>> assert not is_valid_url("http:meow")
    >>> assert not is_valid_url("http://.com")
    >>> assert not is_valid_url("://meow.com")
    >>> assert not is_valid_url("meow.com")
    """
    regex = re.compile(
        r'^(?:http)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+'
        r'(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'                            # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return regex.match(url)
