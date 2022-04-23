"""Connect to the db. I took it out from app.py in order to avoid circular import."""

from pymongo import MongoClient

client: MongoClient = MongoClient("mongodb://localhost:27017")
# connect to db: pneumonia
db = client["pneumonia"]
