import asyncio
import os

import aiostd


def test_open_io_stream_reader_reads_data():
    async def main():
        r_fd, w_fd = os.pipe()
        r_file = os.fdopen(r_fd, "rb", 0)
        reader = await aiostd.open_io_stream_reader(r_file)
        try:
            os.write(w_fd, b"hello")
            data = await asyncio.wait_for(reader.read(5), timeout=1)
            assert data == b"hello"
        finally:
            reader._transport.close()
            r_file.close()
            os.close(w_fd)

    asyncio.run(main())


def test_open_io_stream_writer_writes_data():
    async def main():
        r_fd, w_fd = os.pipe()
        w_file = os.fdopen(w_fd, "wb", 0)
        writer = await aiostd.open_io_stream_writer(w_file)
        try:
            writer.write(b"world")
            await writer.drain()
            data = os.read(r_fd, 5)
            assert data == b"world"
        finally:
            writer.close()
            await asyncio.sleep(0)
            os.close(r_fd)

    asyncio.run(main())


def test_open_io_stream_combined():
    async def main():
        read_r, read_w = os.pipe()
        write_r, write_w = os.pipe()
        r_file = os.fdopen(read_r, "rb", 0)
        w_file = os.fdopen(write_w, "wb", 0)
        reader, writer = await aiostd.open_io_stream(r_file, w_file)
        try:
            writer.write(b"out")
            await writer.drain()
            assert os.read(write_r, 3) == b"out"

            os.write(read_w, b"in")
            data = await asyncio.wait_for(reader.read(2), timeout=1)
            assert data == b"in"
        finally:
            writer.close()
            await asyncio.sleep(0)
            reader._transport.close()
            await asyncio.sleep(0)
            r_file.close()
            os.close(read_w)
            os.close(write_r)

    asyncio.run(main())
