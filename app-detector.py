"""Detector."""

import os
import tkinter
from tkinter import filedialog, ttk
from typing import Sized
import torch
from detecto import core, utils, visualize

detector = core.Model(["pneumonia"], pretrained=False)
detector._model.load_state_dict(
    torch.load("./model_weight/weights_v2.pth", map_location=detector._device)
)


def app() -> None:
    """Run the app."""
    os.system("cls||clear")
    root = tkinter.Tk()
    root.title("PneumoDetectr")
    root.geometry("200x50")
    upload_to_inference_button = ttk.Button(root, text="upload & infer")
    upload_to_inference_button.pack()
    upload_to_inference_button["command"] = lambda: upload_action()
    root.mainloop()


def upload_action(event=None) -> None:
    """Button commpand."""
    filename = filedialog.askopenfilename(
        title="Select file", filetypes=(("jpg files", "*.jpg"), ("all files", "*.*"))
    )
    if filename == "":
        return
    file_type = filename.split(".")[-1]
    if file_type not in {"jpg", "jpeg"}:
        print("the uploaded image should be *.jpg | *.jpeg")
    print("Selected PID:", filename.split(".")[0].split("/")[-1])
    inference_symptom(filepath=filename)


def inference_symptom(filepath: str, threshold=0.4) -> None:
    """Make inference."""
    image = utils.read_image(filepath)
    _, _boxes, _scores = detector.predict(image)
    # select by threshold
    boxes = _boxes[_scores > threshold]
    scores = _scores[_scores > threshold]
    _conf_label = list(scores.numpy().round(2).astype("str"))
    conf_label = ["confidence:" + c for c in _conf_label]
    _inference_symptom(boxes, scores)
    visualize.show_labeled_image(image, boxes, conf_label)


def _inference_symptom(boxes: torch.Tensor, scores: torch.Tensor) -> None:
    """Display the result in terminal."""
    print("Inflamations are located by bounding boxes")
    print(
        """
        box format: [Left, Top, Right, Bottom]

        (Left,Top)
            *_________
            |         |
            |         |
            |_________|
                      *
                    (Right,Bottom)
        """
    )
    for i in range(len(boxes)):
        print("confidence:", round(scores[i].item(), 2))
        print("       box:", [round(boxes[i][j].item()) for j in range(4)])


if __name__ == "__main__":
    app()
