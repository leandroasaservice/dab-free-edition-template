"""Simple PySpark transformations for demonstration."""

from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def remove_extra_spaces(df: DataFrame, column: str) -> DataFrame:
    """Remove extra whitespace from a string column, leaving single spaces."""
    return df.withColumn(column, F.regexp_replace(F.col(column), r"\s+", " "))


def uppercase_column(df: DataFrame, column: str) -> DataFrame:
    """Convert a string column to uppercase."""
    return df.withColumn(column, F.upper(F.col(column)))


def add_full_name(df: DataFrame, first_col: str, last_col: str) -> DataFrame:
    """Concatenate first and last name columns into a full_name column."""
    return df.withColumn("full_name", F.concat_ws(" ", F.col(first_col), F.col(last_col)))


def filter_by_age(df: DataFrame, min_age: int) -> DataFrame:
    """Filter rows where age is greater than or equal to min_age."""
    return df.filter(F.col("age") >= min_age)
