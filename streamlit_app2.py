# Import python packages
import streamlit as st
## from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col,when_matched

# Write directly to the app
st.title(":cup_with_straw: Pending Smoothie Orders :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie! 
  """
)

##option = st.selectbox('What is your favorite food?', 
##                      ('Banana',  'Strawberries', 'Peaches'))

##st.write('You selected:', option)


st.write('Orders that need to be filled.')
cnx = st.connection("snowflake")
session = cnx.session()
## session = get_active_session()
my_dataframe = session.table("smoothies.public.orders").filter(col("order_filled") == 0).collect()
## st.dataframe(data=my_dataframe, use_container_width=True)

if my_dataframe:
    editable_df = st.data_editor(my_dataframe)

    submitted = st.button('Submit')

    og_dataset = session.table("smoothies.public.orders")
    edited_dataset = session.create_dataframe(editable_df)
    try:
        if submitted:
            og_dataset.merge(edited_dataset,
                        (og_dataset['order_uid'] == edited_dataset['order_uid']),
                        [when_matched().update({'order_filled':edited_dataset['order_filled']})])
            st.success('Someone clicked the button.', icon='👍')
    except:
        st.write('something went wrong.')
else:
    st.success('There are no pending order right now', icon='👍')
