# Import required packages
import streamlit as st
# App Title
st.title("🥤 Customize Your Smoothie! 🥤")

st.write("Choose the fruits you want in your custom Smoothie!")

# User input for smoothie name
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
    return Session.builder.configs(connection_parameters).create()

# ✅ Function to Create Snowflake Session (Fixed session initialization)
@st.cache_resource
def create_snowflake_session():
    try:
        return Session.builder.configs(connection_parameters).create()
    except Exception as e:

# Create a Snowflake session (Ensure it's created before use)
session = create_snowflake_session()

# ✅ Ensure session exists before querying Snowflake
fruit_options = []
if session:
    try:
        my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME')).collect()
        fruit_options = [row["FRUIT_NAME"] for row in my_dataframe]  # Extract fruit names
    except Exception as e:
        st.error("❌ Error fetching fruit options from Snowflake: " + str(e))

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
    if st.button("Submit Order") and session:
        try:
            session.sql(my_insert_stmt).collect()
            st.success("✅ Your Smoothie is ordered!")
        except Exception as e:
            st.error("❌ Error inserting order into Snowflake: " + str(e))
