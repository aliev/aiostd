# aioshutdown

A simple library for asynchronous communication with standard I/O

The library employs asyncio's I/O multiplexing, which enables efficient I/O operations by monitoring multiple file descriptors simultaneously without the overhead of creating separate threads.

## Installation

```
pip install -U aiostd
```

## Usage

```python
from aiostd import open_io_stream
import sys

async def main():
    reader, writer = await open_io_stream(sys.stdin, sys.stdout)

    async for line in reader:
        writer.write(line)
        await writer.drain()

asyncio.run(main())
```
