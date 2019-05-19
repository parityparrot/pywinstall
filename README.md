# PyWinstall

Windows installer for FTDI device and sound playback.

Driver files are copied from `inno-setup/driver/` and obtained from the libusb-win32 
[source](https://sourceforge.net/p/libusb-win32/wiki/Home/).

The executable was built using [pyinstaller](https://www.pyinstaller.org/). 
It simply lists out all FTDI devices available via [pyftdi](https://github.com/eblot/pyftdi) 
using a [pyusb](https://github.com/pyusb/pyusb) styled connection string.

The installer was compiled using [Inno Setup](http://www.jrsoftware.org/isinfo.php).

## Setup

0. (Prereq) Download [winpython](https://winpython.github.io/) 3.7. 
Rename `python-3.7.3.amd64` to `python37` and add it to the root directory of this project.

1. Run `start-env.bat` to start up the virtual envrionment.