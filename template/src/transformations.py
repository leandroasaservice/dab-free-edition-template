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
    select cast(a.transactionID as bigint) as transactionID
        ,cast(a.dateTime as timestamp) as transactionDateTime
        ,cast(c.franchiseID as bigint) as franchiseID
        ,cast(a.product as string) as product
        ,cast(a.quantity as int) as quantity
        ,cast(a.unitPrice as decimal(10,2)) as unitPrice
        ,cast(a.totalPrice as decimal(10,2)) as totalPrice
        ,cast(a.paymentMethod as string) as paymentMethod
        ,cast(concat('XXXX-XXXX-XXXX-', right(cast(a.cardNumber as string), 4)) as string) as masked_cardNumber
        ,cast(b.customerId as bigint) as customerId
        ,cast(b.first_name as string) as first_name
        ,cast(b.last_name as string) as last_name
        ,cast(b.gender as string) as gender
        ,cast(b.country as string) as customer_country
        ,cast(b.continent as string) as customer_continent
        ,cast(c.name as string) as franchise_name
        ,cast(case when c.size = 'S' then 1
            when c.size = 'M' then 2
            when c.size = 'L' then 3
            when c.size = 'XL' then 4
            when c.size = 'XXL' then 5
            else null end as int) as franchise_size
        ,cast(c.longitude as double) as franchise_longitude
        ,cast(c.latitude as double) as franchise_latitude
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
