# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

# option = st.selectbox(
#     "How would you like to be contacted?",
#     ("Email", "Home phone", "Mobile phone"),
# )
# st.write("you have selected:", option)

# fruits = st.selectbox(
#     "Which fruits you want in your custom Smoothie??",
#     ('Apple', 'Banana','Pine-apple')
# )
# st.write('Your favourite fruit is:', fruits)

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be: ", name_on_order)

# session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True);
# my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()
ingrediant_list = st.multiselect(
    'Choose upto 5 elements:',
    my_dataframe,
    max_selections=5
)

if ingrediant_list:
    # st.write(ingrediant_list)
    # st.text(ingrediant_list)
    ingrediant_string = ''

    for fruit_chosen in ingrediant_list:
         ingrediant_string += fruit_chosen+ ' '
    st.write(ingrediant_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingrediant_string + """','""" + name_on_order +"""')"""

    # st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered '+ name_on_order+'!', icon="✅")


import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response.json())

