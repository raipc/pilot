"""
This module compares performance of different implementations of check_email function.
You need a prepared text file containing multiple emails, one for each line.
Usage:
    python main.py < emails.txt
"""
import sys
from time import time

from check_email_cython import check_email as check_email_cython_f
from check_email_regex import check_email as check_email_regex_f
from check_email_regex_inverted import check_email as check_email_regex_inv_f
from check_email_traverse import check_email as check_email_traverse_f


def process_lines(func, emails, out_info=None, out_stat=sys.stdout):
    start = time()
    for email in emails:
        func(email)
    spent = time() - start
    if out_info is not None:  # as we shouldn't count collections and I/O
        output = tuple("%s is a %s email\n" % (email, func(email))
                       for email in emails)
        with open(out_info, 'w') as output_file:
            output_file.write(''.join(output))
    out_stat.write('%s: %s seconds\n' % (func.__module__, spent))


def main(inp=sys.stdin):
    lines = tuple(line.strip() for line in inp)
    tested_functions = [check_email_cython_f,
                        check_email_regex_f,
                        check_email_regex_inv_f,
                        check_email_traverse_f]
    for i, func in enumerate(tested_functions):
        process_lines(func, lines)


if __name__ == '__main__':
    main()
