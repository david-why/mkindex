import argparse
import time
from os import listdir, stat
from os.path import isdir, isfile, realpath, dirname
from os.path import join as path_join

from jinja2 import Environment, FileSystemLoader, select_autoescape


def directory(name):
    if not isdir(name):
        raise TypeError('not a directory')
    return name


sizeof_cache = {}


def sizeof(path: str, s=None) -> int:
    if path in sizeof_cache:
        return sizeof_cache[path]
    size = (s if s else stat(path)).st_size
    if isfile(path):
        return size
    for file in listdir(path):
        size += sizeof(path_join(path, file))
    sizeof_cache[path] = size
    return size


def generate_index(
    base: str,
    directory: str,
    env: Environment,
    charset: str = 'UTF-8',
    recursive: bool = False,
    verbose: bool = False,
    ishome: bool = True,
):
    realdir = path_join(base, directory)
    items = listdir(realdir)
    files = []
    directories = []
    for item in items:
        path = path_join(realdir, item)
        s = stat(path)
        size = sizeof(path, s)
        mtime = s.st_mtime
        data = (item, size, time.ctime(mtime))
        if isfile(path):
            if item == 'index.html':
                continue
            files.append(data)
        else:
            directories.append(data)
            if recursive:
                generate_index(
                    base, path_join(directory, item), env, charset, True, verbose, False
                )
    tmpl = env.get_template('index_stub.html')
    if verbose:
        print(f'Writing {path_join(realdir, "index.html")}')
    with open(path_join(realdir, 'index.html'), 'w') as f:
        f.write(
            tmpl.render(
                path=directory,
                files=files,
                directories=directories,
                ishome=ishome,
                charset=charset,
            )
        )


if __name__ == '__main__':
    ap = argparse.ArgumentParser(
        description='Generate index.html from the files in a directory',
    )
    ap.add_argument(
        'directory',
        type=directory,
        help='The folder where all files to be added to the index are located',
    )
    ap.add_argument(
        '-r',
        '--recursive',
        action='store_true',
        help='Recursively generate index.html in subdirectories',
    )
    ap.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help='Show what is being done',
    )
    ap.add_argument(
        '--charset',
        default='UTF-8',
        help='The <meta charset> tag in the generated HTML (default: UTF-8)',
    )
    args = ap.parse_args()
    env = Environment(
        loader=FileSystemLoader(realpath(dirname(__file__))),
        autoescape=select_autoescape(),
    )
    generate_index(args.directory, '', env, args.charset, args.recursive, args.verbose)
