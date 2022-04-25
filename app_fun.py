"""App functions."""

from tkinter import ttk
from chest_radiography import CXR, NoSymptomException
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
    print(f"Checking for pid:'{pid}'...")
    cxr = CXR(pid=pid)
    if cxr.is_diagnosed:
        n = len(cxr._x)
        print(f"Find number of inflamation areas: {n}")
        if n == 0:
            print("No inflamation is detected.")
            return
        cxr.display_bboxes
        return
    else:
        print(f"pid:'{pid}' has not been diagnosed yet.")
        return


def diagnose_record(
    fig_frame: ttk.Frame, pid_entry: ttk.Entry, parse_type: str
) -> None:
    """Parse record and output image."""
    pid = pid_entry.get()
    pid_entry.delete(0, "end")
    # check if the entry is empty
    if not pid:
        print("pid entry cannot be empty.")
        return
    cxr = CXR(pid=pid)
    if not cxr.is_diagnosed:
        print(f"pid:'{cxr.pid}' has not been diagnosed yet.")
        return
    try:
        if parse_type == "display":
            fig = cxr.display_img
        elif parse_type == "mark":
            fig = cxr.mark_symptoms
        elif parse_type == "segment":
            fig = cxr.segment_symptom
        else:
            print("incorrect pasre_type")
            return
    except NoSymptomException as e:
        print(e.message)
        return
    canvas = FigureCanvasTkAgg(fig, master=fig_frame)
    fig_widget = canvas.get_tk_widget()
    fig_widget.grid(row=0, column=0)


def clear_img_record(fig_frame: ttk.Frame, pid_entry: ttk.Entry) -> None:
    """Clear the diagnosis image."""
    pid_entry.delete(0, "end")
    widges = fig_frame.winfo_children()
    for w in widges:
        w.destroy()
