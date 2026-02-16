"""Shared schema definitions for test fixtures.

Single source of truth so that unit tests and behavior tests stay in sync.
"""

TRANSACTION_SCHEMA = """
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

CUSTOMER_SCHEMA = (
    "customerId BIGINT, first_name STRING, last_name STRING, gender STRING, country STRING, continent STRING"
)

FRANCHISE_SCHEMA = "franchiseID BIGINT, name STRING, size STRING, longitude DOUBLE, latitude DOUBLE"
