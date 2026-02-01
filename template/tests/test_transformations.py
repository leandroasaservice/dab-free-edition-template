"""Unit tests for transformations module."""

from pyspark.testing.utils import assertDataFrameEqual

from src.transformations import (
    add_full_name,
    enrich_bakehouse_sales,
    filter_by_age,
    remove_extra_spaces,
    uppercase_column,
)


def test_remove_extra_spaces(spark):
    """Test that extra whitespace is collapsed to single spaces."""
    data = [{"name": "John    Doe"}, {"name": "Jane   Smith"}]
    df = spark.createDataFrame(data)

    result = remove_extra_spaces(df, "name")

    expected = spark.createDataFrame([{"name": "John Doe"}, {"name": "Jane Smith"}])
    assertDataFrameEqual(result, expected)


def test_uppercase_column(spark):
    """Test that string column is converted to uppercase."""
    data = [{"city": "new york"}, {"city": "los angeles"}]
    df = spark.createDataFrame(data)

    result = uppercase_column(df, "city")

    expected = spark.createDataFrame([{"city": "NEW YORK"}, {"city": "LOS ANGELES"}])
    assertDataFrameEqual(result, expected)


def test_add_full_name(spark):
    """Test that first and last names are concatenated."""
    data = [{"first": "John", "last": "Doe"}, {"first": "Jane", "last": "Smith"}]
    df = spark.createDataFrame(data)

    result = add_full_name(df, "first", "last")

    assert "full_name" in result.columns
    names = [row.full_name for row in result.collect()]
    assert names == ["John Doe", "Jane Smith"]


def test_filter_by_age(spark):
    """Test that rows are filtered by minimum age."""
    data = [{"name": "Alice", "age": 25}, {"name": "Bob", "age": 17}, {"name": "Carol", "age": 30}]
    df = spark.createDataFrame(data)

    result = filter_by_age(df, min_age=18)

    assert result.count() == 2
    names = [row.name for row in result.collect()]
    assert "Alice" in names
    assert "Carol" in names
    assert "Bob" not in names


def test_enrich_bakehouse_sales(
    df_transactions,
    df_customers,
    df_franchises,
    df_expected_enriched_sales,
):
    """Test that bakehouse sales are enriched with customer and franchise data."""
    result = enrich_bakehouse_sales(df_transactions, df_customers, df_franchises)

    assertDataFrameEqual(result, df_expected_enriched_sales)
