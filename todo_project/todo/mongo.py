# todo/mongo.py

from pymongo import MongoClient

def get_db():
    client = MongoClient('mongodb://localhost:27017/')  # Update with your MongoDB connection string
    return client['todo_db']  # Use your desired database name
