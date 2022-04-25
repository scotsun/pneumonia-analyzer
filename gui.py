"""Application front-end."""


import tkinter
from tkinter import CENTER, ttk
from tkinter import filedialog
from app_fun import *


def main() -> None:
    """GUI front-end."""
    root = tkinter.Tk()
    root.title("Pneumonia Chest Radiography Diagnoser")
    root.geometry("700x600")
    add_cxr_diagnoser_frame(root)
    root.mainloop()


def add_cxr_diagnoser_frame(root: tkinter.Tk) -> None:
    """Generate GUI frames and link GUI to the db."""
    # first frame:
    search_frame = ttk.Frame(root, padding=20, name="search_frame")
    search_frame.place(anchor=CENTER, relx=0.5, rely=0.1)
    pid_label = ttk.Label(search_frame, text="input pid:", padding=20)
    pid_entry = ttk.Entry(search_frame, width=35)
    search_button = ttk.Button(search_frame, text="click to search")
    pid_label.grid(row=0, column=0)
    pid_entry.grid(row=0, column=1)
    search_button.grid(row=0, column=2)
    # second frame:
    diag_action_frame = ttk.Frame(root, padding=20, name="diag_action_frame")
    diag_action_frame.place(anchor=CENTER, relx=0.5, rely=0.2)
    display_button = ttk.Button(diag_action_frame, text="diagnose: display")
    mark_button = ttk.Button(diag_action_frame, text="diagnose: mark")
    segment_button = ttk.Button(diag_action_frame, text="diagnose: segment")
    clear_button = ttk.Button(diag_action_frame, text="clear")

    def UploadAction(event=None) -> None:
        filename = filedialog.askopenfilename()
        file_type = filename.split(".")[-1]
        if file_type not in {"jpg", "jpeg"}:
            print("the uploaded image should be *.jpg | *.jpeg")
            return
        print("Selected:", filename)

    upload_to_inference_button = ttk.Button(diag_action_frame, text="upload & infer")

    display_button.grid(row=0, column=0)
    mark_button.grid(row=0, column=1)
    segment_button.grid(row=0, column=2)
    clear_button.grid(row=0, column=3)
    upload_to_inference_button.grid(row=1, column=1)
    # third frame:
    fig_frame = ttk.Frame(root, padding=20, name="fig_frame")
    fig_frame.place(anchor=CENTER, relx=0.5, rely=0.6)

    # add actions to buttons
    search_button["command"] = lambda: find_record(pid_entry)
    display_button["command"] = lambda: diagnose_record(fig_frame, pid_entry, "display")
    mark_button["command"] = lambda: diagnose_record(fig_frame, pid_entry, "mark")
    segment_button["command"] = lambda: diagnose_record(fig_frame, pid_entry, "segment")
    clear_button["command"] = lambda: clear_img_record(fig_frame, pid_entry)
    upload_to_inference_button["command"] = lambda: UploadAction()
