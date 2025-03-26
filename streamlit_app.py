# Import python packages
import streamlit as st

# Write directly to the app
st.title("🥤 Customize Your Smoothie! 🥤")
st.write("Choose the fruits you want in your custom Smoothie!")

# Input for name
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# Snowflake connection
cnx = st.connection("snowflake")
session = cnx.session()

# Retrieve fruit options and convert to a list
my_dataframe = (
    session.table("smoothies.public.fruit_options")
    .select(col("FRUIT_NAME"))
    .to_pandas()  # Convert to pandas for easier handling
)

fruit_options = my_dataframe["FRUIT_NAME"].tolist()

# Multi-select dropdown
ingredients_list = st.multiselect("Choose up to 5 ingredients:", fruit_options)

# Display the selected ingredients
if ingredients_list:
    ingredients_string = ", ".join(ingredients_list)  # Properly format the string
    st.write("Selected Ingredients:", ingredients_string)

# Prepare SQL insert statement (parameterized to avoid SQL injection)
my_insert_stmt = f"INSERT INTO smoothies.public.orders (ingredients) VALUES (%s)"

st.write("SQL Query:", my_insert_stmt)

# Submit button
if st.button("Submit Order"):
    session.sql(my_insert_stmt, params=[ingredients_string]).collect()
    st.success("Your Smoothie is ordered! ✅")
