"""Chest Radiography (CXR) Image object and methods."""

from PIL import Image
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib import patches
from pandas import DataFrame
import io
import numpy as np


class CXR:
    """Chest Radiography."""

    def __init__(
        self,
        pid: str,
        x: list[float],
        y: list[float],
        width: list[float],
        height: list[float],
        diagnose: bool,
        source: str,
    ) -> None:
        """Init a CXR object."""
        img = Image.open(f"./pneumonia/{source}/{pid}.jpg")
        self._pid = pid
        self._img = img
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._dignose = diagnose

    @property
    def img(self) -> Image:
        """Getter of img."""
        return self._img

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


def get_cxr_document(pid: str, annot_df: DataFrame) -> dict:
    """Convert a subset of dataframe a dict document."""
    # subset the dataframe
    cxr_df = annot_df.loc[annot_df["patientId"] == pid].drop("patientId", axis=1)
    # check if there is observation
    if cxr_df.shape[0] == 0:
        raise CXRMissingException(f"patient pid:{pid} does not exist")
    cxr_doc: dict[str, str | int | list[float]] = dict()
    cxr_doc["pid"] = pid
    cxr_doc["diagnose"] = int(cxr_df["Target"].values[0])
    cxr_df = cxr_df.drop("Target", axis=1)
    for col in cxr_df.columns:
        val = cxr_df[col].values.tolist()
        cxr_doc[col] = [] if np.isnan(val[0]) else val
    return cxr_doc


def convert_img_to_bytes(img: Image):
    """Convert the .jpg image to data in bytes so that it can be saved into MongDB."""
    pass
