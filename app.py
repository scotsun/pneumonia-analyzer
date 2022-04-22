"""Application front-end."""

# TODO: GUI front-end

from pymongo import MongoClient

client: MongoClient = MongoClient("mongodb://localhost:27017")
# connect to db: pneumonia
db = client["pneumonia"]
