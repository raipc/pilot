import re


EVEN_QUOTES_REGEXP = r'%(valid)s(?:"[a-z0-9.!,:_-]*?"%(valid)s)*?' % {
    'valid': '[a-z0-9._-]*?'}

NOT_NAME_REGEXP = re.compile(r'''$
    |(?:.{129,}?)|.*?(?:
        \.{2}
        |(?:[^a-z0-9"._!,:-]))
        |(?:%(quotes)s
            (?:[!,:]+?)
         %(quotes)s)    
''' % {'quotes': EVEN_QUOTES_REGEXP}, re.VERBOSE)

NOT_DOMAIN_REGEXP = re.compile(r'''^[.-]|
    (?:.{0,2}$)|(?:.{257,}?)|.*?(?:(?:-(?:\.|$))
    |(?:\.(?:[.-]|$))
    |(?:[^a-z0-9._-]))
    ''', re.VERBOSE)


def check_email(email):
    if not isinstance(email, basestring):
        raise TypeError('email should be a string')
    email_parts = email.split('@')
    if len(email_parts) != 2:
        return False
    good_name = NOT_NAME_REGEXP.match(email_parts[0]) is None
    good_domain = NOT_DOMAIN_REGEXP.match(email_parts[1]) is None
    return good_name and good_domain and email_parts[0].count('"') % 2 == 0

