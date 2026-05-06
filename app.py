import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Title
st.title("Uber Eats Data Analysis App")

# Connect to MySQL
engine = create_engine("mysql+pymysql://root:@localhost/uber_eats_db")

# Sidebar navigation
page = st.sidebar.selectbox("Select Page", ["Dashboard", "Q&A", "Orders"])

# ================= DASHBOARD =================
if page == "Dashboard":
    st.header("📊 Dashboard Filters")

    # Filters
    location = st.text_input("Enter Location")
    online_order = st.selectbox("Online Order", ["All", "Yes", "No"])
    book_table = st.selectbox("Table Booking", ["All", "Yes", "No"])
    min_rating = st.slider("Minimum Rating", 0.0, 5.0, 0.0)

    # Button
    if st.button("Apply Filters"):

        query = """
        SELECT * FROM cleaned_uber_eats_data
        WHERE 1=1
        """

        # Dynamic filters
        if location:
            query += f" AND location LIKE '%{location}%'"

        if online_order != "All":
            query += f" AND online_order = '{online_order}'"

        if book_table != "All":
            query += f" AND book_table = '{book_table}'"

        if min_rating > 0:
            query += f" AND rating >= {min_rating}"

        # Execute
        df = pd.read_sql(query, engine)
        st.dataframe(df)

# =========================
# Q&A PAGE
# =========================
elif page == "Q&A":
    st.header("📊 Business Questions & Insights")

    # Q1
    st.subheader("1. Which Bangalore locations have the highest average restaurant ratings?")
    st.write("Business Value: Identifies premium-performing areas for expansion.")
    if st.button("Run Q1"):
        query = """
        SELECT location, AVG(rating) AS avg_rating
        FROM cleaned_uber_eats_data
        GROUP BY location
        ORDER BY avg_rating DESC
        LIMIT 10
        """
        st.dataframe(pd.read_sql(query, engine))

    # Q2
    st.subheader("2. Which locations are over-saturated with restaurants?")
    st.write("Business Value: Helps avoid overcrowded markets.")
    if st.button("Run Q2"):
        query = """
        SELECT location, COUNT(*) AS total_restaurants
        FROM cleaned_uber_eats_data
        GROUP BY location
        ORDER BY total_restaurants DESC
        LIMIT 10
        """
        st.dataframe(pd.read_sql(query, engine))

    # Q3
    st.subheader("3. Does online ordering improve restaurant ratings?")
    st.write("Business Value: Evaluates ROI of online ordering.")
    if st.button("Run Q3"):
        query = """
        SELECT online_order, AVG(rating) AS avg_rating
        FROM cleaned_uber_eats_data
        GROUP BY online_order
        """
        st.dataframe(pd.read_sql(query, engine))

    # Q4
    st.subheader("4. Does table booking correlate with higher ratings?")
    st.write("Business Value: Measures effectiveness of premium features.")
    if st.button("Run Q4"):
        query = """
        SELECT book_table, AVG(rating) AS avg_rating
        FROM cleaned_uber_eats_data
        GROUP BY book_table
        """
        st.dataframe(pd.read_sql(query, engine))

    # Q5
    st.subheader("5. What price range delivers the best customer satisfaction?")
    st.write("Business Value: Identifies optimal pricing segment.")
    if st.button("Run Q5"):
        query = """
        SELECT cost, AVG(rating) AS avg_rating
        FROM cleaned_uber_eats_data
        GROUP BY cost
        ORDER BY avg_rating DESC
        LIMIT 10
        """
        st.dataframe(pd.read_sql(query, engine))

    # Q6
    st.subheader("6. How do low, mid, and premium-priced restaurants perform?")
    st.write("Business Value: Helps pricing segmentation strategy.")
    if st.button("Run Q6"):
        query = """
        SELECT 
            CASE 
                WHEN cost < 300 THEN 'Low'
                WHEN cost BETWEEN 300 AND 700 THEN 'Mid'
                ELSE 'Premium'
            END AS price_category,
            AVG(rating) AS avg_rating
        FROM cleaned_uber_eats_data
        GROUP BY price_category
        """
        st.dataframe(pd.read_sql(query, engine))

    # Q7
    st.subheader("7. Which cuisines are most common in Bangalore?")
    st.write("Business Value: Reveals demand and saturation.")
    if st.button("Run Q7"):
        query = """
        SELECT cuisines, COUNT(*) AS count
        FROM cleaned_uber_eats_data
        GROUP BY cuisines
        ORDER BY count DESC
        LIMIT 10
        """
        st.dataframe(pd.read_sql(query, engine))

    # Q8
    st.subheader("8. Which cuisines receive the highest ratings?")
    st.write("Business Value: Identifies high-quality cuisine segments.")
    if st.button("Run Q8"):
        query = """
        SELECT cuisines, AVG(rating) AS avg_rating
        FROM cleaned_uber_eats_data
        GROUP BY cuisines
        ORDER BY avg_rating DESC
        LIMIT 10
        """
        st.dataframe(pd.read_sql(query, engine))

    # Q9
    st.subheader("9. Do restaurants offering both online ordering and table booking perform better?")
    st.write("Business Value: Validates bundled feature effectiveness.")
    if st.button("Run Q9"):
        query = """
        SELECT online_order, book_table, AVG(rating) AS avg_rating
        FROM cleaned_uber_eats_data
        GROUP BY online_order, book_table
        """
        st.dataframe(pd.read_sql(query, engine))

    # Q10
    st.subheader("10. What is the relationship between restaurant cost and rating?")
    st.write("Business Value: Determines if higher price improves perception.")
    if st.button("Run Q10"):
        query = """
        SELECT cost, AVG(rating) AS avg_rating
        FROM cleaned_uber_eats_data
        GROUP BY cost
        ORDER BY cost
        """
        st.dataframe(pd.read_sql(query, engine))


# =========================
# ORDERS PAGE
# =========================
elif page == "Orders":
    st.header("📦 Orders Analysis")

    # Q1
    st.subheader("1. Which restaurants generate the highest revenue?")
    if st.button("Run O1"):
        query = """
        SELECT restaurant_name, SUM(order_value) AS revenue
        FROM orders_data
        GROUP BY restaurant_name
        ORDER BY revenue DESC
        LIMIT 10
        """
        st.dataframe(pd.read_sql(query, engine))

    # Q2
    st.subheader("2. What is the average order value by payment method?")
    if st.button("Run O2"):
        query = """
        SELECT payment_method, AVG(order_value) AS avg_order_value
        FROM orders_data
        GROUP BY payment_method
        """
        st.dataframe(pd.read_sql(query, engine))

    # Q3
    st.subheader("3. Do discounts increase order value?")
    if st.button("Run O3"):
        query = """
        SELECT discount_used, AVG(order_value) AS avg_order_value
        FROM orders_data
        GROUP BY discount_used
        """
        st.dataframe(pd.read_sql(query, engine))

    # Q4   
    st.subheader("4. Monthly order trend")
    if st.button("Run O4"):
    	query = """
    	SELECT DATE_FORMAT(order_date, '%%Y-%%m') AS month, 
        COUNT(*) AS total_orders
    	FROM orders_data
    	GROUP BY month
    	ORDER BY month
    	"""
    	st.dataframe(pd.read_sql(query, engine))

    # Q5
    st.subheader("5. Which payment method is most used?")
    if st.button("Run O5"):
        query = """
        SELECT payment_method, COUNT(*) AS total_orders
        FROM orders_data
        GROUP BY payment_method
        ORDER BY total_orders DESC
        """
        st.dataframe(pd.read_sql(query, engine))

    # Q6
    st.subheader("6. High-value orders (above 1000)")
    if st.button("Run O6"):
        query = """
        SELECT *
        FROM orders_data
        WHERE order_value > 1000
        """
        st.dataframe(pd.read_sql(query, engine))

    # Q7
    st.subheader("7. Discount usage rate")
    if st.button("Run O7"):
        query = """
        SELECT discount_used, COUNT(*) AS count
        FROM orders_data
        GROUP BY discount_used
        """
        st.dataframe(pd.read_sql(query, engine))