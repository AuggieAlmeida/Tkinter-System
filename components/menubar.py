from tkinter import Frame, Label
from lib.colours import color


def init_bar(master):
    bar = Frame(master, width=980, height=60)
    bar.config(bg="#254480")
    bar.pack(fill="both")

    Label(bar, text="MITRA", font="Time 40", bg="#254480", fg=color("background")).grid(row=0, column=1)

    for child in bar.winfo_children():
        widget_class = child.__class__.__name__
        if widget_class == "Label":
            child.grid_configure(pady=0, padx=15, sticky="W")
        elif widget_class == "Frame":
            child.grid_configure(pady=0, padx=0, sticky="NSWE")
        else:
            child.grid_configure(padx=5, pady=3, sticky='N')
