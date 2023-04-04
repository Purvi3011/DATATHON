import streamlit as st
st.set_page_config(layout="wide")

import re
import requests
import pandas as pd

import pickle
food_options=pickle.load(open('options.pkl','rb'))

st.title("Global Foods Recommender")
question = st.selectbox("Search your food item here",food_options)
body = {"name":"Bean salad"}

if st.button("Recommend"):
    url = "http://hfkhsdfh98y.pythonanywhere.com/recommend"
    data = {"name": question}
    headers = {"Content-type": "application/json"}
    response = requests.post(url, json=data, headers=headers)
    df = pd.DataFrame(response.json())
    df.columns = ["Results"]
    st.dataframe(df)