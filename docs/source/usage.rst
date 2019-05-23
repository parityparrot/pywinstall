Usage
======================================

The generated `pywince.exe` executable has the following options:

.. code-block:: bash

    usage: pywince.exe [-h] [-f FILENAME] [-d DEV_NO] [-l]

    Simple sound player

    optional arguments:
    -h, --help            show this help message and exit
    -f FILENAME, --filename FILENAME
                            .wav filename
    -d DEV_NO, --dev-no DEV_NO
                            device number
    -l, --list-devices    list connected FTDI devices

.. _ListDevices:

List devices
--------------------------------------

To list all connected sound devices and FTDI USB devices, run

.. code-block:: bash

    pywince.exe -l

The output will be similar to the following:

.. code-block:: bash

    Output sound devices:
    [
      {
        "name": "Microsoft Sound Mapper - Output",
        "hostapi": 0,
        "max_input_channels": 0,
        "max_output_channels": 2,
        "default_low_input_latency": 0.09,
        "default_low_output_latency": 0.09,
        "default_high_input_latency": 0.18,
        "default_high_output_latency": 0.18,
        "default_samplerate": 44100.0,
        "dev_no": 0
      },
      ...
    ]

    Available interfaces:
      ftdi://ftdi:232h:FT123ABC/1   (C232HM-DDHSL-0)

    Please specify the USB device

Play sound
--------------------------------------

To a `.wav` file, run

.. code-block:: bash

    pywince.exe -f [YOUR-WAVE-FILE]

where :code:`[YOUR-WAVE-FILE]` is the location of a `.wav` sound file, e.g. `parrot.wav`.

Additionally, you can specify an alternative output sound device with the :code:`-d` or :code:`--dev-no` flag.

.. code-block:: bash

    pywince.exe -f [YOUR-WAVE-FILE] -d 5

You can find the device number of a particular output sound device from the :code:`dev_no` attributes in ListDevices_.