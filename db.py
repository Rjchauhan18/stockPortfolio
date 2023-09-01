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
DETA_KEY =os.getenv("DETA_KEY")
deta= Deta(DETA_KEY)


db=deta.Base("auth")

stock=deta.Base("Stocks")

def insert_user(username,full_name,email,password):
    date_join=str(datetime.datetime.now()) 
    db.put({"key":username,"email":email,"Fullname":full_name,"Password":password,"Date of join":date_join})

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