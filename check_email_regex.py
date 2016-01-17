import re

MIN_NAME_LENGTH = 1
MAX_NAME_LENGTH = 128
MIN_DOMAIN_LENGTH = 3
MAX_DOMAIN_LENGTH = 256

EMAIL_REGEX = re.compile(r'''
    ^(?:[a-z0-9_-]|(?:\.(?!\.))|(?:"(?:[a-z0-9!,:_-]|\.(?!\.))*"))+
    @
    [a-z0-9_]+(?:(?:\.|-+)[a-z0-9_]+)*$
    ''', re.VERBOSE)


def check_email(email):
    if not isinstance(email, basestring):
        raise TypeError('email should be a string')
    if len(email) > MAX_NAME_LENGTH + MAX_DOMAIN_LENGTH + 1:
        return False
    match = EMAIL_REGEX.match(email)
    if match is None:
        return False
    name_length = email.find('@')
    domain_length = len(email) - name_length - 1
    return MIN_NAME_LENGTH <= name_length <= MAX_NAME_LENGTH and (
        MIN_DOMAIN_LENGTH <= domain_length <= MAX_DOMAIN_LENGTH)
