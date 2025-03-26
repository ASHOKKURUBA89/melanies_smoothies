# Import necessary packages
import streamlit as st
import snowflake.connector
from snowflake.snowpark.session import Session
from snowflake.snowpark.functions import col

# Streamlit Title
st.title("🥤 Customize Your Smoothie! 🥤")
st.write("Choose the fruits you want in your custom Smoothie!")

# Text Input for Smoothie Name
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# Snowflake connection function
@st.cache_resource
def create_snowflake_session():
    connection_parameters = {
        "account": "ZXIXOIX-UCB52362",
        "user": "ASHOKKURUBA",
        "password": "Moveoutnow@123",
        "warehouse": "COMPUTE_WH",
        "database": "SMOOTHIES",
        "schema": "PUBLIC",
    }
    # Function to Create Snowflake Session
@st.cache_resource
def create_snowflake_session():
    return Session.builder.configs(connection_parameters).create()

# Create a Snowflake session
session = create_snowflake_session()

# Fetch Fruit Options from Snowflake
try:
    my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME')).collect()
    fruit_options = [row["FRUIT_NAME"] for row in my_dataframe]  # Extract fruit names
except Exception as e:
    st.error("Error fetching fruit options from Snowflake: " + str(e))
    fruit_options = []

# Multi-Select Dropdown for Ingredients
ingredients_list = st.multiselect("Choose up to 5 ingredients:", fruit_options)

# Display Selected Ingredients
if ingredients_list:
    ingredients_string = ", ".join(ingredients_list)
    st.write("Your chosen ingredients:", ingredients_string)

    # Construct SQL Insert Statement
    my_insert_stmt = f"INSERT INTO smoothies.public.orders(ingredients) VALUES ('{ingredients_string}')"

    # Show Insert Statement for Debugging
    st.write("SQL Query:", my_insert_stmt)

    # Submit Order Button
    if st.button("Submit Order"):
        try:
            session.sql(my_insert_stmt).collect()
            st.success("Your Smoothie is ordered! ✅")
        except Exception as e:
            st.error("Error inserting order into Snowflake: " + str(e))
