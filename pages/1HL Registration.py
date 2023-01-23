import streamlit as st
import base64
from PIL import Image
import sqlite3
from datetime import date
from datetime import datetime
st.set_page_config(page_title='Human Library Registration', page_icon='', layout="wide", initial_sidebar_state="expanded", menu_items=None)
def text_field(label, columns=None, **input_params):
    c1, c2 = st.columns(columns or [1, 4])
    c1.markdown("##")
    c1.markdown(label)
    input_params.setdefault("key", label)
    return c2.text_input("", **input_params)
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
add_bg_from_local('image3.jpg')
sqliteConnection = sqlite3.connect('libys.db')
cursor = sqliteConnection.cursor()
sql_command = """CREATE TABLE IF NOT EXISTS hl (
h_name VARCHAR(50),
h_domain VARCHAR(100),
h_email VARCHAR(100),
h_meet DATE,
h_time VARCHAR(20),
h_rate FLOAT,
h_n INTEGER);"""
cursor.execute(sql_command)
original_title = '<p style="font-family:Georgia; color:#31704d; font-size: 60px;">Register your next meeting !!!</p>'
st.markdown(original_title, unsafe_allow_html=True)
with st.form("my_form", clear_on_submit=True):
    name = text_field("Name : ")
    email = text_field("Email : ")
    options = [" ","Accounting", "Arts", "Beauty", "Biology", "Business Studies", "Chemistry", "Civil", "Commerce", "Communication",
"Computer Science", "Councelling", "Digital Marketing", "Economics", "Health & Fitness", "IT", "Languages", "Leadership",
"Maths", "Mechanical", "Medical", "Music", "Physics", "Psychology", "Sports", "Teaching", "Teamwork"]
    comp = (st.selectbox('Select your domain of Expertise : ',(options)))
    today = date.today()
    d = st.date_input("Select the date you are available :")
    now = datetime.now()
    t = str(st.time_input("Select the meeting time :", now))
    cursor.execute("INSERT INTO hl(h_name, h_domain, h_email, h_meet, h_time) values(?, ?, ?, ?, ?)", (name, comp, email, d, t))
    submit = st.form_submit_button(label="Submit")
    sqliteConnection.commit()
    sqliteConnection.close()
