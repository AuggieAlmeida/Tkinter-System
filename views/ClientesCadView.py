import sqlite3
import os
from tkinter import *
from tkcalendar import DateEntry
from datetime import date

from lib.functions import set_window_sided
from lib.colours import color
import lib.global_variable as glv


class ClientsCadController:
    def connect_db(self):
        db_path = os.path.join(
            glv.get_variable("APP_PATH"),
            glv.get_variable("DATA_DIR"),
            "SPDB.db"
        )
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def disconnect_db(self):
        self.conn.close()

    def insertClients(self):
        self.name = self.name_entry.get()
        self.email = self.email_entry.get()
        self.cp = self.cp_entry.get()
        self.birth= self.birth_entry.get()
        self.occup = self.occup_entry.get()
        self.datecad = date.today().strftime("%d/%m/%Y")
        self.obs = self.obs_entry.get("1.0", END)
        self.connect_db()
        self.cursor.execute(""" INSERT INTO tb_clientes (nome, email, cp, profissao, datacad, nascimento, fiscal)
            VALUES (?, ?, ?, ?, ?, ?, ?)""", (self.name, self.email, self.cp,  self.occup, self.datecad, self.birth,
                                              self.obs))
        self.conn.commit()
        self.disconnect_db()


class ClientsCadView(ClientsCadController):
    def __init__(self):
        super().__init__()
        self.cadwin = Toplevel()
        self.cadwin.title("Clientes")
        self.cadwin.configure(background=color("background-bar"))
        self.cadwin.resizable(False, False)
        set_window_sided(self.cadwin, 400, 600)
        self.init_window()

    def init_window(self):
        Label(self.cadwin, text="ATUALIZAR E CADASTRAR CLIENTES", font="Ivy 15", bg="#254465", fg=color("background"))\
            .place(relx=0, rely=0, relwidth=1, relheight=0.07)

        self.reg = Frame(self.cadwin, background=color("background"))
        self.reg.place(relx=0.01, rely=0.08, relwidth=0.98, relheight=0.83)

        self.buttons = Frame(self.cadwin, background=color("background"))
        self.buttons.place(relx=0.01, rely=0.92, relwidth=0.98, relheight=0.07)

        self.cadname = Label(self.reg, text="Nome *:", font="Ivy 13", bg=color("background"))
        self.cadname.place(relx=0.01, rely=0.02, relwidth=0.18, relheight=0.08)
        self.name_entry = Entry(self.reg)
        self.name_entry.place(relx=0.20, rely=0.03, relwidth=0.75, relheight=0.06)

        self.cademail = Label(self.reg, text="Email:", font="Ivy 13", bg=color("background"))
        self.cademail.place(relx=0.03, rely=0.11, relwidth=0.18, relheight=0.08)
        self.email_entry = Entry(self.reg)
        self.email_entry.place(relx=0.20, rely=0.12, relwidth=0.75, relheight=0.06)

        self.cadcp = Label(self.reg, text="CPF/CNPJ:", font="Ivy 10", bg=color("background"))
        self.cadcp.place(relx=0.01, rely=0.20, relwidth=0.18, relheight=0.08)
        self.cp_entry = Entry(self.reg)
        self.cp_entry.place(relx=0.20, rely=0.21, relwidth=0.33, relheight=0.06)

        self.cadbirth = Label(self.reg, text="Data Nasc.:", font="Ivy 10", bg=color("background"))
        self.cadbirth.place(relx=0.56, rely=0.20, relwidth=0.18, relheight=0.08)
        self.birth_entry = DateEntry(self.reg)
        self.birth_entry.place(relx=0.75, rely=0.21, relwidth=0.20, relheight=0.06)

        self.cadoccup = Label(self.reg, text="Profissão:", font="Ivy 10", bg=color("background"))
        self.cadoccup.place(relx=0.02, rely=0.29, relwidth=0.18, relheight=0.08)
        self.occup_entry = Entry(self.reg)
        self.occup_entry.place(relx=0.20, rely=0.30, relwidth=0.75, relheight=0.06)

        self.cadctts = Label(self.reg, text="Telefones/Celulares:", font='Ivy 10', bg=color("background"))
        self.cadctts.place(relx=0.02, rely=0.39, relwidth=0.29, relheight=0.08)
        self.ctt_entry = Entry(self.reg)
        self.ctt_entry.place(relx=0.02, rely=0.47, relwidth=0.42, relheight=0.06)
        self.bt_cttadd = Button(self.reg, text="+", font='Ivy 16', background=color("background"))
        self.bt_cttadd.place(relx=0.02, rely=0.54, relwidth=0.07, relheight=0.05)
        self.bt_cttdel = Button(self.reg, text="-", font='Ivy 16', background=color("background"))
        self.bt_cttdel.place(relx=0.37, rely=0.54, relwidth=0.07, relheight=0.05)
        self.bt_cttdef = Button(self.reg, text="Definir principal", font='Ivy 10', background=color("background"))
        self.bt_cttdef.place(relx=0.10, rely=0.54, relwidth=0.26, relheight=0.05)

        self.list_ctt = Listbox(self.reg, width=100, height=100)
        self.list_ctt.place(relx=0.02, rely=0.61, relheight=0.17, relwidth=0.40)
        self.scroll_ctt = Scrollbar(self.reg, orient='vertical')
        self.scroll_ctt.place(relx=0.42, rely=0.61, relheight=0.17, relwidth=0.03)

        self.cadaddress = Label(self.reg, text="Endereços:", font='Ivy 10', bg=color("background"))
        self.cadaddress.place(relx=0.53, rely=0.39, relwidth=0.18, relheight=0.08)
        self.address_entry = Entry(self.reg)
        self.address_entry.place(relx=0.53, rely=0.47, relwidth=0.42, relheight=0.06)
        self.bt_addressadd = Button(self.reg, text="+", font='Ivy 16', background=color("background"))
        self.bt_addressadd.place(relx=0.53, rely=0.54, relwidth=0.07, relheight=0.05)
        self.bt_addressdel = Button(self.reg, text="-", font='Ivy 16', background=color("background"))
        self.bt_addressdel.place(relx=0.88, rely=0.54, relwidth=0.07, relheight=0.05)
        self.bt_addressdef = Button(self.reg, text="Definir principal", font='Ivy 10', background=color("background"))
        self.bt_addressdef.place(relx=0.61, rely=0.54, relwidth=0.26, relheight=0.05)

        self.list_address = Listbox(self.reg, width=100, height=100)
        self.list_address.place(relx=0.53, rely=0.61, relheight=0.17, relwidth=0.40)
        self.scroll_adress = Scrollbar(self.reg, orient='vertical')
        self.scroll_adress.place(relx=0.93, rely=0.61, relheight=0.17, relwidth=0.03)

        self.cadobs = Label(self.reg, text="Observação Fiscal:", font="Ivy 13", background=color("background"))
        self.cadobs.place(relx=0.02, rely=0.79)
        self.obs_entry = Text(self.reg)
        self.obs_entry.place(relx=0.03, rely=0.85, relwidth=0.94, relheight=0.12)

        self.bt_leave = Button(self.buttons, text="Sair", font='Ivy 14', bg=color("background"),
                               command=self.cadwin.destroy)
        self.bt_leave.place(relx=0.03, rely=0.10, relheight=0.80, relwidth=0.20)
        self.bt_clean = Button(self.buttons, text="Limpar", font='Ivy 14', bg=color("background"),
                               command=self.clean)
        self.bt_clean.place(relx=0.40, rely=0.10, relheight=0.80, relwidth=0.20)
        self.bt_save = Button(self.buttons, text="Salvar", font="Ivy 14", background=color("background"),
                              command=self.insertClients)
        self.bt_save.place(relx=0.77, rely=0.10, relheight=0.80, relwidth=0.20)

    def clean(self):
        self.name_entry.delete(0, END)
        self.email_entry.delete(0, END)
        self.cp_entry.delete(0, END)
        self.ctt_entry.delete(0, END)
        self.address_entry.delete(0, END)
        self.birth_entry.delete(0, END)
        self.occup_entry.delete(0, END)
        self.obs_entry.delete("1.0", END)


