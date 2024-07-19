import pandas as pd
import streamlit as st
# import streamlit_authenticator as st_auth
import os
import json
import requests

# Streamlit login form
st.title("Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    response = requests.post("http://localhost:8000/token", data={"username": username, "password": password})
    if response.status_code == 200:
        token = response.json().get("access_token")
        st.session_state.token = token
        st.success("Logged in successfully!")
    else:
        st.error("Login failed")

if "token" in st.session_state:
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    response = requests.get("http://localhost:8000/users/me/", headers=headers)

    if response.status_code == 200:
        data = response.json()
        st.write(data)
    else:
        st.error("Unauthorized access")


# -- UNCOMMENT EVERYTHING BELOW WHEN DONE TESTING -- ##
# MOCK_DATA = 'data/MOCK_DATA.json'
#
# # Configures the default settings of the page.
# st.set_page_config(page_title="crypto_api", layout="wide")
#
#
# st.title('My Cryptocurrency app')
#
#
#

# # -- User Auth -- #
#
#
#
#
#
#
# st_name = st.sidebar.text_input("Enter your name", 'John')
# # st.write(f'Hello {st_name}!')
#
# st.write("Hello", st_name, '!')
#
# # What path is the app located
# # app_location = os.getcwd()
# # st.write("App path: ", app_location)
#
#
# with open(MOCK_DATA, 'r') as file:
#     data_dict = json.load(file)
#
# df = pd.DataFrame(data_dict)
#
#
# def dict_to_list(d):
#     """
#     Helper function to convert column of dicts to column lists
#     """
#     return d['price']
#
#
# # Want to convert the sparklines from dicts to lists
# df['sparkline_in_7d'] = df['sparkline_in_7d'].apply(dict_to_list)
#
# # Add column of false values for favorite checkboxes
# df.insert(0, 'favorite', False)
#
# # data_dict = data_dict.iloc[:, 1:] # Drop db _id column
# columns_to_keep = [
#     'favorite',
#     'market_cap_rank',
#     'image',
#     'id',
#     'current_price',
#     'price_change_percentage_24h',
#     'market_cap',
#     'sparkline_in_7d',
# ]
#
# # Only keep columns we care about
# df = df[columns_to_keep]
#
# # Only allow edits for favorite column, used int 'disabled' for data_editor
# columns_to_edit = ['favorite']
# columns_all = df.columns.to_list()
# columns_not_to_edit = [col for col in columns_all if col not in columns_to_edit]
#
#
# st.data_editor(
#     data=df,
#     width=None,
#     use_container_width=False,
#     height=2000,
#     disabled=columns_not_to_edit,
#     column_config={
#         "favorite": st.column_config.CheckboxColumn(
#             "Favorite?",
#             help="Select your **favorite** currencies.",
#             default=False
#         ),
#         "image": st.column_config.ImageColumn(
#             "Icon", help="Icons for currencies"
#         ),
#         "current_price": st.column_config.NumberColumn(
#             label="current_price",
#             format='$%g',
#             help="USD",
#         ),
#         "price_change_percentage_24h": st.column_config.NumberColumn(
#             label="price_change_percentage_24h",
#             format="%.2f%%",
#         ),
#         "market_cap": st.column_config.NumberColumn(
#             label="market_cap",
#             format="$%g",
#             help="USD",
#         ),
#         "sparkline_in_7d": st.column_config.LineChartColumn(
#             "Last 7 days",
#             help="Line chart for the last 7 days",
#         ),
#
#     },
#     hide_index=True
# )