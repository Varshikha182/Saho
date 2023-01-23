import base64
import sqlite3
import os
import streamlit as st
from datetime import date 
from collections import defaultdict as dd
import pandas as pd
st.set_page_config(page_title='Book Human Library', page_icon='', layout="wide", initial_sidebar_state="expanded", menu_items=None)

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
    add_bg_from_local('books.jpeg')
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
    options = [" ","Accounting", "Arts", "Beauty", "Biology", "Business Studies", "Chemistry", "Civil", "Commerce", "Communication",
"Computer Science", "Councelling", "Digital Marketing", "Economics", "Health & Fitness", "IT", "Languages", "Leadership",
"Maths", "Mechanical", "Medical", "Music", "Physics", "Psychology", "Sports", "Teaching", "Teamwork"]
    comp = (st.selectbox('Choose the Domain : ',(options)))
    today = date.today()
    cursor.execute("SELECT h_name, h_email, h_time FROM hl where h_domain = (?) and h_meet = (?)", (comp,today))
    dicti = dd(list)
    help = dd(str)
    ans = cursor.fetchall()
    for x in ans: 
        dicti["Name"].append(x[0])
        dicti["Email"].append(x[1])
        dicti["Time"].append(x[2])
        help[x[1]] = x[2]
    df = pd.DataFrame(dicti)
    if(comp != " "):
        if(len(dicti) == 0):
            st.error("Currently human libraries are not available in this domain")
        else:
            st.table(dicti)
            if(comp != " "):
                with st.form("my_form", clear_on_submit=True):
                    u_email = text_field("Enter your Email ID : ")
                    e_mail = text_field("Enter the Email ID of prefered expert : ")
                    submit = st.form_submit_button(label="Submit")
                if(submit):
                    x = help[e_mail]
                    cursor.execute("INSERT INTO meeting(h_email, r_email, h_time, h_date) VALUES(?, ?, ?, ?)",(e_mail, u_email, x, today))
                    st.text("Booking Sucessful link will be shared via Email shortly")
    sqliteConnection.commit()
    sqliteConnection.close()