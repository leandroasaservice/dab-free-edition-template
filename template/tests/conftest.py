"""Pytest fixtures for PySpark testing."""

import pytest
from pyspark.sql import SparkSession

pytest_plugins = ["tests.mocks.bakehouse_mocks"]


@pytest.fixture(scope="session")
def spark():
    """Create a SparkSession for testing."""
    spark = SparkSession.builder \
        .appName("pytest-spark") \
        .master("local[*]") \
        .getOrCreate()
    yield spark
    spark.stop()
