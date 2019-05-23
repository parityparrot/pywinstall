Setup
======================================

.. role:: raw-html(raw)
    :format: html

Considerations
--------------------------------------

The project uses :raw-html:`<a href="https://eblot.github.io/pyftdi/" target="_blank">PyFtdi</a>`, which requires Python 3.5 or newer.

This project assumes you have :raw-html:`<a href="https://winpython.github.io/" target="_blank">WinPython</a>`.
After extracting the WinPython files, rename `python-3.x.y.amd64\\` to `python3x\\` at the project root, where `x` is the version of Python 3.

If you are not using Python 3.7, rename :code:`start-env.bat` in `resources\\scripts\\` accordingly.

Preparing your workspace
--------------------------------------

Simply run :code:`start-env.bat` in `resources\\scripts\\`.

The :code:`start-env.bat` script performs the following actions:

* Adds the paths for `python.exe`, `pip.exe` are other executables installed by pip into the the `PATH` environment variable.

* Creates a virtual environment if it does not yet exist.

* Installs Python dependencies from the :code:`requirements.txt` file.