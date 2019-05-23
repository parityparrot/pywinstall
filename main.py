import sys
import argparse
import json
import asyncio
import signal
import numpy as np
import sounddevice as sd
import soundfile as sf
from pyftdi.i2c import I2cController


def int_handler(*args):
    """`SIGINT` and `SIGTERM` interrupt handler that cancels all 
    :raw-html:`<a href="https://docs.python.org/3/library/asyncio-task.html#asyncio.Task.cancel" 
    target="_blank"><code style="color:#E74C3C">asyncio</code></a>` tasks.
    """
    for task in asyncio.Task.all_tasks():
        task.cancel()


async def play_file(buffer, device):
    """Asynchronously plays input sound buffer.
    
    :param buffer: Input sound buffer used by 
        :raw-html:`<a href="https://python-sounddevice.readthedocs.io/en/0.3.12/api.html?highlight=outputstream#sounddevice.OutputStream" 
        target="_blank"><code style="color:#E74C3C">sounddevice.OutpuSttream</code></a>`.
    :type buffer: :raw-html:`<a href="https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html" 
        target="_blank"><i>numpy.ndarray</i></a>`
    :param device: Output sound device number.
    :type device: int
    :raises sd.CallbackStop: Exception to be raised by the user to abort callback processing. 
        All pending buffers are discarded and the callback will not be invoked anymore.
        See :raw-html:`<a href="https://python-sounddevice.readthedocs.io/en/0.3.12/api.html?highlight=outputstream#sounddevice.CallbackStop" 
        target="_blank"><code style="color:#E74C3C">sounddevice.CallbackStop</code></a>`.
    """
    loop = asyncio.get_event_loop()
    event = asyncio.Event()
    idx = 0

    def callback(outdata, frame_count, time_info, status):
        nonlocal idx
        if status:
            print(status)
        remainder = len(buffer) - idx
        if remainder == 0:
            loop.call_soon_threadsafe(event.set)
            raise sd.CallbackStop
        valid_frames = frame_count if remainder >= frame_count else remainder
        outdata[:valid_frames] = buffer[idx:idx + valid_frames]
        outdata[valid_frames:] = 0
        idx += valid_frames
    
    stream = sd.OutputStream(callback=callback, dtype='float32', channels=2, samplerate=32100, device=device)
    with stream:
        await event.wait()


async def main(filename, device=1):
    """Transforms input `.wav` file to a :raw-html:`<a href="https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html" 
    target="_blank"><code style="color:#E74C3C">numpy.ndarray</code></a>` object for sound buffer.
    Calls :py:meth:`main.play_file` with the sound buffer.
    
    :param filename: The file name of the sound file.
    :type filename: str
    :param device: The device number of the output sound source, defaults to 1.
    :type device: int, optional
    """
    buffer, sr = sf.read(filename, dtype='float32')
    if not np.allclose(buffer.shape, (len(buffer),2)):
        buffer = np.c_[
            buffer if np.allclose(buffer.shape, (len(buffer),1)) else np.reshape(buffer, (len(buffer)),1),
            buffer if np.allclose(buffer.shape, (len(buffer),1)) else np.reshape(buffer, (len(buffer)),1)
        ]
    play_task = asyncio.ensure_future(play_file(buffer, device))
    for i in [float(j) / 100*(len(buffer)/sr) for j in range(0, 100, 1)]:
        await asyncio.sleep((len(buffer)/sr)/100)
    if not play_task.done():
        play_task.cancel()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Simple sound player")
    parser.add_argument('-f', '--filename', dest='filename', help=".wav filename", type=str)
    parser.add_argument('-d', '--dev-no', dest='dev_no', help="device number", type=int)
    parser.add_argument('-l', '--list-devices', action='store_true', help='list connected FTDI devices')
    args = parser.parse_args()

    i2c = I2cController()
    if args.list_devices:
        out_devs = sd.query_devices()
        if out_devs is None:
            print('No output sound devices')
        else:
            devices = []
            for dno, out_dev in enumerate(out_devs):
                out_dev['dev_no'] = dno
                devices.append(out_dev)
            print('Output sound devices:')
            print(json.dumps(devices, indent=2))
            print('')

        i2c.configure('ftdi:///?')
        # ignore [-f FILENAME] if included
        sys.exit(0)
    else:
        if args.filename is None:
            parser.error('must select either [-h] or [-f FILENAME]')
        else:   
            if not (args.filename).endswith('.wav'):
                parser.error('filename must end in .wav')

    loop = asyncio.get_event_loop()
    if loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    signal.signal(signal.SIGINT, int_handler)
    signal.signal(signal.SIGTERM, int_handler)

    try:
        if args.dev_no is None:
            loop.run_until_complete(asyncio.gather(main(args.filename)))
        else:
            loop.run_until_complete(asyncio.gather(main(args.filename, args.dev_no)))
    except asyncio.CancelledError:
        pass
    finally:
        loop.close()
