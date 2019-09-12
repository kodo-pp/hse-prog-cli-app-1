#!/usr/bin/env python3

import os
import sys
import time
from argparse import ArgumentParser


def parse_args():
    ap = ArgumentParser(description = 'CLI Application (workshop 2)')
    action_group = ap.add_mutually_exclusive_group(required=True)
    action_group.add_argument(
        '--mtime',
        '-m',
        action = 'store_true',
        default = None,
        help = 'Print file modification time',
    )
    action_group.add_argument(
        '--size',
        '-s',
        action = 'store_true',
        default = None,
        help = 'Print file size (in MiB)',
    )
    action_group.add_argument(
        '--rename',
        type = str,
        metavar = 'B',
        help = 'Rename file to B',
    )

    ap.add_argument(
        '--time-format',
        '-t',
        help='Date format. See https://docs.python.org/3/library/time.html#time.strftime for documentation',
        default='%Y-%m-%d %H:%M:%S'
    )
    ap.add_argument('filename', help='The name of the file')
    return ap.parse_args()


def get_mtime(filename):
    return os.stat(filename).st_mtime


def get_size(filename):
    if not os.path.isfile(filename):
        raise Exception(f'`{filename}` is not a regular file')
    return os.stat(filename).st_size


def get_size_in_mib(filename):
    return get_size(filename) / 2**20


def action_mtime(options):
    filename = options.filename
    raw_mtime = get_mtime(filename)
    mtime = time.localtime(raw_mtime)
    print(time.strftime(options.time_format, mtime))


def action_size(options):
    filename = options.filename
    size = get_size_in_mib(filename)
    print('{:.4f}'.format(size))


def action_rename(options):
    old_filename = options.filename
    new_filename = options.rename
    os.rename(old_filename, new_filename)


def main():
    options = parse_args()
    if options.mtime is not None:
        action_mtime(options)
    elif options.size is not None:
        action_size(options)
    elif options.rename is not None:
        action_rename(options)
    else:
        raise Exception('Internal error: none of the action arguments specified')


def main_wrapper():
    try:
        main()
    except Exception as e:
        print('Error: ' + str(e), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main_wrapper()
