"""App functions."""

from tkinter import ttk
from chest_radiography import *


def find_record(pid_entry: ttk.Entry, stored_cxr_record: None | CXR) -> None:
    """Find CXR record."""
    pid = pid_entry.get()
    pid_entry.delete(0, "end")

    print("checking for pid:", pid)
    stored_cxr_record = CXR(pid=pid)

    if stored_cxr_record.is_diagnosed:
        print(stored_cxr_record._x)
    else:
        print(f"pid: {pid} has not been diagnosed yet.")
