"""Migrate data into MongoDB."""

from unicodedata import name
from pymongo import MongoClient
import pandas as pd
import numpy as np
import os
from chest_radiography import *


def main() -> None:
    """Migrate data into a MongoDB collection."""
    client: MongoClient = MongoClient("mongodb://localhost:27017")

    annot_df = pd.read_csv("./pneumonia/annot.csv")
    imgs = os.listdir("./pneumonia/images")


if __name__ == "__main__":
    main()
