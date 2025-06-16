import streamlit as st
import yaml
from datetime import datetime
import pandas as pd
from utils import build_data, build_data2
import time 
import os
st.title("Admin Login")
username=st.text_input("Username")
password=st.text_input("Password", type="password")

################################### this page is used for rebuilding pickle files ##########################################################3

def auth(username, password):
    if username=="admin" and password=="admin": # current username and password 
     #use elif here for multiple users
     return True
    else:
     return False
    

if st.button("Login"):
   if auth(username, password):
      st.success(f"Login successful, Welcome back {username}")#success message with username
      st.text("Rebuild database2")
      submit_button = st.button(label='REBUILD DATASET2')
      st.text("Rebuild database1 ")
      submit_button2=st.button(label='REBUILD DATASET 1 (fr)')
      if submit_button:
        with st.spinner("Rebuilding dataset..."):
            build_data()
        st.success("Dataset has been reset")
      elif submit_button2:
         with st.spinner("Rebuilding dataset..."):
          build_data2()
         st.success("Dataset has been rest")
   else:
     st.error("Please enter Login Details.")





    
 
  







