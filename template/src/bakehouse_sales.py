from pyspark.sql import SparkSession

from transformations import enrich_bakehouse_sales


def main():
    app_name = "bakehouse_sales"
    spark = SparkSession.builder.appName(app_name).getOrCreate()

    bakehouse_transactions = "samples.bakehouse.sales_transactions"
    bakehouse_customers = "samples.bakehouse.sales_customers"
    bakehouse_franchises = "samples.bakehouse.sales_franchises"
    target_enrich_bakehouse_sales = "workspace.bakehouse.enrich_bakehouse_sales"

    columns_transactions = [
        "transactionID",
        "product",
        "quantity",
        "unitPrice",
        "totalPrice",
        "paymentMethod",
        "cardNumber",
        # Joins:
        "customerID",
        "franchiseID",
    ]

    columns_customers = [
        "customerID",
        "first_name",
        "last_name",
        "gender",
        "country",
        "continent",
    ]

    columns_franchises = ["franchiseID", "name", "size", "longitude", "latitude"]

    df_transactions = spark.read.table(bakehouse_transactions).select(columns_transactions)
    df_customers = spark.read.table(bakehouse_customers).select(columns_customers)
    df_franchises = spark.read.table(bakehouse_franchises).select(columns_franchises)

    df_enrich_bakehouse_sales = enrich_bakehouse_sales(
        df_transactions=df_transactions, df_customers=df_customers, df_franchises=df_franchises
    )

    spark.sparkContext.setJobGroup(app_name, f"Saving table {target_enrich_bakehouse_sales}.")
    df_enrich_bakehouse_sales.write.mode("overwrite").saveAsTable(target_enrich_bakehouse_sales)


if __name__ == "__main__":
    main()
