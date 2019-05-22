import sys
import argparse
import json
import asyncio
import signal
import numpy as np
import sounddevice as sd
import soundfile as sf
from pyftdi.i2c import I2cController

"""[summary]
"""

def int_handler(*args):
    """[summary]
    """
    for task in asyncio.Task.all_tasks():
        task.cancel()


async def play_file(buffer):
    """[summary]
    
    :param buffer: [description]
    :type buffer: [type]
    :raises sd.CallbackStop: [description]
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
    
    # TODO: device
    stream = sd.OutputStream(callback=callback, dtype='float32', channels=2, samplerate=32100)
    with stream:
        await event.wait()


async def main(filename):
    """[summary]
    
    :param filename: [description]
    :type filename: [type]
    """
    buffer, sr = sf.read(filename, dtype='float32')
    if not np.allclose(buffer.shape, (len(buffer),2)):
        buffer = np.c_[
            buffer if np.allclose(buffer.shape, (len(buffer),1)) else np.reshape(buffer, (len(buffer)),1),
            buffer if np.allclose(buffer.shape, (len(buffer),1)) else np.reshape(buffer, (len(buffer)),1)
        ]
    play_task = asyncio.ensure_future(play_file(buffer))
    for i in [float(j) / 100*(len(buffer)/sr) for j in range(0, 100, 1)]:
        await asyncio.sleep((len(buffer)/sr)/100)
    if not play_task.done():
        play_task.cancel()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple sound player")
    parser.add_argument('-f', '--filename', dest='filename', help=".wav filename", type=str)
    parser.add_argument('-l', '--list-devices', action='store_true', help='list connected FTDI devices')
    args = parser.parse_args()

    i2c = I2cController()
    if args.list_devices:
        out_devs = sd.query_devices(kind='output')
        if out_devs is None:
            print('No output sound devices')
        else:
            if not isinstance(out_devs, list):
                out_devs = [out_devs]
            for out_dev in out_devs:
                out_dev['dev_no'] = out_dev['hostapi']+1
            print('Output sound devices:')
            print(json.dumps(out_devs, indent=2))
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
        loop.run_until_complete(asyncio.gather(main(args.filename)))
    except asyncio.CancelledError:
        pass
    finally:
        loop.close()
