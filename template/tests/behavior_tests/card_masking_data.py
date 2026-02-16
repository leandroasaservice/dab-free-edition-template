"""Mock data for card masking behavior tests."""

import pytest

from tests.schemas import CUSTOMER_SCHEMA, FRANCHISE_SCHEMA


@pytest.fixture
def single_customer(spark):
    """One customer that matches customerID=1."""
    return spark.createDataFrame(
        [(1, "Alice", "Test", "F", "US", "North America")],
        CUSTOMER_SCHEMA,
    )


@pytest.fixture
def single_franchise(spark):
    """One franchise that matches franchiseID=10."""
    return spark.createDataFrame(
        [(10, "Test Bakehouse", "M", -73.99, 40.71)],
        FRANCHISE_SCHEMA,
    )
