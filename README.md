# lakeception [![Build status](https://ci.appveyor.com/api/projects/status/q6lm2fh9qojx6vsw/branch/master?svg=true)](https://ci.appveyor.com/project/Bemoliph/lakeception/branch/master)
![http://i.imgur.com/CHjSPCG.gif](http://i.imgur.com/CHjSPCG.gif)

Aww yeah, boats!

## How to Play

Get the [latest stable release](https://github.com/Bemoliph/lakeception/releases), or install from source using the developer instructions below.

## Developers

### Installing

#### Requirements
 * Python 2.7 with `pip` + `virtualenv`

#### Windows, Ubuntu 16.04 LTS
```sh
# Download the game's source code
cd ~
git clone https://github.com/Bemoliph/lakeception.git lakeception
cd lakeception

# Install required Python modules
virtualenv env
. env/bin/activate  # On Windows: env\Scripts\activate
pip install -r requirements.txt
```

#### CentOS 7
```sh
# Install GCC and friends + Python development files
sudo yum groupinstall "Development Tools"
sudo yum install python-devel

# Install SDL libraries for PyGame
sudo yum install SDL-devel libv4l-dev SDL_ttf SDL_ttf-devel
cd /usr/include/linux
sudo ln -s ../libv4l1-videodev.h videodev.h

# Download the game's source code
cd ~
git clone https://github.com/Bemoliph/lakeception.git lakeception
cd lakeception

# Install required Python modules
virtualenv env
. env/bin/activate
pip install -r requirements.txt
```

Additionally, you will need some way to display SDL if your CentOS is terminal only (X, framebuffer, etc).

### Running

To start the game,

```sh
bin/lakeception
```

or

```sh
python -m lakeception
```

### Testing

To test that everything built and runs okay, enter:

```sh
$ python setup.py test
```

Or test multiple python environments with:

```sh
$ tox
```
