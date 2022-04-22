"""Chest Radiography (CXR) Image object and methods."""

from typing import Any
from PIL import Image
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib import patches
from pandas import DataFrame
from io import BytesIO
import numpy as np
from app import db


class CXR:
    """Chest Radiography."""

    def __init__(self, pid: str) -> None:
        """Init a CXR object."""
        self._pid = pid
        cxr_record = db.cxr.find_one({"pid": pid})
        if cxr_record:
            self._img = cxr_record["img"]
            self._diagnose = cxr_record["diagnose"]
            self._x = cxr_record["x"]
            self._y = cxr_record["y"]
            self._width = cxr_record["width"]
            self._height = cxr_record["height"]

    @property
    def img(self) -> Image:
        """Getter of img."""
        img = Image.open(BytesIO(self._img))
        return img

    @property
    def mark_symptoms(self) -> Figure:
        """Produce bounding boxes for the symptometic area on the CXR image, and display."""
        fig, ax = plt.subplots()
        ax.imshow(self.img, cmap="gray")
        num_box = len(self._x)
        for i in range(num_box):
            rect = patches.Rectangle(
                (self._x[i], self._y[i]),
                self._width[i],
                self._height[i],
                linewidth=1,
                edgecolor="r",
                facecolor="none",
            )
            ax.add_patch(rect)
        plt.show()
        return fig

    @property
    def get_symptom_areas(self) -> Figure:
        """Clip out the symptom areas."""
        n = len(self._x)
        fig, ax = plt.subplots(1, n)
        for i in range(len(ax)):
            box = (
                self._x[i],
                self._y[i],
                self._x[i] + self._width[i],
                self._y[i] + self._height[i],
            )
            clip = self._img.crop(box)
            ax[i].imshow(clip, cmap="gray")
        return fig


class CXRMissingException(Exception):
    """Exception is raised when CXR for a given patient is missing."""

    def __init__(self, *args: object) -> None:
        """Initialize."""
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self) -> str:
        """Output string."""
        if self.message:
            return "{0}".format(self.message)
        else:
            return "a CXRMissingException has been raised."


def img_to_bytes(img: Image) -> bytes:
    """Convert the .jpg image to data in bytes so that it can be saved into MongDB."""
    image_bytes = BytesIO()
    img.save(image_bytes, format="JPEG")
    return image_bytes.getvalue()


def get_cxr_document(pid: str, annot_df: DataFrame) -> dict:
    """Convert a subset of dataframe a dict document."""
    # subset the dataframe
    cxr_df = annot_df.loc[annot_df["patientId"] == pid].drop("patientId", axis=1)
    # check if there is observation
    if cxr_df.shape[0] == 0:
        raise CXRMissingException(f"patient pid:{pid} does not exist")
    cxr_doc: dict[str, Any] = dict()
    cxr_doc["pid"] = pid
    cxr_doc["diagnose"] = int(cxr_df["Target"].values[0])
    img = Image.open(f"./pneumonia/images/{pid}.jpg")
    cxr_doc["img"] = img_to_bytes(img)
    cxr_df = cxr_df.drop("Target", axis=1)
    for col in cxr_df.columns:
        val = cxr_df[col].values.tolist()
        cxr_doc[col] = [] if np.isnan(val[0]) else val
    return cxr_doc
