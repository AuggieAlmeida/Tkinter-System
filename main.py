import os
from tkinter import *

from components import menubar
from views import ClientesView

from lib.colours import color
from lib.functions import set_window_center
import lib.global_variable as glv
from database import db


glv.init_global_variable()
glv.set_variable("APP_NAME", "MITRA")
glv.set_variable("APP_PATH", os.path.dirname(__file__))
glv.set_variable("DATA_DIR", "database")

root = Tk()


class App:
    def __init__(self):
        self.root = root
        self.home()
        menubar.init_bar(self.root)
        db.Database().struct_db()
        self.frames()
        self.init_clientes()

        root.mainloop()

    def home(self):
        self.root.title("MITRA")
        self.root.configure(background=color("background2"))
        set_window_center(self.root, 1260, 720)
        self.root.resizable(False, False)

    def frames(self):
        self.frameup = Frame(self.root, background=color("background"))
        self.frameup.place(relx=0.005, rely=0.1, width=430, height=640)

        self.framedown = Frame(self.root, background=color("background"))
        self.framedown.place(relx=0.353, rely=0.1, width=810, height=640)

    def init_clientes(self):
        win = ClientesView.ClientsView(self.frameup, self.framedown)



    def init_home(self):
        pass


App()
