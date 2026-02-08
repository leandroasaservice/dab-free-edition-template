"""Unit tests for src/transformations.py."""

from pyspark.testing.utils import assertDataFrameEqual

from src.transformations import (
    add_full_name,
    enrich_bakehouse_sales,
    filter_by_age,
    remove_extra_spaces,
    uppercase_column,
)


pytest_plugins = ["tests.unit_tests.transformations_data"]


def test_remove_extra_spaces(mock_names, expected_names):
    """Test that extra whitespace is collapsed to single spaces."""
    result = remove_extra_spaces(mock_names, "name")

    assertDataFrameEqual(result, expected_names)


def test_uppercase_column(mock_cities, expected_cities):
    """Test that string column is converted to uppercase."""
    result = uppercase_column(mock_cities, "city")

    assertDataFrameEqual(result, expected_cities)


def test_add_full_name(mock_full_name):
    """Test that first and last names are concatenated."""
    result = add_full_name(mock_full_name, "first", "last")

    assert "full_name" in result.columns
    names = [row.full_name for row in result.collect()]
    assert names == ["John Doe", "Jane Smith"]


def test_filter_by_age(mock_ages):
    """Test that rows are filtered by minimum age."""
    result = filter_by_age(mock_ages, min_age=18)

    assert result.count() == 2
    names = [row.name for row in result.collect()]
    assert "Alice" in names
    assert "Carol" in names
    assert "Bob" not in names


def test_enrich_bakehouse_sales(
    mock_transactions,
    mock_customers,
    mock_franchises,
    expected_enriched_sales,
):
    """Test that bakehouse sales are enriched with customer and franchise data."""
    result = enrich_bakehouse_sales(mock_transactions, mock_customers, mock_franchises)

    assertDataFrameEqual(result, expected_enriched_sales)
