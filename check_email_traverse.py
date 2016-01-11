# -*- coding: utf-8
import string

VALID_NAME_CHARS = set(string.ascii_lowercase + string.digits + '_-')
VALID_NAME_CHARS_INSIDE_QUOTES = set('!,:')
VALID_DOMAIN_CHARS = VALID_NAME_CHARS

MIN_NAME_LENGTH = 1
MAX_NAME_LENGTH = 128
MIN_DOMAIN_LENGTH = 3
MAX_DOMAIN_LENGTH = 256


def check_email(email):
    if not isinstance(email, basestring):
        raise TypeError('email should be a string')
    if len(email) > MAX_NAME_LENGTH + MAX_DOMAIN_LENGTH + 1:
        return False
    name_part = True
    open_quote = False
    char_counter = 0
    prev = ''
    char = '.'
    for char in email:
        char_counter += 1

        if name_part:
            if char in VALID_NAME_CHARS or (open_quote and
                    char in VALID_NAME_CHARS_INSIDE_QUOTES):
                prev = char
                continue
            if char == '.':
                if prev == '.':
                    return False
            elif char == '@':
                if char_counter == MIN_NAME_LENGTH or open_quote or (
                            char_counter > MAX_NAME_LENGTH + 1):
                    return False
                name_part = False
                char_counter = 0
            elif char == "\"":
                open_quote = not open_quote
            else:
                return False
        else:
            if char == '.':
                if prev == '.' or prev == '-' or prev == '@':
                    return False
            elif char == '-':
                if prev == '.' or prev == '@':
                    return False
            elif char not in VALID_DOMAIN_CHARS:
                return False
        prev = char
    return not name_part and (
        MIN_DOMAIN_LENGTH <= char_counter <= MAX_DOMAIN_LENGTH) and (
               char != '.' and char != '-')
