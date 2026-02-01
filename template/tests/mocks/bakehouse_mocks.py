"""Mock data fixtures for bakehouse sales testing."""

from datetime import datetime

import pytest


@pytest.fixture
def df_transactions(spark):
    """Create transactions DataFrame from mock data."""
    schema = """
        transactionID STRING,
        dateTime TIMESTAMP,
        customerID STRING,
        franchiseID STRING,
        product STRING,
        quantity INT,
        unitPrice DOUBLE,
        totalPrice DOUBLE,
        paymentMethod STRING,
        cardNumber LONG
    """
    data = [
        ("TXN001", datetime(2024, 1, 15, 10, 30, 0), "CUST001", "FR001", "Croissant", 2, 3.50, 7.00, "Credit Card", 1234567890123456),
        ("TXN002", datetime(2024, 1, 15, 11, 45, 0), "CUST002", "FR002", "Baguette", 1, 4.00, 4.00, "Cash", 9876543210987654),
        ("TXN003", datetime(2024, 1, 16, 9, 0, 0), "CUST003", "FR001", "Sourdough Loaf", 1, 6.50, 6.50, "Debit Card", 1111222233334444),
    ]
    return spark.createDataFrame(data, schema)


@pytest.fixture
def df_customers(spark):
    """Create customers DataFrame from mock data."""
    schema = """
        customerId STRING,
        first_name STRING,
        last_name STRING,
        gender STRING,
        country STRING,
        continent STRING
    """
    data = [
        ("CUST001", "Alice", "Johnson", "F", "USA", "North America"),
        ("CUST002", "Bob", "Smith", "M", "Canada", "North America"),
        ("CUST003", "Carol", "Williams", "F", "UK", "Europe"),
    ]
    return spark.createDataFrame(data, schema)


@pytest.fixture
def df_franchises(spark):
    """Create franchises DataFrame from mock data."""
    schema = """
        franchiseID STRING,
        name STRING,
        size STRING,
        longitude DOUBLE,
        latitude DOUBLE
    """
    data = [
        ("FR001", "Downtown Bakehouse", "L", -73.9857, 40.7484),
        ("FR002", "Suburban Bakehouse", "M", -74.0060, 40.7128),
    ]
    return spark.createDataFrame(data, schema)


@pytest.fixture
def df_expected_enriched_sales(spark):
    """Create expected enriched sales DataFrame."""
    schema = """
        transactionID STRING,
        transactionDateTime TIMESTAMP,
        franchiseID STRING,
        product STRING,
        quantity INT,
        unitPrice DOUBLE,
        totalPrice DOUBLE,
        paymentMethod STRING,
        masked_cardNumber STRING,
        customerId STRING,
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
        ("TXN001", datetime(2024, 1, 15, 10, 30, 0), "FR001", "Croissant", 2, 3.50, 7.00, "Credit Card", "XXXX-XXXX-XXXX-3456", "CUST001", "Alice", "Johnson", "F", "USA", "North America", "Downtown Bakehouse", 3, -73.9857, 40.7484),
        ("TXN002", datetime(2024, 1, 15, 11, 45, 0), "FR002", "Baguette", 1, 4.00, 4.00, "Cash", "XXXX-XXXX-XXXX-7654", "CUST002", "Bob", "Smith", "M", "Canada", "North America", "Suburban Bakehouse", 2, -74.0060, 40.7128),
        ("TXN003", datetime(2024, 1, 16, 9, 0, 0), "FR001", "Sourdough Loaf", 1, 6.50, 6.50, "Debit Card", "XXXX-XXXX-XXXX-4444", "CUST003", "Carol", "Williams", "F", "UK", "Europe", "Downtown Bakehouse", 3, -73.9857, 40.7484),
    ]
    return spark.createDataFrame(data, schema)
