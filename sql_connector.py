from sqlalchemy import create_engine

import pandas as pd


MYSQL_USER = "root"
MYSQL_PASSWORD = "2193"
MYSQL_HOST = "localhost" 
MYSQL_PORT = 3306
MYSQL_DB = "Ecommerce_Project"
engine = create_engine(f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}")

olist_products_cleaned_dataset = pd.read_csv("olist_products_cleaned_dataset.csv")

olist_customers_cleaned_dataset = pd.read_csv("olist_customers_cleaned_dataset.csv") 

olist_orders_cleaned_dataset = pd.read_csv("olist_orders_cleaned_dataset.csv")

olist_sellers_cleaned_dataset = pd.read_csv("olist_sellers_cleaned_dataset.csv")

olist_products_cleaned_dataset.to_sql(name="dim_products", con=engine, if_exists="replace", index=False)

olist_customers_cleaned_dataset.to_sql(name = "dim_customers", con = engine, if_exists = "replace", index = False)

olist_orders_cleaned_dataset.to_sql(name = "dim_orders", con = engine, if_exists = "replace", index = False)

olist_sellers_cleaned_dataset.to_sql(name = "dim_sellers", con = engine, if_exists = "replace", index = False)
