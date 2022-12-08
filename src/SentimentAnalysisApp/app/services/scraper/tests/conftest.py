import pytest
import logging


@pytest.fixture
def logger():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s: %(message)s',
    )
    return logging.getLogger()
