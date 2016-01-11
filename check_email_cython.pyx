# -*- coding: utf-8
cdef bint allowed_char(Py_UCS4 ch, bint inside_quotes):
    return u'a' <= ch <= u'z' or u'0'<= ch <= u'9' or ch in u'_-' or (
        inside_quotes and ch in u'!,:')


def check_email(basestring input):
    #if not isinstance(input, basestring):
    #    raise TypeError('email should be a string')
    cdef bint name_part, open_quote
    cdef int char_counter = 0
    cdef Py_UCS4 prev, ch
    cdef unicode email = unicode(input)
    name_part = True
    open_quote = False
    prev = u'0'
    for ch in email:
        char_counter += 1

        if name_part:
            if allowed_char(ch, open_quote):
                prev = ch
                continue
            if ch == u'.':
                if prev == u'.':
                    return False
            elif ch == u'@':
                if char_counter == 1 or char_counter > 129 or open_quote:
                    return False
                name_part = False
                char_counter = 0
            elif ch == u"\"":
                open_quote = not open_quote
            else:
                return False
        else:
            if ch == u'.':
                if prev == u'.' or prev == u'-' or prev == u'@':
                    return False
            elif ch == u'-':
                if prev == u'.' or prev == u'@':
                    return False
            elif not allowed_char(ch, False):
                return False
        prev = ch
    return name_part == 0 and 3 <= char_counter <= 256 and ch not in u'.-'

