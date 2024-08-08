import asyncio
import io
import pytest
import aiostd


@pytest.fixture
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.mark.asyncio
async def test_open_io_stream_reader(event_loop):
    input_data = "test input\n"
    reader = io.StringIO(input_data)

    stream_reader = await aiostd.open_io_stream_reader(reader, loop=event_loop)
    result = await stream_reader.readline()

    assert result == input_data


@pytest.mark.asyncio
async def test_open_io_stream_writer(event_loop):
    output = io.StringIO()

    stream_writer = await aiostd.open_io_stream_writer(output, loop=event_loop)
    test_data = "test output\n"
    stream_writer.write(test_data)
    await stream_writer.drain()

    assert output.getvalue() == test_data


@pytest.mark.asyncio
async def test_open_io_stream(event_loop):
    input_data = "test input\n"
    reader = io.StringIO(input_data)
    output = io.StringIO()

    stream_reader, stream_writer = await aiostd.open_io_stream(reader, output, loop=event_loop)
    result = await stream_reader.readline()
    stream_writer.write(result)
    await stream_writer.drain()

    assert result == input_data
    assert output.getvalue() == input_data
