"""Unit tests for src/bakehouse_sales.py."""

pytest_plugins = ["tests.unit_tests.bakehouse_sales_data"]

# Note: bakehouse_sales.py contains the main() orchestration function
# that reads from Unity Catalog tables and writes results.
# Unit testing main() requires mocking spark.read.table() and write operations.
# Consider integration tests for end-to-end validation of the pipeline.
