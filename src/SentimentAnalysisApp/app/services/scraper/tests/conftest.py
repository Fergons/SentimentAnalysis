import pytest
import logging


@pytest.fixture
def logger():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s: %(message)s',
    )
    return logging.getLogger()

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"