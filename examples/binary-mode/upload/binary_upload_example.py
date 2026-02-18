"""note-python binary upload example.

This example uploads binary data to a Notehub proxy route using the
high-speed chunked upload mechanism. The data is staged through the
Notecard's binary buffer and sent to Notehub via web.post.

Before running this example:
1. Create a Proxy Route in your Notehub project (e.g. pointing to
   https://httpbin.org/post or your own endpoint).
2. Set PRODUCT_UID below to your Notehub product UID.
3. Set ROUTE_ALIAS to the alias of your proxy route.

Targets Raspberry Pi and other Linux systems.
"""
import os
import sys
import time

sys.path.insert(0, os.path.abspath(
                os.path.join(os.path.dirname(__file__), '..', '..')))

import serial  # noqa: E402

import notecard  # noqa: E402
from notecard import hub  # noqa: E402
from notecard.upload import upload  # noqa: E402


PRODUCT_UID = 'com.your-company:your-product'
ROUTE_ALIAS = 'upload'
# Keep chunks small enough to reliably transfer over cellular.
# The Notecard buffer can hold ~250KB, but pushing that much data
# in a single web.post over cellular often times out.
MAX_CHUNK_SIZE = 65536  # 64 KB


def on_progress(info):
    """Print upload progress after each chunk."""
    print(f'  Chunk {info["chunk"]}/{info["total_chunks"]} '
          f'- {info["percent_complete"]:.1f}% '
          f'- {info["avg_bytes_per_sec"]:.0f} B/s '
          f'- ETA {info["eta_secs"]:.1f}s')


def run_example():
    """Connect to Notecard and upload binary data to Notehub."""
    port = serial.Serial('/dev/ttyUSB0', 115200)
    card = notecard.OpenSerial(port, debug=True)

    # Connect the Notecard to Notehub.
    hub.set(card, product=PRODUCT_UID, mode='continuous')

    # Wait for the Notecard to connect to Notehub.
    print('Waiting for Notehub connection...')
    while True:
        rsp = hub.status(card)
        connected = rsp.get('connected', False)
        status_msg = rsp.get('status', '')
        if connected:
            print('Connected to Notehub.')
            break
        print(f'  Not yet connected: {status_msg}')
        time.sleep(2)

    # Read the image file to upload.
    image_path = os.path.join(os.path.dirname(__file__), 'blues_logo.png')
    with open(image_path, 'rb') as f:
        data = f.read()

    print(f'Uploading {image_path} ({len(data)} bytes) '
          f'to route "{ROUTE_ALIAS}"...')

    result = upload(
        card,
        data,
        route=ROUTE_ALIAS,
        label='blues_logo.png',
        content_type='image/png',
        max_chunk_size=MAX_CHUNK_SIZE,
        progress_cb=on_progress,
    )

    print(f'Upload complete: {result["bytes_uploaded"]} bytes '
          f'in {result["chunks"]} chunks, '
          f'{result["duration_secs"]:.1f}s '
          f'({result["bytes_per_sec"]:.0f} B/s)')


if __name__ == '__main__':
    run_example()
