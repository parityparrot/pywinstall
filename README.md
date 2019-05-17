# PyWinstall

Windows 64-bit installer that installs libusb driver and executable.

Driver files are copied from `inno-setup/driver/` and obtained from the libusb-win32 [source](https://sourceforge.net/p/libusb-win32/wiki/Home/).

The executable was built using [pyinstaller](https://www.pyinstaller.org/). It simply lists out all FTDI devices available via [pyftdi](https://github.com/eblot/pyftdi) using a [pyusb](https://github.com/pyusb/pyusb) styled connection string.

The installer was compiled using [Inno Setup](http://www.jrsoftware.org/isinfo.php).

## Setup

0. (Optional) Create a Python virtual environment.

1. Install Python requirements with
```
pip install -r requirements.txt
```

2. Build the executable with the batch script
```
install.bat
```

3. Compile the Windows installer using the Inno Setup compiler. You can download Inno Setup [here](http://www.jrsoftware.org/isdl.php).

4. Make sure FTDI device is plugged in.

5. Install the software using the generated installer in `inno-setup/Output/`. To run the executable with its parent folder added to system envrionment, you must first restart your host machine.

## TODO

- Uninstall should remove `libusb0.sys` and `libusb0.dll`.

- Pyinstaller encrypt Python bytecode