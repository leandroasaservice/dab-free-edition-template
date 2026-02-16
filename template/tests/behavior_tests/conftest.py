"""Pytest fixtures for behavior tests — reuses the session-scoped SparkSession."""

import pytest
from pyspark.sql import SparkSession


@pytest.fixture(scope="session")
def spark():
    """Create a SparkSession for testing."""
    spark = SparkSession.builder.appName("pytest-spark").master("local[*]").getOrCreate()
    yield spark
    spark.stop()
