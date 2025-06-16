import os
import time
import shutil
import tempfile
import numpy as np
import streamlit as st
from utils import get_databse, get_databse2, build_data, build_data2, sendmail, load_lottieurl
from collections import defaultdict, Counter
import cv2
import face_recognition
from sklearn.cluster import DBSCAN
from imutils import build_montages
import yaml
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import pickle as pkl


database2=get_databse2()
cfg = yaml.load(open('config.yaml','r'),Loader=yaml.FullLoader)
PKL_PATH = cfg['PATH']['PKL_PATH']
PKL_PATH2 = cfg['PATH']['PKL_PATH2']
information=defaultdict(dict)
#body_html_path="C:/Users/Abrar sharif/OneDrive/Desktop/hackrevolution2023/mailtemplate.html"
subject="here are your photos"
namel=[]
listid=[]
lottie_coding = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json")
lottie_photography = load_lottieurl("https://lottie.host/d748dad9-3ac5-4fb7-bcfb-641e553f2330/utgv65gwdt.json")
img_path="assets/imgr.png"






flag1 = 0

st.set_page_config(layout = 'wide')
col1, col2, col3 = st.columns([2.3, 1, 2]) # Add an image to the middle column
col2.image(img_path, width=100)

st.markdown("<h1 style='text-align: center; color: grey;'>SnapSort AI</h1>", unsafe_allow_html=True)
with st.container():
  left_column, right_column = st.columns(2)
  with left_column:
   st.text(" ")
   st.text("Seamleassly Connect with Your Loved ones!")
   st.text("Please wait a while after uploading the images until")
   st.text("you see a dialog box stating that the images were")
   st.text("uploaded successfully.")
   st.text("Sometimes Streamlit takes unusually more time to")
   st.text("upload the images...")
   st.text("if failed, try compressing the images before uploading.")
  with right_column:
    st_lottie(lottie_photography, height=300, key="photography")
with st.container():
  st.write("---")
  left_column, right_column = st.columns(2)
  with left_column:
    st.header("What We do")
    st.write("##")
    st.write(
            """
            Here we help photographers :
            - Looking for a way for distribution of photos easily to the clients.
            - Securely transmitting photos.
            - Fast and Smooth service.

            If this sounds interesting to you, 
            Try it out !!
            """
        )
       
  with right_column:
    st_lottie(lottie_coding, height=300, key="coding")

uploaded_files = st.file_uploader("", type = ["png","jpg","jpeg"], accept_multiple_files = True)

no_of_files = len(uploaded_files)

if no_of_files > 0:
  placeholder = st.empty()
  placeholder.success("{} Images uploaded successfully!".format(no_of_files))
  time.sleep(3)
  placeholder.empty()
  data = []
  
  for f in uploaded_files:
    tfile = tempfile.NamedTemporaryFile(delete = False)
    tfile.write(f.read())
    image = cv2.imread(tfile.name)
    #print("[INFO] processing image {}/{}".format(len(image)))
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb, model = "cnn")
    encodings = face_recognition.face_encodings(rgb, boxes)
    d = [{"imagePath": tfile.name, "loc": box, "encoding": enc} for (box, enc) in zip(boxes, encodings)]
    print("LL")#to check the progress of files encoded


    data.extend(d)
  
  

    
    
    
  
  # converting the data into a numpy array
  data_arr = np.array(data)
  
 
  # extracting the 128-d facial encodings and placing them in a list
  encodings_arr = [item["encoding"] for item in data_arr]

    
  

  # initializing and fitting the clustering model on the encoded data
  cluster = DBSCAN(min_samples=3)
  cluster.fit(encodings_arr)
  st.balloons()
  
  
  labelIDs = np.unique(cluster.labels_)
  numUniqueFaces = len(np.where(labelIDs > -1)[0])
  
  st.subheader("Number of unique faces identified (excluding the unknown faces) is: " + str(numUniqueFaces))

  if flag1 == 0:
    cols1 = st.columns(numUniqueFaces + 1)
    flag1 = 1

  # loop over the unique face integers
  for labelID in labelIDs:
    idxs = np.where(cluster.labels_ == labelID)[0]
    idxs = np.random.choice(idxs, size = min(15, len(idxs)), replace = False)
    # initializing the list of faces to include in the montage
    faces = []
    # initializing the list of whole_images to include in the zip files of each faces, to be downloaded by the user
    whole_images = []
    
    if labelID != -1:
      dir_name = 'face#{}'.format(labelID + 1)
      os.mkdir(dir_name)

    for i in idxs:
      current_image = cv2.imread(data_arr[i]["imagePath"])
      current_encoding = data_arr[i]["encoding"]
      rgb_current_image = cv2.cvtColor(current_image, cv2.COLOR_BGR2RGB)
      (top, right, bottom, left) = data_arr[i]["loc"]
      current_face = rgb_current_image[top:bottom, left:right]
      current_face = cv2.resize(current_face, (96, 96))
      whole_images.append(rgb_current_image)  
      faces.append(current_face)
      cli = [database2[id]['encoding'] for id in database2.keys()]
      namer = None
      idd=None
      matchess=face_recognition.compare_faces(cli,current_encoding)
      while True in matchess and labelID != -1:
       matchess_ind=matchess.index(True)
       namer=database2[matchess_ind]['name']
       
       idd=database2[matchess_ind]['id']
       break
      #stores the matched names and  email in a list to remove false positives 
      if labelID!=-1:
       namel.append(namer)
       listid.append(idd)
      

      if labelID != -1:
        face_image_name = 'image{}.jpg'.format(i)
        cv2.imwrite(os.path.join(dir_name, face_image_name), current_image)
      
    
    if labelID != -1:
      count1=Counter(namel)
      count2=Counter(listid)
      namer2=max(count1, key=count1.get) #gets the most repeated values in a list (for removing false positives)
      id2=max(count2, key=count2.get)
      zip_path=shutil.make_archive('zip_face#{}'.format(labelID + 1), 'zip', dir_name)
      if namer2!=None:
       zip_path2=shutil.make_archive('zip_{}'.format(namer2), 'zip', dir_name)
      output_folder = 'output/'
      os.makedirs(output_folder, exist_ok=True)
      # deleting the directory and image files contained in it as we need only the zip file which has been created already
      shutil.rmtree('face#{}'.format(labelID + 1))
      if namer2!=None:
       zip_file_name = 'zip_{}.zip'.format(namer2)
       shutil.copy(zip_file_name, output_folder)
       recipient_email=id2
       sendmail(recipient_email,zip_file_name)
       #shutil.rmtree(zip_file_name)
      #this part clears the list for new matched names 
      namel.clear()
      listid.clear()

      
      
      
      
      
    montage = build_montages(faces, (96, 96), (2, 2))[0]

    current_title = "Face #{}:".format(labelID + 1)
    expander_caption = "Images with Face #{}:".format(labelID + 1)
    current_title = "Unknown:" if labelID == -1 else current_title

    with cols1[labelID + 1]:
      st.write(current_title)
      st.image(montage)
    if labelID != -1:
      with st.expander(expander_caption):
        # displaying the images of the current face
        cols2 = st.columns(3)
        for j in range(len(whole_images)):
          with cols2[j%3]:
            st.image(whole_images[j], use_column_width = 'always')
        # providing an option for the user to download folders with images of particular faces after clustering as zip files
        with open("zip_face#{}.zip".format(labelID + 1), "rb") as fp:
          btn = st.download_button(
              label="Download ZIP of Clustered Images with Face #{}".format(labelID + 1),
              data=fp,
              file_name="clustered_faces#{}.zip".format(labelID + 1),
              mime="application/zip"
          )
          
        fp.close()


