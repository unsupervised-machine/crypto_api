import ast

import pandas as pd
import streamlit as st
import os
import json

MOCK_DATA = 'data/MOCK_DATA.json'

st.title('My first app')

st_name = st.sidebar.text_input("Enter your name", 'John')

# st.write(f'Hello {st_name}!')

st.write("Hello", st_name, '!')

app_location = os.getcwd()

st.write("App path: ", app_location)


with open(MOCK_DATA, 'r') as file:
    data_dict = json.load(file)

df = pd.DataFrame(data_dict)


def dict_to_list(d):
    return d['price']


# Want to convert the sparklines from dicts to lists
df['sparkline_in_7d'] = df['sparkline_in_7d'].apply(dict_to_list)

# data_dict = data_dict.iloc[:, 1:] # Drop db _id column
columns_to_keep = [
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

st.dataframe(
    data=df,
    column_config={
        "image": st.column_config.ImageColumn(
            "Icon", help="Icons for currencies"
        ),
        "sparkline_in_7d": st.column_config.LineChartColumn(
            "Last 7 days",
            help="Line chart for the last 7 days",
        ),
    },
    hide_index=True
)