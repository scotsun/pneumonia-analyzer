"""Application front-end."""


from pymongo import MongoClient
import tkinter
from tkinter import ttk
from app_fun import *
from db import db
from chest_radiography import CXR


def gui() -> None:
    """GUI front-end."""
    stored_cxr_record: None | CXR = None

    root = tkinter.Tk()
    root.title("Pneumonia Chest Radiography Diagnoser")
    root.geometry("720x400")
    cxr_diagnoser_frame(root, stored_cxr_record)

    root.mainloop()


def cxr_diagnoser_frame(root: tkinter.Tk, stored_cxr_record: None | CXR) -> None:
    """Generate GUI frame and link to the db."""
    # frame = ttk.Frame(root, padding=20)
    # frame.grid(row=0)

    pid_label = ttk.Label(root, text="input pid:", padding=20)
    pid_entry = ttk.Entry(root, width=35)
    search_button = ttk.Button(root, text="click")

    pid_label.grid(row=0, column=0)
    pid_entry.grid(row=0, column=1)
    search_button.grid(row=0, column=2)

    search_button["command"] = lambda: find_record(pid_entry, stored_cxr_record)


if __name__ == "__main__":
    gui()
