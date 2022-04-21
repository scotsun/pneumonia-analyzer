"""Chest Radiography (CXR) Image object and methods."""

from tty import IFLAG
from PIL import Image
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib import patches
from numpy import clip


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


if __name__ == "__main__":
    cxr = CXR(
        pid="00436515-870c-4b36-a041-de91049b9ab4",
        x=[264.0, 562.0],
        y=[152.0, 152.0],
        width=[213.0, 256.0],
        height=[379.0, 453.0],
        diagnose=True,
        source="images",
    )
    f = cxr.get_symptom_areas
