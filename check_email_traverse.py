# -*- coding: utf-8
import string

VALID_NAME_CHARS = set(string.ascii_lowercase + string.digits + '_-')
VALID_NAME_CHARS_INSIDE_QUOTES = set('!,:')
VALID_DOMAIN_CHARS = VALID_NAME_CHARS

def check_email(email):
    if not isinstance(email, basestring):
        raise TypeError('email should be a string')
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
                if char_counter == 1 or char_counter > 129 or open_quote:
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
    return not name_part and 3 <= char_counter <= 256 and char != '.' and char != '-'

#if __name__ == '__main__':
    #import sys


    #def main(inp=sys.stdin, out=sys.stdout):
    #    for s in inp:
    #        s = s.strip()
    #        out.write(u"%s: %s\n" % (s, unicode(check_emails(s))))


    #main()
