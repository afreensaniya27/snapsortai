import mysql.connector as sql
import random
import string
try: 
 conn=sql.connect(host="localhost",user="root",password="tiger")
 print(conn)
except Exception as e:
    print("Error in connection",e)

cursor=conn.cursor()
cursor.execute("create database if not exists photosyncstudio")

def generate_random_string(length=6):
  chars = string.ascii_letters + string.digits
  result = ''.join(random.choice(chars) for _ in range(length))
  return result

# Generate a random 6-digit string
def createnewevent():
  random_string = generate_random_string()
  cursor.execute("CREATE TABLE IF NOT EXISTS your_table_name (id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255) NOT NULL, encodings_file BLOB NOT NULL, unique_id VARCHAR(255) NOT NULL UNIQUE)")
  conn.commit()
  return random_string
