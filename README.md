# lakeception

Aww yeah, boats!

## Installation

First install [pygame](http://www.pygame.org/download.shtml), following the
official instructions for your operation system of choice.

```
# On CentOS
$ sudo yum install SDL-devel libv4l-dev SDL_ttf SDL_ttf-devel
$ cd /usr/include/linux
$ sudo ln -s ../libv4l1-videodev.h videodev.h

$ virtualenv .
$ source bin/activate
$ pip install -r requirements.txt
```

## Run

To start the game, either double-click on `lakeception/main.py` or run:

```
$ python -m lakeception
```

## Testing

To test that everything built and runs okay, enter:

```
$ python setup.py test
```

Or test multiple python environments with:

```
$ tox
```
