import pickle as pkl
import yaml
import numpy as np
import face_recognition as frg
import cv2
from collections import defaultdict
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import smtplib
import requests




info=defaultdict(dict)




cfg = yaml.load(open('config.yaml','r'),Loader=yaml.FullLoader)
DATASET_DIR=cfg['PATH']['DATASET_DIR']
PKL_PATH = cfg['PATH']['PKL_PATH']
PKL_PATH2 = cfg['PATH']['PKL_PATH2']

def isFaceExists(image): 
    face_location = frg.face_locations(image)
    if len(face_location) == 0:
        return False
    return True
def get_databse():
    with open(PKL_PATH,'rb') as f:
        database = pkl.load(f)
    return database
def get_databse2():
    with open(PKL_PATH2,'rb') as f:
        database2 = pkl.load(f)
    return database2

        
  

def submitNew(name, id, image, old_idx=None):
    database2 = get_databse2()
    #Read image 
    if type(image) != np.ndarray:
        image = cv2.imdecode(np.fromstring(image.read(), np.uint8), 1)

    isFaceInPic = isFaceExists(image)
    if not isFaceInPic:
        return -1
    #Encode image
    encoding = frg.face_encodings(image)[0]
    #Append to database
    #check if id already exists
    existing_id = [database2[i]['id'] for i in database2.keys()]
    #Update mode 
    if old_idx is not None: 
        new_idx = old_idx
    #Add mode
    else: 
        if id in existing_id:
            return 0
        new_idx = len(database2)
    image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    database2[new_idx] = {'image':image,
                        'id': id, 
                        'name':name,
                        'encoding':encoding}
    try:
     with open(PKL_PATH2,'wb') as f:
        pkl.dump(database2,f)
     return True
    except Exception as e:
        print("dumping issue={}",e)


def build_data():
     
    for image in os.listdir(DATASET_DIR):
        image_path = os.path.join(DATASET_DIR,image)
        image_name = image.split('.')[0]
        parsed_name = image_name.split('_')
        person_id = "krayon461@gmail.com"
        person_name = ' '.join(parsed_name[1:])
        if not image_path.endswith('.jpg'):
            continue
        image = frg.load_image_file(image_path)
        info[0]['image'] = image 
        info[0]['id'] = person_id
        info[0]['name'] = person_name
        info[0]['encoding'] = frg.face_encodings(image)[0]
        

    with open(os.path.join(DATASET_DIR,'database2.pkl'),'wb') as f:
        pkl.dump(info,f)

      
def build_data2():
 for image in os.listdir(DATASET_DIR):
        image_path = os.path.join(DATASET_DIR,image)
        image_name = image.split('.')[0]
        parsed_name = image_name.split('_')
        person_id = "krayon461@gmail.com"
        person_name = ' '.join(parsed_name[1:])
        if not image_path.endswith('.jpg'):
            continue
        image = frg.load_image_file(image_path)
        info[0]['imagepath'] = image_path 
        info[0]['loc'] = frg.face_locations(image)
        info[0]['encoding'] = frg.face_encodings(image)[0]
        

 with open(os.path.join(DATASET_DIR,'database1.pkl'),'wb') as f:
        pkl.dump(info,f)


    
def sendmail(recipient_email,file_path):

    sender_email = "studiophotosync@gmail.com"


    # SMTP server details
    smtp_server = "smtp.gmail.com"
    smtp_port = 587  # Use 465 for SSL/TLS connection

    # Your email account credentials
    smtp_username = "studiophotosync@gmail.com"
    smtp_password = "wfdhblckiujgukpj"
    with open("mailtemplate.html", "r") as template_file:
     template_content = template_file.read()

     html_body = MIMEText(template_content, "html")


    # Create a MIME object
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = "Here are your photos"
    message.attach(html_body)

    # Attach the file
    with open(file_path, "rb") as file:
        attachment = MIMEApplication(file.read())
        attachment.add_header('Content-Disposition', 'attachment', filename='yourphotos.zip')
        message.attach(attachment)

    # Connect to the SMTP server
    try:
     with smtplib.SMTP(smtp_server, smtp_port) as server:
        # Start the TLS connection (if using 587 port)
        server.starttls()
        
        # Login to the email account
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, recipient_email, message.as_string())
     print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")
        
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
 






