import base64
import sqlite3
import streamlit as st
from datetime import date 
from collections import defaultdict as dd
import pandas as pd
import smtplib
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
    with st.form("my_form"):
        h_mail = text_field("Enter registerd Email id : ")
        options = [" ","View bookings", "Ratings", "Achievements"]
        comp = (st.selectbox('Choose options : ',(options)))
        link = text_field("Enter the meeting link (if you have meeting today) : ")
        submit = st.form_submit_button(label="Submit")
    if submit:
        today = date.today()
        cursor.execute("SELECT r_email, h_time from meeting where h_email = (?) and h_date = (?)", (h_mail,today))
        if(comp == "View bookings"):
            ans = cursor.fetchall()
            dicti = dd(list)
            options = []
            for x in ans:
                dicti["Email"].append(x[0])
                options.append(x[0])
                dicti["Time"].append(x[1])
            df = pd.DataFrame(dicti)
            st.table(dicti)
            if(len(dicti) != 0):
                try:
                    h_msg = "Hello,\nWe are happy that you wish to enrich your knowledge with our human libraries.\nGet ready for an exciting meeting.\nHere is your link\n"+link 
                    myemail = "humanlibraryadmn@gmail.com"
                    mypassword = "adminhl@123"  
                    for to_address in options:
                        connection = smtplib.SMTP("smtp.gmail.com", 587)
                        connection.ehlo()
                        connection.starttls()
                        connection.ehlo()
                        connection.login(user = myemail, password = mypassword)
                        connection.sendmail(from_addr = myemail, to_addrs = to_address, msg = h_msg)
                        st.text("mail sent")
                        connection.close()
                except:
                    st.text("")
        elif(comp == "Ratings"):
            cursor.execute("SELECT h_rate from hl WHERE h_email = (?)", (h_mail,))
            ans = cursor.fetchone()
            st.text("Your Rating is : ")
            st.text(ans[0])
        elif(comp == "Achievements"):
            cursor.execute("SELECT COUNT(*) FROM meeting where h_email = (?)", (h_mail,))
            n = cursor.fetchone()
            if(n[0] != 0):
                st.text("Hey!!! See how much meetings you have completed")
                st.text("Its....")
                st.text(n[0])
                st.text("Congrats Human Library")
                st.text("You can request your certificate from humanlibraryadmn@gmail.com")
            else:
                st.text("Complete meetings to achieve")
    sqliteConnection.commit()
    sqliteConnection.close()