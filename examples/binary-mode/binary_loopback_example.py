"""note-python binary loopback example.

This example writes an array of bytes to the binary data store on a Notecard and
reads them back. It checks that what was written exactly matches what's read
back.

Supports MicroPython, CircuitPython, and Raspberry Pi (Linux).
"""
import sys


def run_example(product_uid, use_uart=True):
    """Connect to Notcard and run a binary loopback test."""
    tx_buf = bytearray([
        0x67, 0x48, 0xa8, 0x1e, 0x9f, 0xbb, 0xb7, 0x27, 0xbb, 0x31, 0x89, 0x00, 0x1f,
        0x60, 0x49, 0x8a, 0x63, 0xa1, 0x2b, 0xac, 0xb8, 0xa9, 0xb0, 0x59, 0x71, 0x65,
        0xdd, 0x87, 0x73, 0x8a, 0x06, 0x9d, 0x40, 0xc1, 0xee, 0x24, 0xca, 0x31, 0xee,
        0x88, 0xf7, 0xf1, 0x23, 0x60, 0xf2, 0x01, 0x98, 0x39, 0x21, 0x18, 0x25, 0x3c,
        0x36, 0xf7, 0x93, 0xae, 0x50, 0xd6, 0x7d, 0x93, 0x55, 0xff, 0xcb, 0x56, 0xd3,
        0xd3, 0xd5, 0xe9, 0xf0, 0x60, 0xf7, 0xe9, 0xd3, 0xa4, 0x40, 0xe7, 0x8a, 0x71,
        0x72, 0x8b, 0x28, 0x5d, 0x57, 0x57, 0x8c, 0xc3, 0xd4, 0xe2, 0x05, 0xfa, 0x98,
        0xd2, 0x26, 0x4f, 0x5d, 0xb3, 0x08, 0x02, 0xf2, 0x50, 0x23, 0x5d, 0x9c, 0x6e,
        0x63, 0x7e, 0x03, 0x22, 0xa5, 0xb3, 0x5e, 0x95, 0xf2, 0x74, 0xfd, 0x3c, 0x2d,
        0x06, 0xf8, 0xdc, 0x34, 0xe4, 0x3d, 0x42, 0x47, 0x7c, 0x61, 0xe6, 0xe1, 0x53
    ])

    biggest_notecard_response = 400
    binary_chunk_size = 32
    uart_rx_buf_size = biggest_notecard_response + binary_chunk_size

    if sys.implementation.name == 'micropython':
        from machine import UART
        from machine import I2C
        from machine import Pin
        import board

        if use_uart:
            port = UART(board.UART, 9600)
            port.init(9600, bits=8, parity=None, stop=1,
                      timeout=3000, timeout_char=100, rxbuf=uart_rx_buf_size)
        else:
            port = I2C(board.I2C_ID, scl=Pin(board.SCL), sda=Pin(board.SDA))
    elif sys.implementation.name == 'circuitpython':
        import busio
        import board

        if use_uart:
            port = busio.UART(board.TX, board.RX, baudrate=9600, receiver_buffer_size=uart_rx_buf_size)
        else:
            port = busio.I2C(board.SCL, board.SDA)
    else:
        import os

        sys.path.insert(0, os.path.abspath(
                        os.path.join(os.path.dirname(__file__), '..')))

        from periphery import I2C
        import serial

        if use_uart:
            port = serial.Serial('/dev/ttyACM0', 9600)
        else:
            port = I2C('/dev/i2c-1')

    import notecard
    from notecard import binary_helpers

    if use_uart:
        card = notecard.OpenSerial(port, debug=True)
    else:
        card = notecard.OpenI2C(port, 0, 0, debug=True)

    print('Clearing out any old data...')
    binary_helpers.binary_store_reset(card)

    print('Sending buffer...')
    binary_helpers.binary_store_transmit(card, tx_buf, 0)
    print(f'Sent {len(tx_buf)} bytes to the Notecard.')

    print('Reading it back...')
    rx_buf = bytearray()

    left = binary_helpers.binary_store_decoded_length(card)
    offset = 0
    while left > 0:
        chunk_size = left if binary_chunk_size > left else binary_chunk_size
        chunk = binary_helpers.binary_store_receive(card, offset, chunk_size)
        rx_buf.extend(chunk)
        left -= chunk_size
        offset += chunk_size

    print(f'Received {len(rx_buf)} bytes from the Notecard.')

    print('Checking if received matches transmitted...')
    rx_len = len(rx_buf)
    tx_len = len(tx_buf)
    assert rx_len == tx_len, f'Length mismatch between sent and received data. Sent {tx_len} bytes. Received {rx_len} bytes.'

    for idx, (tx_byte, rx_byte) in enumerate(zip(tx_buf, rx_buf)):
        assert tx_byte == rx_byte, f'Data mismatch detected at index {idx}. Sent: {tx_byte}. Received: {rx_byte}.'

    print('Received matches transmitted.')
    print('Example complete.')


if __name__ == '__main__':
    product_uid = 'com.your-company.your-project'
    # Choose either UART or I2C for Notecard
    use_uart = True
    run_example(product_uid, use_uart)
