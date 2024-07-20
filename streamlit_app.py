import pandas as pd
import streamlit as st
# import streamlit_authenticator as st_auth
import os
import json
import requests


# # Configures the default settings of the page.
st.set_page_config(page_title="crypto_api", layout="wide")
# Streamlit login form
st.title("Login")




# if "token" in st.session_state:
    # st.markdown("### Logged in")
    #
    # headers = {"Authorization": f"Bearer {st.session_state.token}"}
    # response = requests.get("http://localhost:8000/users/me/", headers=headers)

    # if response.status_code == 200:
    #     data = response.json()
    #     st.write(data)
    # else:
    #     st.error("Unauthorized access")
    #
    # if st.sidebar.button("Logout"):
    #     del st.session_state.token
    #     st.rerun()
        # st.success("Logged out successfully!")


# -- User Auth Portion of App -- #

with st.popover("Sign In"):
    with st.form("Signin Form", clear_on_submit=True):
        username = st.text_input("username")
        plain_password = st.text_input("Password")
        submitted = st.form_submit_button("Submit")

        response = requests.post("http://localhost:8000/token", data={"username": username, "password": plain_password})

        if submitted:
            if response.status_code == 200:
                token = response.json().get("access_token")
                st.session_state.token = token
                st.session_state.username = username
                headers = {"Authorization": f"Bearer {st.session_state.token}"}
                st.success("Logged in successfully!")
            else:
                st.error("Login failed")


with st.popover("Sign Up"):
    with st.form("Signup Form", clear_on_submit=True):
        email = st.text_input("Email")
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        username = st.text_input("Username")
        plain_password = st.text_input("Password")
        submitted = st.form_submit_button("Submit")

        response = requests.post(url="http://localhost:8000/signup",
                                 data={"email": email,
                                       "first_name": first_name,
                                       "last_name": last_name,
                                       "username": username,
                                       "plain_password": plain_password,
                                       }
                                 )

        if submitted:
            if response.status_code == 200:
                st.success("Successfully registered.")

                response = requests.post("http://localhost:8000/token",
                                         data={"username": username, "password": plain_password})
                if submitted:
                    if response.status_code == 200:
                        token = response.json().get("access_token")
                        st.session_state.token = token
                        st.session_state.username = username
                        headers = {"Authorization": f"Bearer {st.session_state.token}"}
                        if st.session_state.token:
                            st.success("Logged in successfully!")
                    else:
                        st.error("Login failed")

            else:
                st.error("Registration failed")

if "token" in st.session_state:
    with st.popover("Log out"):
        with st.form("Logout Form"):
            submitted = st.form_submit_button("Log out")

            if submitted:
                st.success("Logged out successfully!")
                del st.session_state.token
                st.rerun()


# if user is logged in get their favorites portfolio
if "token" in st.session_state and st.session_state.username:
    st.write(st.session_state.token)
    response = requests.get("http://localhost:8000/users/me/favorites",
                            data={"username": username},
                            headers = {"Authorization": f"Bearer {st.session_state.token}"})
    data = response.json()
    st.write(data)

# -- Crypto portion of app -- #
st.title('My Cryptocurrency app')

MOCK_DATA = 'data/MOCK_DATA.json'
with open(MOCK_DATA, 'r') as file:
    data_dict = json.load(file)

df = pd.DataFrame(data_dict)


def dict_to_list(d):
    """
    Helper function to convert column of dicts to column lists
    """
    return d['price']


# Want to convert the sparklines from dicts to lists
df['sparkline_in_7d'] = df['sparkline_in_7d'].apply(dict_to_list)

# Add column of false values for favorite checkboxes
df.insert(0, 'favorite', False)

# data_dict = data_dict.iloc[:, 1:] # Drop db _id column
columns_to_keep = [
    'favorite',
    'market_cap_rank',
    'image',
    'id',
    'current_price',
    'price_change_percentage_24h',
    'market_cap',
    'sparkline_in_7d',
]

# Only keep columns we care about
df = df[columns_to_keep]

# Only allow edits for favorite column, used int 'disabled' for data_editor
columns_to_edit = ['favorite']
columns_all = df.columns.to_list()
columns_not_to_edit = [col for col in columns_all if col not in columns_to_edit]


st.data_editor(
    data=df,
    width=None,
    use_container_width=False,
    height=2000,
    disabled=columns_not_to_edit,
    column_config={
        "favorite": st.column_config.CheckboxColumn(
            "Favorite?",
            help="Select your **favorite** currencies.",
            default=False
        ),
        "image": st.column_config.ImageColumn(
            "Icon", help="Icons for currencies"
        ),
        "current_price": st.column_config.NumberColumn(
            label="current_price",
            format='$%g',
            help="USD",
        ),
        "price_change_percentage_24h": st.column_config.NumberColumn(
            label="price_change_percentage_24h",
            format="%.2f%%",
        ),
        "market_cap": st.column_config.NumberColumn(
            label="market_cap",
            format="$%g",
            help="USD",
        ),
        "sparkline_in_7d": st.column_config.LineChartColumn(
            "Last 7 days",
            help="Line chart for the last 7 days",
        ),

    },
    hide_index=True
)