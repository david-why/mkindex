# mkindex
Generate index.html from the files in a directory.

## WARNING
Make sure there is no `index.html` in the directory being indexed! If there is it will be overwritten!!

## Requirements
You need to install [jinja2](https://pypi.org/project/Jinja2/). Just using `pip install Jinja2` would usually be enough.

## To use
```
usage: mkindex.py [-h] [-r] [-v] [--charset CHARSET] directory

Generate index.html from the files in a directory

positional arguments:
  directory          The folder where all files to be added to the index are located

optional arguments:
  -h, --help         show this help message and exit
  -r, --recursive    Recursively generate index.html in subdirectories
  -v, --verbose      Show what is being done
  --charset CHARSET  The <meta charset> tag in the generated HTML (default: UTF-8)
```
I think it is pretty much straightforward.
