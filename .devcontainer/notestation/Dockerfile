FROM python:3.10-slim

ARG USER="blues"

RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/* && \
    useradd -ms /bin/bash ${USER}

USER ${USER}

WORKDIR /workspace

RUN pip install pyserial requests

# Install note-python in editable mode
CMD ["pip", "install", "-e", "."]
