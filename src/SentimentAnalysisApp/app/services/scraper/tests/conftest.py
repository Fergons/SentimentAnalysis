import pytest
import asyncio
import os


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()