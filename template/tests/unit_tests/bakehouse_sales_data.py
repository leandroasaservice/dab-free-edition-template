"""Mock data for bakehouse_sales unit tests."""

from datetime import datetime
from decimal import Decimal

import pytest


@pytest.fixture
def mock_transactions(spark):
    """Mock transactions table data."""
    schema = """
        transactionID BIGINT,
        dateTime TIMESTAMP,
        customerID BIGINT,
        franchiseID BIGINT,
        product STRING,
        quantity INT,
        unitPrice DECIMAL(10,2),
        totalPrice DECIMAL(10,2),
        paymentMethod STRING,
        cardNumber DECIMAL(20,0)
    """
    data = [
        (
            1001,
            datetime(2024, 1, 15, 10, 30, 0),
            101,
            201,
            "Croissant",
            2,
            Decimal("3.50"),
            Decimal("7.00"),
            "Credit Card",
            Decimal("1234567890123456"),
        ),
    ]
    return spark.createDataFrame(data, schema)


@pytest.fixture
def mock_customers(spark):
    """Mock customers table data."""
    schema = """
        customerID BIGINT,
        first_name STRING,
        last_name STRING,
        gender STRING,
        country STRING,
        continent STRING
    """
    data = [
        (101, "Alice", "Johnson", "F", "USA", "North America"),
    ]
    return spark.createDataFrame(data, schema)


@pytest.fixture
def mock_franchises(spark):
    """Mock franchises table data."""
    schema = """
        franchiseID BIGINT,
        name STRING,
        size STRING,
        longitude DOUBLE,
        latitude DOUBLE
    """
    data = [
        (201, "Downtown Bakehouse", "L", -73.9857, 40.7484),
    ]
    return spark.createDataFrame(data, schema)
