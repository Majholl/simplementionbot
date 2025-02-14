import pymongo
import os 
from dotenv import load_dotenv

load_dotenv()
DATABASEURL = os.getenv('DBURL')

def makeDBoperations():
    myclient = pymongo.MongoClient(DATABASEURL)
    mydb = myclient['simplemention']
    mycoll = mydb['users']
    return mycoll