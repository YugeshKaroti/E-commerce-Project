import os, pandas as pd

cleaned_files = os.listdir(r"C:\Users\yuges\Downloads\E - commerce pipeline cleaned data")

 
l = []
for i in cleaned_files:
    l.append(pd.read_csv(r"C:\Users\yuges\Downloads\E - commerce pipeline cleaned data\{}".format(i)))

 
cleaned_files

 
olist_customers_cleaned_dataset = l[0]

olist_geolocation_cleaned_dataset = l[1]

olist_orders_cleaned_dataset = l[2]

olist_order_items_cleaned_dataset = l[3]

olist_order_payments_cleaned_dataset = l[4]

olist_order_reviews_cleaned_dataset = l[5]

olist_products_cleaned_dataset = l[6]

olist_sellers_cleaned_dataset = l[7]

 
from sqlalchemy import create_engine


MYSQL_USER = "root"
MYSQL_PASSWORD = "2193"
MYSQL_HOST = "localhost" 
MYSQL_PORT = 3306
MYSQL_DB = "Ecommerce_Project"
engine = create_engine(f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}")

olist_products_cleaned_dataset.to_sql(name="dim_products", con=engine, if_exists="replace", index=False)


 
olist_customers_cleaned_dataset.to_sql(name = "dim_customers", con = engine, if_exists = "replace", index = False)

 
olist_orders_cleaned_dataset.to_sql(name = "dim_orders", con = engine, if_exists = "replace", index = False)

 
olist_sellers_cleaned_dataset.to_sql(name = "dim_sellers", con = engine, if_exists = "replace", index = False)

 


 



