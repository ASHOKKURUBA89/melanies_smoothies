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

# Fetch fruit options
try:
    fruit_df = session.table("fruit_options").select("FRUIT_NAME").to_pandas()
    fruit_list = fruit_df["FRUIT_NAME"].tolist()
except Exception as e:
    st.error(f"Error fetching fruit options: {e}")
    fruit_list = []

# Multi-select dropdown
ingredients_list = st.multiselect("Choose up to 5 ingredients:", fruit_list)

# Display selected ingredients
if ingredients_list:
    st.write("Your smoothie will include:", ", ".join(ingredients_list))

# Order submission
if st.button("Submit Order"):
    ingredients_string = ", ".join(ingredients_list)
    try:
        insert_query = f"INSERT INTO smoothies.public.orders (ingredients) VALUES ('{ingredients_string}')"
        session.sql(insert_query).collect()
        st.success("Your Smoothie is ordered! ✅")
    except Exception as e:
        st.error(f"Error submitting order: {e}")
