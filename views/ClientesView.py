import sqlite3
import os

from tkinter import *
from tkinter import ttk
from tkcalendar import *
from tkinter import messagebox

from datetime import date

from lib.colours import color
import lib.global_variable as glv


class ClientsController:
    def __init__(self):
        pass

    def getEntry(self):
        self.name = self.name_entry.get()
        self.email = self.email_entry.get()
        self.cp = self.cod_entry.get()
        self.occup = self.occup_entry.get()
        self.birthday = self.birth.get_date()
        self.datecad = date.today().strftime("%d/%m/%Y")
        self.obs = self.obs_entry.get("1.0", END)

    def setEntry(self, cod, name, email, cp, occup, datecad, birth, obs):
        self.lb_id.config(text=cod)
        self.name_entry.insert(END, name)
        self.email_entry.insert(END, email)
        self.cod_entry.insert(END, cp)
        self.occup_entry.insert(END, occup)
        self.lb_date.config(text=datecad)
        self.obs_entry.insert("1.0", obs)

    def clean(self):
        self.cod_entry.delete(0, END)
        self.name_entry.delete(0, END)
        self.email_entry.delete(0, END)
        self.occup_entry.delete(0, END)
        self.ctts_entry.delete(0, END)
        self.obs_entry.delete("1.0", END)

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

    def insertClient(self):
        self.getEntry()
        if self.name == '':
            messagebox.showerror('Erro', 'Preencha os dados obrigatórios')
        else:
            self.getEntry()
            self.clean()
            self.connect_db()
            self.cursor.execute(""" INSERT INTO tb_clientes (nome, email, cp, profissao, datacad, nascimento, fiscal)
                VALUES (?, ?, ?, ?, ?, ?, ?)""",
                                (self.name, self.email, self.cp, self.occup, self.datecad, self.birthday,
                                 self.obs))
            self.conn.commit()
            messagebox.showinfo('Sucesso', 'Dados inseridos com sucesso')
            self.disconnect_db()

    def selectAllClients(self):
        auxlist = []
        self.connect_db()
        self.cursor.execute(""" SELECT * FROM tb_clientes """)
        self.info = self.cursor.fetchall()

        for i in self.info:
            auxlist.append(i)

        self.disconnect_db()
        return auxlist

    def selectClientbyId(self, idclient=int):
        self.connect_db()
        self.cursor.execute(""" SELECT * FROM tb_clientes 
            WHERE cod = ?""", (idclient,))
        row = self.cursor.fetchall()
        self.disconnect_db()

        return row

    def updateClient(self):
        self.connect_db()
        self.cursor.execute(""" UPDATE tb_clientes SET
            nome = ?
            WHERE cod = ?""")
        self.disconnect_db()

    def deleteClient(self):
        self.getEntry()
        self.connect_db()
        self.cursor.execute(""" DELETE FROM tb_clientes 
            WHERE cod = ? """, (self.cp,))
        self.conn.commit()
        self.disconnect_db()

    def treeSelect(self):
        treev_data = tree.focus()
        treev_dicionario = tree.item(treev_data)
        treev_list = treev_dicionario['values']

        return treev_list

    def OnDoubleClick(self, event):
        self.clean()
        cod = self.treeSelect()
        values = self.selectClientbyId(cod[0])
        self.setEntry(values[0][0], values[0][1], values[0][2], values[0][3], values[0][4], values[0][5],
                      values[0][6], values[0][7])


class ClientsView(ClientsController):
    def __init__(self, frameup, framedown):
        self.list_header = ['ID', 'Nome', 'Email', 'Documento', 'Nascimento', 'Profissão']
        self.list_cli = ttk.Treeview
        self.framedown = framedown
        self.frameup = frameup
        self.setup()
        self.selectAllClients()

    def setup(self):
        self.init_menu()
        self.init_Clients()
        self.init_tree()

    def init_menu(self):
        bar = Frame(self.frameup, width=470, height=40)
        bar.config(bg="#254480")
        bar.pack(fill="both")

        Label(bar, text="Clientes", font="Time 20", bg="#254480", fg=color("background")).grid(row=0, column=1)

    def init_Clients(self):
        self.init_layout()
        self.init_buttons()

    def init_layout(self):
        self.lb_cod = Label(self.frameup, text="CPF/CNPJ:", font="Ivy 10", bg=color("background"))
        self.lb_cod.place(relx=0.002, rely=0.08, relwidth=0.2)
        self.cod_entry = Entry(self.frameup, font="Ivy 11")
        self.cod_entry.place(relx=0.20, rely=0.08, relwidth=0.30, relheight=0.035)

        self.lb_name = Label(self.frameup, text="Nome:", font="Ivy 11", bg=color("background"))
        self.lb_name.place(relx=0.075, rely=0.15, relwidth=0.1)
        self.name_entry = Entry(self.frameup, font="Ivy 11")
        self.name_entry.place(relx=0.20, rely=0.15, relwidth=0.75, relheight=0.04)

        self.lb_email = Label(self.frameup, text="Email:", font="Ivy 11", bg=color("background"))
        self.lb_email.place(relx=0.08, rely=0.22, relwidth=0.1)
        self.email_entry = Entry(self.frameup, font="Ivy 11")
        self.email_entry.place(relx=0.20, rely=0.22, relwidth=0.75, relheight=0.04)

        Label(self.frameup, text="________________________________________________", font="Ivy 13",
              bg=color("background")). \
            place(relx=0, rely=0.27, relwidth=1, relheight=0.04)

        self.lb_occup = Label(self.frameup, text="Profissão:", font="Ivy 11", bg=color("background"))
        self.lb_occup.place(relx=0.02, rely=0.32, relwidth=0.16)
        self.occup_entry = Entry(self.frameup, font="Ivy 11")
        self.occup_entry.place(relx=0.02, rely=0.37, relwidth=0.58, relheight=0.04)

        self.lb_birth = Label(self.frameup, text="Data de Nasc.:", font="Ivy 11", bg=color("background"))
        self.lb_birth.place(relx=0.65, rely=0.32, relwidth=0.24)
        self.birth = DateEntry(self.frameup)
        self.birth.config()
        self.birth.place(relx=0.65, rely=0.37, relwidth=0.30, relheight=0.04)

        Label(self.frameup, text="________________________________________________", font="Ivy 13",
              bg=color("background")). \
            place(relx=0, rely=0.42, relwidth=1, relheight=0.04)

        Label(self.frameup, text="________________________________________________", font="Ivy 13",
              bg=color("background")). \
            place(relx=0, rely=0.67, relwidth=1, relheight=0.04)

        self.lb_ctts = Label(self.frameup, text="Telefones/Celulares:", font="Ivy 12", bg=color("background"))
        self.lb_ctts.place(relx=0, rely=0.46, relwidth=0.50, relheight=0.04)
        self.ctts_entry = Entry(self.frameup, font="Ivy 11")
        self.ctts_entry.place(relx=0.02, rely=0.52, relwidth=0.30, relheight=0.04)

        self.ctts_entry2 = Entry(self.frameup, font="Ivy 11")
        self.ctts_entry2.place(relx=0.02, rely=0.59, relwidth=0.46, relheight=0.04)

        Label(self.frameup, text=" ", font="Ivy 13", bg="black"). \
            place(relx=0.5, rely=0.451, relwidth=0.002, relheight=0.25)

        self.lb_ctts = Label(self.frameup, text="Endereços:", font="Ivy 12", bg=color("background"))
        self.lb_ctts.place(relx=0.51, rely=0.46, relwidth=0.50, relheight=0.04)

        self.cadobs = Label(self.frameup, text="Observação Fiscal:", font="Ivy 13", background=color("background"))
        self.cadobs.place(relx=0.02, rely=0.72)
        self.obs_entry = Text(self.frameup)
        self.obs_entry.place(relx=0.03, rely=0.77, relwidth=0.94, relheight=0.12)

        self.cadid = Label(self.framedown, text="ID: ", font="Ivy 20", background=color("background"))
        self.cadid.place(relx=0.02, rely=0.013)
        self.lb_id = Label(self.framedown, text="1", font="Ivy 20", background=color("background"), justify=LEFT)
        self.lb_id.place(relx=0.07, rely=0.013)

        self.caddate = Label(self.framedown, text="Registrado em: ", font="Ivy 20", background=color("background"))
        self.caddate.place(relx=0.56, rely=0.013)
        self.lb_date = Label(self.framedown, text="12/12/2020", font="Ivy 20", background=color("background"))
        self.lb_date.place(relx=0.80, rely=0.013)

    def init_buttons(self):
        self.bt_pesquisar = Button(self.frameup, text="Pesquisar", bg=color("background"))
        self.bt_pesquisar.place(relx=0.53, rely=0.08, relwidth=0.2, relheight=0.05)
        self.bt_limpar = Button(self.frameup, text="Limpar", bg=color("background"), command=self.clean)
        self.bt_limpar.place(relx=0.75, rely=0.08, relwidth=0.2, relheight=0.05)

        self.bt_defctt = Button(self.frameup, text="Definir principal", bg=color("background"))
        self.bt_defctt.place(relx=0.05, rely=0.64, relwidth=0.4, relheight=0.04)

        self.bt_insert = Button(self.frameup, text="Inserir", bg=color("background-bar"), fg="white",
                                command=self.createClient)
        self.bt_insert.place(relx=0.020, rely=0.93, relwidth=0.225, relheight=0.05)

        self.bt_update = Button(self.frameup, text="Atualizar", bg="green", fg="white",
                                command=self)
        self.bt_update.place(relx=0.265, rely=0.93, relwidth=0.225, relheight=0.05)

        self.bt_delete = Button(self.frameup, text="Deletar", bg="red", fg="white",
                                command=self.removeClient)
        self.bt_delete.place(relx=0.51, rely=0.93, relwidth=0.225, relheight=0.05)

        self.bt_import = Button(self.frameup, text="Importar CSV", bg=color("background"), fg="black")
        self.bt_import.place(relx=0.755, rely=0.93, relwidth=0.225, relheight=0.05)

    def init_tree(self):
        global tree
        list = self.selectAllClients()

        self.list_header = ['ID', 'Nome', 'Email', 'Documento', 'Profissão', 'Data de nascimento']
        tree = ttk.Treeview(self.framedown, selectmode="extended", columns=self.list_header, show="headings")
        self.vsb = ttk.Scrollbar(self.framedown, orient="vertical", command=tree.yview)

        tree.configure(yscrollcommand=self.vsb.set)
        tree.place(relx=0.01, rely=0.10, relwidth=0.96, relheight=0.60)
        self.vsb.place(relx=0.97, rely=0.10, relwidth=0.02, relheight=0.60)

        hd = ["nw", "nw", "nw", "nw", "center", "center"]
        h = [10, 170, 190, 90, 130, 100]
        n = 0

        for col in self.list_header:
            tree.heading(col, text=col.title(), anchor=CENTER)
            tree.column(col, width=h[n], anchor=hd[n])
            n += 1

        for item in list:
            tree.insert('', END, values=item)

        tree.bind("<Double-1>", self.OnDoubleClick)

    def createClient(self):
        self.insertClient()

        for widget in self.framedown.winfo_children():
            widget_class = widget.__class__.__name__
            if widget_class == 'Treeview':
                widget.destroy()

        self.init_tree()

    def removeClient(self):
        self.deleteClient()

        for widget in self.framedown.winfo_children():
            widget_class = widget.__class__.__name__
            if widget_class == 'Treeview':
                widget.destroy()

        self.init_tree()
