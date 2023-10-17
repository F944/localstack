from contextlib import contextmanager
from typing import Optional

import pytest

from localstack.constants import (
    TEST_AWS_ACCESS_KEY_ID,
    TEST_AWS_REGION_NAME,
    TEST_AWS_SECRET_ACCESS_KEY,
)


@pytest.fixture(autouse=True)
def switch_region():
    """A fixture which allows to easily switch the region in the config within a `with` context."""

    @contextmanager
    def _switch_region(region: Optional[str]):
        from localstack import config

        # FIXME adapt or remove with 2.0
        previous_region = config.DEFAULT_REGION
        try:
            config.DEFAULT_REGION = region
            yield
        finally:
            config.DEFAULT_REGION = previous_region

    return _switch_region


@pytest.fixture(autouse=True)
def set_boto_test_credentials_and_region(monkeypatch):
    """
    Automatically sets the default credentials and region for all unit tests.
    """
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", TEST_AWS_ACCESS_KEY_ID)
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", TEST_AWS_SECRET_ACCESS_KEY)
    monkeypatch.setenv("AWS_DEFAULT_REGION", TEST_AWS_REGION_NAME)
