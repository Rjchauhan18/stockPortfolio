import os
from deta import Deta
from dotenv import load_dotenv
import datetime
import re


def check(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

 
    if(re.fullmatch(regex, email)):
        return "Valid Email"
 
    else:
        return "Invalid Email"

    
load_dotenv(".env")
DETA_KEY = os.environ["DETA_KEY"]
deta= Deta(DETA_KEY)


db=deta.Base("auth")

stock=deta.Base("Stocks")

def insert_user(username,full_name,email,password,db_list=None):
    date_join=str(datetime.datetime.now()) 
    db.put({"key":username,"email":email,"Fullname":full_name,"Password":password,"Date of join":date_join,"db_list":db_list})

def fetch_user():
    users=db._fetch()
        
    l=users[1]['items']
    return l



def fetch_stocks():
    stocks_data=stock._fetch()
    
    dl=stocks_data[1]['items']

    dd={}

    for dt in dl:
        dd[dt["key"]]=dt["symbol"]
    return dd


# get hte information
def get_user(Username):
    """If not found , the function will return None """
    return db.get(Username)


#Update user detail
def Update_db_list(username,db_list):
    db.update(key=username,updates={"db_list":db_list})



# --------------------------JWT SECTION---------------------------

# import jwt

# payload_data = {
#     "sub": "4242",
#     "name": "Rahul Chauhan",
#     "nickname": "Rjc"
# }

# my_secret = 'my_super_secret'

# # token = jwt.encode(
# #     payload=payload_data,
# #     key=my_secret
# # )

# # print(token)

# # first import the module
# from cryptography.hazmat.primitives import serialization
# # read and load the key
# private_key = open('rahul/.ssh/Rjchauhan', 'r').read()
# key = serialization.load_ssh_private_key(private_key.encode(), password=b'Rjchauhan')

# new_token = jwt.encode(
#     payload=payload_data,
#     key=key,
#     algorithm='RS256'
# )

# print(new_token)

# # print(jwt.decode(token, key='my_super_secret', algorithms=['HS256', ]))

# header_data = jwt.get_unverified_header(new_token)

# public_key=open('rahul/.ssh/Rjchauhan','r').read()
# key2=serialization.load_ssh_public_key(public_key.encode())

# print(jwt.decode(
#     jwt=new_token,
#     key=key2,
#     algorithms=['RS256', ]
# ))
"""
#update the information

def update_user(username, updates):
    # If the item is updates , ruturn none. Otherwise an exception is raised
    return db.update(updates, username)

def update_name(name, updates):
    # If the item is updates , ruturn none. Otherwise an exception is raised
    return db.update(updates, name)

def update_passord(password, updates):
    # If the item is updates , ruturn none. Otherwise an exception is raised
    return db.update(updates, password)

#delet some information
def delete_user (username):
    # Always returns none, even if the key does not exits
    return db.delete(username)

def delete_name (name):
    # Always returns none, even if the key does not exits
    return db.delete(name)


def delete_password(password):
    # Always returns none, even if the key does not exits
    return db.delete(password)


def delete_email (email):
    # Always returns none, even if the key does not exits
    return db.delete(email)
"""