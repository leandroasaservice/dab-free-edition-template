"""Mock data for transformations unit tests."""

from datetime import datetime
from decimal import Decimal

import pytest

from tests.schemas import CUSTOMER_SCHEMA, FRANCHISE_SCHEMA, TRANSACTION_SCHEMA


# Data for test_remove_extra_spaces
@pytest.fixture
def mock_names(spark):
    """Input DataFrame with extra whitespace."""
    data = [("John    Doe",), ("Jane   Smith",)]
    return spark.createDataFrame(data, "name STRING")


@pytest.fixture
def expected_names(spark):
    """Expected DataFrame with single spaces."""
    data = [("John Doe",), ("Jane Smith",)]
    return spark.createDataFrame(data, "name STRING")


# Data for test_uppercase_column
@pytest.fixture
def mock_cities(spark):
    """Input DataFrame with lowercase cities."""
    data = [("new york",), ("los angeles",)]
    return spark.createDataFrame(data, "city STRING")


@pytest.fixture
def expected_cities(spark):
    """Expected DataFrame with uppercase cities."""
    data = [("NEW YORK",), ("LOS ANGELES",)]
    return spark.createDataFrame(data, "city STRING")


# Data for test_add_full_name
@pytest.fixture
def mock_full_name(spark):
    """Input DataFrame with first and last names."""
    data = [("John", "Doe"), ("Jane", "Smith")]
    return spark.createDataFrame(data, "first STRING, last STRING")


# Data for test_filter_by_age
@pytest.fixture
def mock_ages(spark):
    """Input DataFrame with people and ages."""
    data = [("Alice", 25), ("Bob", 17), ("Carol", 30)]
    return spark.createDataFrame(data, "name STRING, age INT")


# Data for test_enrich_bakehouse_sales
@pytest.fixture
def mock_transactions(spark):
    """Mock transactions DataFrame."""
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
        (
            1002,
            datetime(2024, 1, 15, 11, 45, 0),
            102,
            202,
            "Baguette",
            1,
            Decimal("4.00"),
            Decimal("4.00"),
            "Cash",
            Decimal("9876543210987654"),
        ),
        (
            1003,
            datetime(2024, 1, 16, 9, 0, 0),
            103,
            201,
            "Sourdough Loaf",
            1,
            Decimal("6.50"),
            Decimal("6.50"),
            "Debit Card",
            Decimal("1111222233334444"),
        ),
    ]
    return spark.createDataFrame(data, TRANSACTION_SCHEMA)


@pytest.fixture
def mock_customers(spark):
    """Mock customers DataFrame."""
    data = [
        (101, "Alice", "Johnson", "F", "USA", "North America"),
        (102, "Bob", "Smith", "M", "Canada", "North America"),
        (103, "Carol", "Williams", "F", "UK", "Europe"),
    ]
    return spark.createDataFrame(data, CUSTOMER_SCHEMA)


@pytest.fixture
def mock_franchises(spark):
    """Mock franchises DataFrame."""
    data = [
        (201, "Downtown Bakehouse", "L", -73.9857, 40.7484),
        (202, "Suburban Bakehouse", "M", -74.0060, 40.7128),
    ]
    return spark.createDataFrame(data, FRANCHISE_SCHEMA)


@pytest.fixture
def expected_enriched_sales(spark):
    """Expected output for enrich_bakehouse_sales."""
    schema = """
        transactionID BIGINT,
        transactionDateTime TIMESTAMP,
        franchiseID BIGINT,
        product STRING,
        quantity INT,
        unitPrice DECIMAL(10,2),
        totalPrice DECIMAL(10,2),
        paymentMethod STRING,
        masked_cardNumber STRING,
        customerId BIGINT,
        first_name STRING,
        last_name STRING,
        gender STRING,
        customer_country STRING,
        customer_continent STRING,
        franchise_name STRING,
        franchise_size INT,
        franchise_longitude DOUBLE,
        franchise_latitude DOUBLE
    """
    data = [
        (
            1001,
            datetime(2024, 1, 15, 10, 30, 0),
            201,
            "Croissant",
            2,
            Decimal("3.50"),
            Decimal("7.00"),
            "Credit Card",
            "XXXX-XXXX-XXXX-3456",
            101,
            "Alice",
            "Johnson",
            "F",
            "USA",
            "North America",
            "Downtown Bakehouse",
            3,
            -73.9857,
            40.7484,
        ),
        (
            1002,
            datetime(2024, 1, 15, 11, 45, 0),
            202,
            "Baguette",
            1,
            Decimal("4.00"),
            Decimal("4.00"),
            "Cash",
            "XXXX-XXXX-XXXX-7654",
            102,
            "Bob",
            "Smith",
            "M",
            "Canada",
            "North America",
            "Suburban Bakehouse",
            2,
            -74.0060,
            40.7128,
        ),
        (
            1003,
            datetime(2024, 1, 16, 9, 0, 0),
            201,
            "Sourdough Loaf",
            1,
            Decimal("6.50"),
            Decimal("6.50"),
            "Debit Card",
            "XXXX-XXXX-XXXX-4444",
            103,
            "Carol",
            "Williams",
            "F",
            "UK",
            "Europe",
            "Downtown Bakehouse",
            3,
            -73.9857,
            40.7484,
        ),
    ]
    return spark.createDataFrame(data, schema)
