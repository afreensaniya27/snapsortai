import streamlit as st
import cv2
from utils import submitNew, load_lottieurl
import numpy as np

asset_lottie= load_lottieurl("https://lottie.host/11ccb959-61a1-4656-a8f9-c4aa65f8aeb6/mfivFh5J0Q.json")
st.set_page_config(layout="wide")
with st.container():
  left_column, right_column = st.columns(2)
  with left_column:
   st.title("SnapSort AI")
   st.text("Get your personalized photos via email")
   st.text("Upload a clear photo in good lighting")
  with right_column:
    st.lottie(asset_lottie, height=150)

#asset_lottie= load_lottieurl("https://lottie.host/11ccb959-61a1-4656-a8f9-c4aa65f8aeb6/mfivFh5J0Q.json")

name=st.text_input("Enter Your name")
id=st.text_input("Enter your Email")
upload = st.radio("Upload image or use webcam",("Upload","Webcam"))
if upload == "Upload":
        uploaded_image = st.file_uploader("Upload",type=['jpg','png','jpeg'])
        
        
        if uploaded_image is not None:
            st.image(uploaded_image)
            submit_btn = st.button("Submit",key="submit_btn")
            if submit_btn:
                if name == "" or id == "":
                    st.error("Please enter name and ID")
                else:
                    ret = submitNew(name, id, uploaded_image)
                    if ret == 1: 
                        st.success("Added")
                        #call the matching and mailing alggrtihm();
                    elif ret==-1:
                         st.error("ni aaya face")

elif upload == "Webcam":
        img_file_buffer = st.camera_input("Take a picture")
        submit_btn = st.button("Submit",key="submit_btn")
        if img_file_buffer is not None:
            # To read image file buffer with OpenCV:
            bytes_data = img_file_buffer.getvalue()
            cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
            if submit_btn: 
                if name == "" or id == "":
                    st.error("Please enter name and ID")
                else:
                    ret = submitNew(name, id, cv2_img)
                    if ret == 1: 
                        st.success("Student Added")
                        #call the matching and mailing alggrtihm();                        