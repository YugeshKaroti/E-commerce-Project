E-Commerce Event-Driven Analytics Pipeline
This project is an end-to-end E-commerce Data Pipeline & Analytics System designed to simulate, ingest, process, and analyze real-time and historical shopping behavior. It combines synthetic event generation with real-world data to deliver actionable insights via interactive dashboards.

Key Features
Synthetic Event Generation:
Built with the Faker library to simulate user interactions like:

Page views

Product views

Add-to-cart / Remove-from-cart

Purchase events

Data Warehouse Design:
A well-structured star schema implemented in MySQL with:

Fact Table: Events

Dimension Tables: Orders, Products, Sellers, Customers

ETL & Data Pipeline:

Real-time and batch event ingestion

Schema validation & enrichment

Sessionization logic to group events

Incremental loading with error handling

Dashboards & Analytics:

Streamlit dashboard for customer journey visualization

Key performance indicators (KPIs): Conversion rate, funnel analysis, product performance

Drill-downs on sellers, customer activity, and product categories

Integration of Historical Data:
Merged with the Brazilian E-Commerce Public Dataset from Olist for realistic behavior patterns and trend analysis.

Tech Stack
Languages: Python, SQL

Tools: Faker, Pandas, Streamlit, MySQL

Cloud & DB: MySQL

Visualization: Streamlit, Matplotlib, Seaborn

Use Cases
Customer journey and behavior tracking

Product recommendation groundwork

Seller and product performance monitoring

Event-driven architecture simulation

