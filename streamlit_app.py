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
# Display the selected ingredients
if ingredients_list:
    ingredients_string=''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen +' '

    st.write(ingredients_string)

my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
            values ('""" + ingredients_string + """')"""

st.write(my_insert_stmt)

time_to_insert = st.button('Submit Order')

if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon='✅')
