import base64
import sqlite3
import streamlit as st
from datetime import date 
from collections import defaultdict as dd
import pandas as pd
st.set_page_config(page_title='View Meetings', page_icon='', layout="wide", initial_sidebar_state="expanded", menu_items=None)
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
def text_field(label, columns=None, **input_params):
    c1, c2 = st.columns(columns or [1, 4])
    c1.markdown("##")
    c1.markdown(label)
    input_params.setdefault("key", label)
    return c2.text_input("", **input_params)
if __name__ == '__main__':
    add_bg_from_local('image3.jpg')
    sqliteConnection = sqlite3.connect('libys.db')
    cursor = sqliteConnection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS meeting(
        h_email VARCHAR(50),
        r_email VARCHAR(50),
        h_time VARCHAR(15),
        h_date DATE,
        h_link VARCHAR(100)
    );
    """)
    cursor.execute("SELECT h_email FROM meeting")
    options = [" "]
    ans = cursor.fetchall()
    for x in ans:
        options.append(x[0])
    with st.form("my_form", clear_on_submit=True):
        comp = (st.selectbox('Choose Mail id of Human Library : ',(options)))
        ratings = st.number_input("Enter ratings out of 5")
        submit = st.form_submit_button(label="Submit")
    if submit:
        cursor.execute("SELECT h_rate from hl WHERE h_email = (?)", (comp,))
        rate = cursor.fetchone()[0]
        if(rate != None):
            ratings = (rate + ratings)/2
        st.text(ratings)
        cursor.execute("UPDATE hl SET h_rate = (?) WHERE h_email = (?)", (ratings, comp))
    sqliteConnection.commit()
    sqliteConnection.close()