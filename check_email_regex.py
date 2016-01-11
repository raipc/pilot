import re


EMAIL_REGEX = re.compile(r'''
    ^(?:([a-z0-9_-]|(?<!\.)\.)*(?:"(?:[a-z0-9!,:_-]|(?<!\.)\.)*")*)+
    @
    [a-z0-9_]+(?:(?:\.|-+)[a-z0-9_]+)*$
    ''', re.VERBOSE)


def check_email(email):
    if not isinstance(email, basestring):
        raise TypeError('email should be a string')
    match = EMAIL_REGEX.match(email)
    if match is None:
        return False
    name_length = email.find('@')
    email_length = len(email) - name_length - 1
    return 0 < name_length <= 128 and 3 <= email_length <= 256


