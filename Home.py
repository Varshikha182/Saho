import streamlit as st
import base64
st.set_page_config(page_title='Register', page_icon='', layout="wide", initial_sidebar_state="expanded", menu_items=None)
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
add_bg_from_local('image7.jpg')
original_title = '<p style="font-family:Georgia; color:white; font-size: 45px;">Human Library World</p>'
st.markdown(original_title, unsafe_allow_html=True)
with st.expander('', expanded=True):
    st.markdown(f'''
    <ul>
      <li style="color:white;"><p style="font-size:25px; font-family:Georgia; color:LightBlue;">Knowledge is like a garden. If it is not cultivated, it cannot be harvested.<p>
      </li>
      <li style="color:white;"><p style="font-size:25px; font-family:Georgia; color:LightBlue;">Stay anywhere and get connected virtually with our experts.</p> 
      <li style="color:white;"><p style="font-size:25px; font-family:Georgia; color:LightBlue;">Get Set Go... Become a Human Library.</p>
    </ul>
    ''', unsafe_allow_html=True)