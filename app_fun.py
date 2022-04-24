"""App functions."""

import tkinter
from tkinter import CENTER, ttk

from matplotlib.pyplot import plot
from chest_radiography import CXR
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

matplotlib.use("TkAgg")


def find_record(pid_entry: ttk.Entry) -> None:
    """Find CXR record."""
    pid = pid_entry.get()
    pid_entry.delete(0, "end")
    # check if the entry is empty
    if not pid:
        print("pid entry cannot be empty.")
        return
    # locate record in db; if find anything, give simple printout for the diagnosis
    print(f"checking for pid: {pid} ...")
    cxr = CXR(pid=pid)
    if cxr.is_diagnosed:
        print(cxr._x)  # TODO: give more info
        return
    else:
        print(f"pid: {pid} has not been diagnosed yet.")
        return


def diagnose_record(root: tkinter.Tk, pid_entry: ttk.Entry) -> None:
    """Display marked CXR image."""
    pid = pid_entry.get()
    pid_entry.delete(0, "end")
    # check if the entry is empty
    if not pid:
        print("pid entry cannot be empty.")
        return
    cxr = CXR(pid=pid)
    if not cxr.is_diagnosed:
        print(f"pid: {cxr.pid} has not been diagnosed yet.")
        return
    fig = cxr.mark_symptoms
    fig_frame = ttk.Frame(root, padding=20, name="fig_frame")
    fig_frame.place(anchor=CENTER, relx=0.5, rely=0.6)
    canvas = FigureCanvasTkAgg(fig, master=fig_frame)
    fig_widget = canvas.get_tk_widget()
    fig_widget.grid(row=0, column=0)


def clear_img_record(root: tkinter.Tk, pid_entry: ttk.Entry) -> None:
    """Clear the diagnosis image."""
    pid_entry.delete(0, "end")
    widges = root.children["fig_frame"].winfo_children()
    for w in widges:
        w.destroy()
