# Imagesorter
A compact way to organize your pictures based on their luminance!

## Usage

```
usage: imagesorter.py [-h] [-s] [source_dir] [dest_dir]

Sort all pictures in source directory using the average luminance.

positional arguments:
  source_dir     Source directory of pictures to sort. Defaults to current
                  directory.
  dest_dir       Destination directory of sorted pictures. Defaults to
                  'sorted' in current directory

optional arguments:
  -h, --help     show this help message and exit
  -s, --symlink  Avoid copies by using symlinks
```

## Installation

### Option 1: you have python3
Clone the repo and use `imagesorter.py` as an executable directly.

### Option 2: you haven't python3
Clone the repo and use the compiled executable you can find at `/dist/imagesorter`. One can also download it directly via [this link](https://github.com/gabrielefronze/imagesorter/blob/master/dist/imagesorter?raw=true).