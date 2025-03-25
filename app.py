from module.conn import get_conn, run_query

import streamlit as st, plotly.express as px, plotly.graph_objects as go

import logging

logging.basicConfig(filename = "app.log", format = "%(asctime)s %(levelname)s %(module)s %(lineno)d %(message)s",
                    datefmt = "%Y-%m-%d %H:%M:%S",level = logging.INFO)

logging.info("Started Streamlit Application")

st.sidebar.title(":red[E - Commerce Analytics]")

option = st.sidebar.radio("Select Dashboard", ["Customer Insights", "Sales Analytics", "Seller Performance", "Product Analytics"])

logging.info(f"Selected {option} option")

#st.image(r"C:\Users\yuges\OneDrive\Pictures\Screenshots\AdobeStock_223290240-1-scaled.jpeg")

if option == "Sales Analytics":

    st.title(":blue[Sales Performance Overview]")

    type = st.selectbox("Analysis Type ?", ("Please Select","Data mart", "Aggregration tables", "KPI"))

    logging.info(f"Selected {type} in {option}")


    if type == "Data mart":

        query = '''Select date(order_purchase_timestamp) as `Order Date`, sum(total_price) as `Total Revenue`, count(order_id) as `Total Orders`
        from dim_orders group by date(order_purchase_timestamp) order by date(order_purchase_timestamp) desc limit 30;'''

        sales_30_df = run_query(query)

        fig = px.line(sales_30_df, x = "Order Date", y = "Total Revenue", title = " Revenue Trend (Last 30 Days)")

        fig.update_traces(line=dict(color="red"))

        st.plotly_chart(fig)


        query = '''select month(`timestamp`) AS Month, round(sum(product_price * quantity)) AS `Total Revenue`, count(distinct(order_id)) AS `Total Orders`
        from fact_main group by Month order by Month;'''

        monthly_revenue = run_query(query)

        monthly_revenue["Month"] = monthly_revenue["Month"].map({1:"Jan",2:"Feb", 3:"Mar", 4:"Apr", 5:"May", 6:"Jun", 7:"Jul", 8:"Aug", 9:"Sep", 10:"Oct", 11:"Nov", 12:"Dec"})

        fig = px.bar(monthly_revenue, y = "Total Revenue", x = "Month", title = "Monthly Revenue")

        st.plotly_chart(fig)

        query = '''select p.product_category as `Product Category`, round(sum(f.product_price * f.quantity)) as `Total Revenue` from dim_products 
        p inner join fact_main f on p.product_id = f.product_id group by p.product_category order by `Total Revenue` desc limit 5; '''

        best_sell = run_query(query)

        fig = px.pie(best_sell, names = "Product Category", values = "Total Revenue", title = "Revenue of Top 5 Products")

        st.plotly_chart(fig)

        query = '''select payment_type as `Payment Type`, count(*) as count from dim_orders group by payment_type;'''

        pay = run_query(query)

        fig = px.pie(pay, names = "Payment Type", values = "count", title = "Payments users prefer")

        st.plotly_chart(fig)

        logging.debug("Completed Data mart in Sales Analytics")


    if type == "Aggregration tables":

        query = ''' select date(order_purchase_timestamp) as `Order Date`, count(distinct(order_id)) as `Total Orders`, round(sum(total_price),2) as `Total Revenue`
        from dim_orders group by `Order Date`;'''

        sales_table = run_query(query)

        st.subheader("Daily Sales Summary Table")

        st.table(sales_table)

        logging.debug("Completed Aggregration tables in Sales Analytics")

    if type == "KPI":
         query = '''select round(sum(total_price),2) as actual_price from dim_orders;'''

         price = run_query(query)

         price = price.iloc[0,0]

         fig = go.Figure(go.Indicator(
                                        mode="number",
                                        value=price,
                                        title={"text": "Total Revenue (₹)", "font": {"size": 24}},
                                        number={"font": {"size": 36}},
                                        domain={'x': [0, 1], 'y': [0, 1]}
                                    ))

         st.plotly_chart(fig)

         logging.debug("Completed KPI in Sales Analytics")

elif option == "Customer Insights":
    st.title(":green[Customer Insights Dashboard]")

    type = st.selectbox("Analysis Type ?", ("Please Select","Data mart", "Aggregration tables", "KPI"))

    logging.info(f"Selected {type} in {option}")

    if type == "Data mart":

        query = '''select customer_id, count(order_id) as total_orders, round(sum(product_price * quantity)) as total_revenue,
        (case when count(order_id) = 1 then 'New Customer'
        when count(order_id) between 2 and 5 then 'Returning Customer'
        else 'Loyal Customer' end) as customer_segment from fact_main group by customer_id order by total_revenue desc;'''

        customer_segments = run_query(query)

        fig = px.pie(data_frame = customer_segments, names = "customer_segment", values = "total_revenue", title = "Revenue generated")

        st.plotly_chart(fig)

        query = '''select c.customer_state as `Customer State`, count(f.order_id) as `Total Orders` from dim_customers c inner
        join fact_main f on c.customer_id = f.customer_id
        group by c.customer_state order by `Total Orders` desc;'''

        cities = run_query(query)

        fig = px.bar(cities, x = "Total Orders", y = "Customer State", title = "Number of Orders in each State")

        st.plotly_chart(fig)

        logging.debug("Completed Data mart in Customer Insights")

    elif type == "Aggregration tables":
        query = ''' select c.customer_id as `Customer ID`, count(distinct(o.order_id)) as `Total Orders`, sum(f.product_price) as `Total Spent`, avg(f.product_price) as `Average order value`,
        max(o.order_purchase_timestamp) as `Last Purchase Date` from dim_customers c inner join fact_main f on c.customer_id = f.customer_id
        inner join dim_orders o on f.order_id = o.order_id group by c.customer_id;'''

        customer_behaviour = run_query(query)

        st.subheader("Customer Purchase Behaviour Table")

        st.table(customer_behaviour)

        logging.debug("Completed Aggregration tables in Customer Insights")

    elif type == "KPI":
        query = '''select round(sum(total_price) / count(distinct(order_id)), 2) as avg_order_value from dim_orders;'''

        avg = run_query(query)

        avg = avg.iloc[0,0]

        fig = go.Figure(go.Indicator(
                                        mode="number",
                                        value=avg,
                                        title={"text": "Average Order Value (₹)", "font": {"size": 24}},
                                        number={"font": {"size": 36}},
                                        domain={'x': [0, 1], 'y': [0, 1]}
                                    ))

        st.plotly_chart(fig)

        logging.debug("Completed KPI in Customer Insights")

elif option == "Seller Performance":

    st.title(":orange[Seller Performance Overview]")

    type = st.selectbox("Analysis Type ?", ("Please Select","Data mart", "Aggregration tables", "KPI"))

    logging.info(f"Selected {type} in {option}")

    if type == "Data mart":

        query = '''Select seller_state as `Seller State`, count(*) as Count from dim_sellers group by seller_state'''

        no_of_sellers = run_query(query)

        fig = px.bar(no_of_sellers, x = "Count", y = "Seller State", title = "Number of Sellers in each State")

        st.plotly_chart(fig)


        query = '''select s.seller_state as `Seller State`, round(avg(datediff(o.order_estimated_delivery_date, o.order_purchase_timestamp))) as `Average Delivery Time` from dim_sellers s
        inner join fact_main f on s.seller_id = f.seller_id inner join dim_orders o on f.order_id = o.order_id group by s.seller_state;'''

        avg_del = run_query(query)

        fig = px.bar(avg_del, x = "Seller State", y = "Average Delivery Time", title = "Average Delivery Time(in Days) taken by Sellers in each State")

        st.plotly_chart(fig)

        logging.debug("Completed Data mart in {option}")

    elif type == "Aggregration tables":
        query = '''select s.seller_id as `Seller ID`, count(distinct(o.order_id)) as `Total Orders`, sum(o.total_price) as `Total Revenue`, round(avg(datediff(o.order_estimated_delivery_date, o.order_approved_at)))
        as `Average Delivery Time` from dim_sellers s inner join fact_main f on s.seller_id = f.seller_id inner join dim_orders o on f.order_id = o.order_id where o.order_estimated_delivery_date is not null
        group by s.seller_id;'''

        seller_perf = run_query(query)

        st.subheader("Seller Performance Table")

        st.table(seller_perf)

        logging.debug("Completed Aggregration Tables in {option}")

    elif type == "KPI":
        query = '''select s.seller_id as `Seller ID`, round(avg(datediff(o.order_estimated_delivery_date, o.order_approved_at))) as `Average Delivery Time` from dim_sellers s 
        inner join fact_main f on s.seller_id = f.seller_id inner join dim_orders o on f.order_id = o.order_id where o.order_estimated_delivery_date is not null 
        group by s.seller_id order by `Average Delivery Time`;'''

        Delivery_eff = run_query(query)

        st.subheader("Delivery Efficiency of Sellers")

        st.table(Delivery_eff)

        logging.debug("Completed KPI in {option}")

elif option == "Product Analytics":

    st.title(":violet[Product Performance Dashboard]")

    type = st.selectbox("Analysis Type ?", ("Please Select","Data mart", "Aggregration tables", "KPI"))

    logging.info(f"Selected {type} in {option}")

    if type == "Data mart":
        query = ''' select p.product_id as `Product ID`, p.product_category as `Product Category`, round(sum(f.product_price * f.quantity)) as `Total Revenue`, count(f.order_id) as `Total Orders` from dim_products p inner join fact_main
        f on p.product_id = f.product_id group by p.product_id, p.product_category order by `Total Revenue` desc limit 10; '''

        best_products = run_query(query)

        fig = px.pie(best_products, names = "Product Category", values = "Total Revenue", title = "Top 10 Best Selling Products by Revenue")

        st.plotly_chart(fig)

        query = '''select p.product_category as `Product Category`, count(f.order_id) as `Total Orders`, sum(f.quantity) as `Units Sold`, round(sum(f.quantity * f.product_price)) as `Total Revenue`
        from dim_products p inner join fact_main f on p.product_id = f.product_id group by p.product_category order by `Total Revenue` desc limit 10; '''

        units_sold = run_query(query)

        fig = px.bar(units_sold, x = "Product Category", y = "Units Sold", title = "Total Products Sold in each Category")

        st.plotly_chart(fig)

        logging.debug("Completed Data marts in {option}")

    elif type == "Aggregration tables":
        query = '''select p.product_id as `Product ID`, p.product_category as `Product Category`, sum(f.product_price) as `Total Revenue`, count(distinct(f.order_id)) as `Total Orders`, sum(f.quantity) as `Total Quantity`
        from dim_products p inner join fact_main f on p.product_id = f.product_id group by p.product_id, p.product_category;'''

        top_prod = run_query(query)

        st.subheader("Top Selling Products Aggregation Table")

        st.table(top_prod)

        logging.debug("Completed Aggregration Tables in {option}")

    elif type == "KPI":
        query = '''select p.product_id as `Product ID`, p.product_category as `Product Category`, round(sum(o.total_price),2) as `Total Revenue` from dim_products p inner join
        fact_main f on p.product_id = f.product_id inner join
        dim_orders o on f.order_id = o.order_id group by p.product_id, p.product_category order by `Total Revenue` desc limit 5;'''

        top_5 = run_query(query)

        st.subheader("Best Categories")

        st.table(top_5)

        logging.debug("Completed KPI in {option}")
