import asyncio
import os
from typing import IO


async def open_io_stream_reader(
    reader: IO,
    loop: asyncio.AbstractEventLoop | None = None,
) -> asyncio.StreamReader:
    """
    Asynchronously opens a stream reader for the given IO object.

    Args:
        reader (IO): The input stream (e.g., sys.stdin).
        loop (asyncio.AbstractEventLoop | None, optional): The event loop to use.
            Defaults to None, which means the current running loop will be used.

    Returns:
        asyncio.StreamReader: The stream reader object connected to the input stream.
    """
    if loop is None:
        loop = asyncio.get_running_loop()

    # Create a StreamReader and protocol pair
    _reader = asyncio.StreamReader(loop=loop)
    protocol = asyncio.StreamReaderProtocol(_reader)

    # Connect the reader to stdin
    # Source: https://stackoverflow.com/questions/58454190/python-async-waiting-for-stdin-input-while-doing-other-stuff
    await loop.connect_read_pipe(lambda: protocol, reader)

    return _reader


async def open_io_stream_writer(
    writer: IO,
    loop: asyncio.AbstractEventLoop | None = None,
) -> asyncio.StreamWriter:
    """
    Asynchronously opens a stream writer for the given IO object.

    Args:
        writer (IO): The output stream (e.g., sys.stdout).
        loop (asyncio.AbstractEventLoop | None, optional): The event loop to use.
            Defaults to None, which means the current running loop will be used.

    Returns:
        asyncio.StreamWriter: The stream writer object connected to the output stream.
    """
    if loop is None:
        loop = asyncio.get_running_loop()

    # Source: https://stackoverflow.com/questions/52089869/how-to-create-asyncio-stream-reader-writer-for-stdin-stdout
    writer_transport, writer_protocol = await loop.connect_write_pipe(
        lambda: asyncio.streams.FlowControlMixin(loop=loop),
        os.fdopen(writer.fileno(), "wb"),
    )

    _writer = asyncio.streams.StreamWriter(
        writer_transport, writer_protocol, None, loop
    )

    return _writer


async def open_io_stream(
    reader: IO,
    writer: IO,
    loop: asyncio.AbstractEventLoop | None = None,
) -> tuple[asyncio.StreamReader, asyncio.StreamWriter]:
    """
    Asynchronously opens both stream reader and writer for the given IO objects.

    Args:
        reader (IO): The input stream (e.g., sys.stdin).
        writer (IO): The output stream (e.g., sys.stdout).
        loop (asyncio.AbstractEventLoop | None, optional): The event loop to use.
            Defaults to None, which means the current running loop will be used.

    Returns:
        tuple[asyncio.StreamReader, asyncio.StreamWriter]: A tuple containing the
            stream reader and writer objects connected to the input and output streams.
    """
    if loop is None:
        loop = asyncio.get_running_loop()

    _reader = await open_io_stream_reader(reader)
    _writer = await open_io_stream_writer(writer)

    return _reader, _writer
