# Binary Upload Example

Upload a binary file from a Notecard to a remote server via Notehub, using the note-python SDK's chunked upload mechanism.

This example includes two scripts:

- **`binary_upload_example.py`** — Runs on the host (e.g. Raspberry Pi) connected to a Notecard. Reads `blues_logo.png`, chunks it through the Notecard's binary buffer, and sends it to Notehub via `web.post`.
- **`receive_binary.py`** — A minimal HTTP server that receives the binary data routed from Notehub and saves it to disk.

## Prerequisites

- A [Blues Notecard](https://blues.com/products/notecard/) connected via USB serial
- A [Notehub](https://notehub.io) account and project
- Python 3.7+
- `pyserial` and `note-python` installed (`pip install pyserial note-python`)
- [ngrok](https://ngrok.com/) (or another tunnel) to expose the receive server publicly

## Setup

### 1. Start the receive server

On the machine where you want to receive files:

```bash
python3 receive_binary.py
```

This starts an HTTP server on port 8080 (pass a different port as an argument if needed). Files are saved to the current directory.

### 2. Expose the server with ngrok

In a separate terminal:

```bash
ngrok http 8080
```

Copy the HTTPS forwarding URL (e.g. `https://abc123.ngrok.io`).

### 3. Create a Notehub proxy route

In [Notehub](https://notehub.io), go to your project's **Routes** and create a new **General HTTP/HTTPS** route:

- **Route alias**: `upload`
- **URL**: your ngrok HTTPS URL

### 4. Configure and run the upload script

Edit `binary_upload_example.py` and set:

- **`PRODUCT_UID`** — your Notehub product UID (e.g. `com.your-company:your-project`)
- **`ROUTE_ALIAS`** — the route alias from step 3 (default: `upload`)
- **Serial port** — update the `serial.Serial(...)` path to match your Notecard's port

Then run:

```bash
python3 binary_upload_example.py
```

The script will:

1. Connect the Notecard to Notehub and wait for a connection
2. Read `blues_logo.png` (~222 KB)
3. Upload it in 64 KB chunks, printing progress after each chunk
4. Print a summary with total bytes, duration, and throughput

### 5. Check the output

The receive server prints a line for each file received:

```
Listening on port 8080. Saving files to: /your/current/directory
Press Ctrl+C to stop.

[14:23:01] Received 222,511 bytes -> blues_logo.png
```

## Chunk size tuning

The `MAX_CHUNK_SIZE` constant in `binary_upload_example.py` controls how large each chunk is. The Notecard's binary buffer can hold ~250 KB, but large single-chunk uploads over cellular can time out. The default of 64 KB is a good balance between throughput and reliability. Lower it to 32 KB if you experience timeouts on slow connections.

## File naming

Files are named using the Notecard's `label` field (sent as the `X-Notecard-Label` HTTP header by Notehub). If no label is present, the server generates a timestamped filename with an extension inferred from the file's magic bytes (`.png`, `.jpg`, `.pdf`, `.bin`, etc.).
