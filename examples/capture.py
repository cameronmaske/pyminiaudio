"""
Recording audio from a selected input device.
"""

import array
from time import sleep
import miniaudio


def choose_device():

    devices = miniaudio.Devices()
    print("Available recording devices:")
    captures = devices.get_captures()
    for d in enumerate(captures):
        print("{num} = {name}".format(num=d[0], name=d[1]['name']))
    # choice = int(input("record from which device? "))
    return captures[5]


if __name__ == "__main__":
    buffer_chunks = []

    def record_to_buffer():
        after = 10
        counter = 0

        _ = yield
        while True:
            data = yield
            print(".", end="", flush=True)
            if counter == after:
                import win32event
                import random
                evt = win32event.CreateEvent(None, 0, 0, None)
                delay_ms = random.randint(200, 500)
                delay_ms = 333
                print("Delay of {}".format(delay_ms))
                win32event.WaitForSingleObject(evt, delay_ms)
            counter += 1
            # sleep( / 1000)
            buffer_chunks.append(data)

    selected_device = choose_device()
    capture = miniaudio.CaptureDevice(buffersize_msec=0, sample_rate=44100, device_id=selected_device["id"])
    generator = record_to_buffer()
    print("Recording for 3 seconds")
    next(generator)
    capture.start(generator)
    sleep(3)
    capture.stop()

    buffer = b"".join(buffer_chunks)
    print("\nRecorded", len(buffer), "bytes")
    print("Wring to ./capture.wav")
    samples = array.array('h')
    samples.frombytes(buffer)
    sound = miniaudio.DecodedSoundFile('capture', capture.nchannels, capture.sample_rate, capture.format, samples)
    miniaudio.wav_write_file('capture.wav', sound)
    print("Recording done")
