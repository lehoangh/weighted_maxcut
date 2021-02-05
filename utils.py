import sys


DEBUG = True


def debug(string):
    if DEBUG:
        sys.stdout.write(string)
        sys.stdout.flush()