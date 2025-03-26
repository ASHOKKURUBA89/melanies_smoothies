# Import required packages
import streamlit as st
import snowflake.connector
import pandas as pd


# Write directly to the app
st.title("🥤 Customize Your Smoothie! 🥤")
st.write("Choose the fruits you want in your custom Smoothie!")

# Input for name
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# Snowflake connection (Replace with your credentials OR use Streamlit Secrets)
@st.cache_resource
def create_snowflake_connection():
    return snowflake.connector.connect(
        user="ASHOKKURUBA",
        password="Moveoutnow@123",
        account="ZXIXOIX-UCB52362",
        warehouse="COMPUTE_WH",
        database="SMOOTHIES",
        schema="PUBLIC"
         )

cnx = create_snowflake_connection()
cur = cnx.cursor()

# Retrieve fruit options from Snowflake
cur.execute("SELECT FRUIT_NAME FROM fruit_options")
rows = cur.fetchall()
fruit_options = [row[0] for row in rows]  # Convert tuples to list

# Multi-select dropdown
ingredients_list = st.multiselect("Choose up to 5 ingredients:", fruit_options)

# Display the selected ingredients
if ingredients_list:
    ingredients_string = ", ".join(ingredients_list)  # Properly format the string
    st.write("Selected Ingredients:", ingredients_string)

# Prepare SQL insert statement (Using parameterized query)
if st.button("Submit Order"):
    cur.execute("INSERT INTO orders (ingredients) VALUES (%s)", (ingredients_string,))
    cnx.commit()
    st.success("Your Smoothie is ordered! ✅")

# Close the cursor and connection
cur.close()
cnx.close()
