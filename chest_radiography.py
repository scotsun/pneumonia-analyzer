"""Chest Radiography (CXR) Image object and methods."""


from typing import Any
from PIL import Image
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib import patches
from pandas import DataFrame
from io import BytesIO
import numpy as np
from db import db


class CXR:
    """Chest Radiography."""

    def __init__(self, pid: str) -> None:
        """Init a CXR object."""
        self._pid = pid
        cxr_record = db.cxr.find_one({"pid": pid})
        self._is_diagnosed = False
        if cxr_record:
            self._img = cxr_record["img"]
            self._diagnose = cxr_record["diagnose"]
            self._x = cxr_record["x"]
            self._y = cxr_record["y"]
            self._width = cxr_record["width"]
            self._height = cxr_record["height"]
            self._is_diagnosed = True

    @property
    def pid(self) -> str:
        """Getter of self._pid."""
        return self.pid

    @property
    def img(self) -> Image:
        """Getter of img as an Image class."""
        if not self.is_diagnosed:
            raise CXRMissingException(
                f"patient pid:{self._pid} does not exist in the db."
            )
        img = Image.open(BytesIO(self._img))
        return img

    @property
    def is_diagnosed(self) -> bool:
        """Getter of self._is_diagnosed."""
        return self._is_diagnosed

    @property
    def mark_symptoms(self) -> Figure:
        """Produce bounding boxes for the symptometic area on the CXR image, and display.

            x,y ------> (width)
            |
            |  (Left,Top)
            |       *_________
            |       |         |
            |       |         |
                    |_________|
        (height)              *
                        (Right,Bottom)
        """
        if not self.is_diagnosed:
            raise AttributeError("CXR has not been diagnosed yet.")
        fig, ax = plt.subplots()
        ax.imshow(self.img, cmap="gray")
        n = len(self._x)
        for i in range(n):
            rect = patches.Rectangle(
                (self._x[i], self._y[i]),
                self._width[i],
                self._height[i],
                linewidth=1,
                edgecolor="r",
                facecolor="none",
            )
            ax.add_patch(rect)
        plt.axis("off")
        plt.close()
        return fig

    @property
    def get_symptom_areas(self) -> Figure:
        """Clip out the symptom areas."""
        if not self.is_diagnosed:
            raise AttributeError("CXR has not been diagnosed yet.")
        n = len(self._x)
        if n == 0:
            raise AttributeError("CXR record does not show inflammation.")
        fig, ax = plt.subplots(1, n)
        for i in range(len(ax)):
            box = (
                self._x[i],
                self._y[i],
                self._x[i] + self._width[i],
                self._y[i] + self._height[i],
            )
            clip = self.img.crop(box)
            ax[i].imshow(clip, cmap="gray")
        plt.axis("off")
        plt.close()
        return fig


class CXRMissingException(Exception):
    """Exception is raised when CXR for a given patient is missing in the annotations or the db."""

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
        raise CXRMissingException(f"patient pid:{pid} does not exist.")
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


if __name__ == "__main__":
    cxr = CXR(pid="00436515-870c-4b36-a041-de91049b9ab4")
    f = cxr.mark_symptoms
    print(f)
