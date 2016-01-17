# -*- coding: utf-8

cdef int MIN_NAME_LENGTH = 1
cdef int MAX_NAME_LENGTH = 128
cdef int MIN_DOMAIN_LENGTH = 3
cdef int MAX_DOMAIN_LENGTH = 256


cdef bint allowed_char(char ch, bint inside_quotes):
    return 'a' <= ch <= 'z' or '0'<= ch <= '9' or ch == '_' or ch == '-' or (
        inside_quotes and (ch == '!' or ch == ',' or ch == ':'))


def check_email(basestring inp):
    if len(inp) > MAX_NAME_LENGTH + MAX_DOMAIN_LENGTH + 1:
        return False
    cdef bint name_part, open_quote
    cdef int char_counter = 0
    cdef char prev, ch
    cdef char* email
    cdef bytes encoded_str
    if isinstance(inp, unicode):
        try:
            encoded_str = inp.encode("UTF-8")
            email = encoded_str
        except UnicodeEncodeError:
            return False
    else:
        email = inp
    name_part = True
    open_quote = False
    prev = '0'
    for ch in email:
        char_counter += 1

        if name_part:
            if allowed_char(ch, open_quote):
                prev = ch
                continue
            if ch == '.':
                if prev == '.':
                    return False
            elif ch == '@':
                if char_counter == 1 or char_counter > 129 or open_quote:
                    return False
                name_part = False
                char_counter = 0
            elif ch == '"':
                open_quote = not open_quote
            else:
                return False
        else:
            if ch == '.':
                if prev == '.' or prev == '-' or prev == '@':
                    return False
            elif ch == '-':
                if prev == '.' or prev == '@':
                    return False
            elif not allowed_char(ch, False):
                return False
        prev = ch
    return not name_part and 3 <= char_counter <= 256 and ch != '.' and ch != '-'
