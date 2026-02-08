-- DDL for creating Unity Catalog objects for gold_sales_monitoring
-- This script should be run once to initialize the catalog structure.
-- All parameters are passed from the job configuration.

-- Create catalog if not exists
CREATE CATALOG IF NOT EXISTS IDENTIFIER(:catalog_name)
COMMENT 'Catalog for reporting and analytics';

-- Set catalog tags using dynamic SQL
EXECUTE IMMEDIATE 'ALTER CATALOG ' || :catalog_name || ' SET TAGS (
    \'department\' = \'' || :department || '\',
    \'environment\' = \'' || :environment || '\',
    \'team\' = \'' || :team || '\'
)';

-- Use the catalog
USE CATALOG IDENTIFIER(:catalog_name);

-- Create schema if not exists
CREATE SCHEMA IF NOT EXISTS IDENTIFIER(:schema_name)
COMMENT 'Schema for bakehouse sales data';

-- Set schema tags using dynamic SQL
EXECUTE IMMEDIATE 'ALTER SCHEMA ' || :schema_name || ' SET TAGS (
    \'catalog\' = \'' || :catalog_name || '\',
    \'department\' = \'' || :department || '\',
    \'environment\' = \'' || :environment || '\',
    \'team\' = \'' || :team || '\'
)';

-- Use the schema
USE SCHEMA IDENTIFIER(:schema_name);

-- Create table if not exists
CREATE TABLE IF NOT EXISTS IDENTIFIER(:table_name) (
    transactionID BIGINT COMMENT 'Unique transaction identifier',
    transactionDateTime TIMESTAMP COMMENT 'Date and time of the transaction',
    franchiseID BIGINT COMMENT 'Franchise identifier',
    product STRING COMMENT 'Product name',
    quantity INT COMMENT 'Quantity purchased',
    unitPrice DECIMAL(10,2) COMMENT 'Price per unit',
    totalPrice DECIMAL(10,2) COMMENT 'Total transaction price',
    paymentMethod STRING COMMENT 'Payment method used',
    masked_cardNumber STRING COMMENT 'Masked credit card number (last 4 digits visible)',
    customerId BIGINT COMMENT 'Customer identifier',
    first_name STRING COMMENT 'Customer first name',
    last_name STRING COMMENT 'Customer last name',
    gender STRING COMMENT 'Customer gender',
    customer_country STRING COMMENT 'Customer country',
    customer_continent STRING COMMENT 'Customer continent',
    franchise_name STRING COMMENT 'Franchise name',
    franchise_size INT COMMENT 'Franchise size (1=S, 2=M, 3=L, 4=XL, 5=XXL)',
    franchise_longitude DOUBLE COMMENT 'Franchise longitude coordinate',
    franchise_latitude DOUBLE COMMENT 'Franchise latitude coordinate'
)
USING DELTA
COMMENT 'Enriched bakehouse sales data with customer and franchise information'
TBLPROPERTIES (
    'delta.autoOptimize.optimizeWrite' = 'true',
    'delta.autoOptimize.autoCompact' = 'true'
);

-- Set table tags using dynamic SQL
EXECUTE IMMEDIATE 'ALTER TABLE ' || :table_name || ' SET TAGS (
    \'catalog\' = \'' || :catalog_name || '\',
    \'schema\' = \'' || :schema_name || '\',
    \'department\' = \'' || :department || '\',
    \'environment\' = \'' || :environment || '\',
    \'team\' = \'' || :team || '\'
)';
