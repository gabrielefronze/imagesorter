# Imagesorter
A compact way to organize your pictures based on their luminance!

## Usage

```
usage: imagesorter.py [-h] [-s] [-g] [-c] [-a [ALGO]] [source_dir] [dest_dir]

Sort all pictures in source directory using the average luminance.

positional arguments:
  source_dir            Source directory of pictures to sort. Defaults to
                        current directory.
  dest_dir              Destination directory of sorted pictures. Defaults to
                        'sorted' in current directory

optional arguments:
  -h, --help            show this help message and exit
  -s, --symlink         Avoid copies by using symlinks
  -g, --gamma           Correct RGB colors to take in account gamma
  -c, --contrast        Use average contrast as rating algorithm, based on the
                        specified luminance algorithm
  -a [ALGO], --algo [ALGO]
                        Select luminance algorithm: photometrical, digital,
                        physiological. Defaults to physiological
```

## Installation
Clone the repo and use `imagesorter.py` as an executable directly.