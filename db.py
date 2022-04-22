"""Migrate data into MongoDB. Time elapsed: ~10:27 and ~42it/s"""

from unicodedata import name
from pymongo import MongoClient
import pandas as pd
import os
from tqdm import tqdm
from chest_radiography import *


def main() -> None:
    """Migrate data into a MongoDB collection."""
    client: MongoClient = MongoClient("mongodb://localhost:27017")
    # connect to db: pneumonia
    db = client["pneumonia"]
    # unique constraint on pid
    db.cxr.create_index("pid", unique=True, name="pid_unique")

    annot_df = pd.read_csv("./pneumonia/annot.csv")
    imgs = os.listdir("./pneumonia/images")

    for i in tqdm(range(len(imgs))):
        pid = imgs[i].split(".")[0]
        doc = get_cxr_document(pid, annot_df)
        db.cxr.insert_one(document=doc)


if __name__ == "__main__":
    main()
