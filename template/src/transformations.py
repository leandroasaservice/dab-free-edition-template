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


def enrich_bakehouse_sales(df_transactions: DataFrame, df_customers: DataFrame, df_franchises: DataFrame) -> DataFrame:
    query = """
    select a.transactionID
        ,a.dateTime as transactionDateTime
        ,c.franchiseID
        ,a.product
        ,a.quantity
        ,a.unitPrice
        ,a.totalPrice
        ,a.paymentMethod
        ,concat('XXXX-XXXX-XXXX-', right(cast(a.cardNumber as string), 4)) as masked_cardNumber
        ,b.customerId
        ,b.first_name
        ,b.last_name
        ,b.gender
        ,b.country as customer_country
        ,b.continent as customer_continent
        ,c.name as franchise_name
        ,case when c.size = 'S' then 1
            when c.size = 'M' then 2
            when c.size = 'L' then 3
            when c.size = 'XL' then 4
            when c.size = 'XXL' then 5
            else null end as franchise_size
        ,c.longitude as franchise_longitude
        ,c.latitude as franchise_latitude
    from {bakehouse_sales_transactions} a
        left join {bakehouse_sales_customers} b on a.customerID = b.customerID
        left join {bakehouse_sales_franchises} c on a.franchiseID = c.franchiseID
    """
    return df_transactions.sparkSession.sql(
        query,
        bakehouse_sales_transactions=df_transactions,
        bakehouse_sales_customers=df_customers,
        bakehouse_sales_franchises=df_franchises,
    )
