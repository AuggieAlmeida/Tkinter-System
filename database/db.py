import sqlite3


class Database:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def conect_db(self):
        self.conn = sqlite3.connect("./database/SPDB.db")
        self.cursor = self.conn.cursor()

    def disconnect_db(self):
        self.conn.close()

    def struct_db(self):
        self.conect_db()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tb_clientes (
                cod INTEGER PRIMARY KEY AUTOINCREMENT,
                nome VARCHAR(80) NOT NULL,
                email VARCHAR(120),
                cp VARCHAR(20),
                profissao VARCHAR(40),
                datacad VARCHAR(11),
                nascimento VARCHAR(11),
                fiscal char(255)
            );
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tb_enderecos (
                cod INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_cod INTEGER,
                cep VARCHAR(10) NOT NULL,
                num INTEGER
            );
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tb_contatos (
                linha INTEGER PRIMARY KEY,
                cliente_cod INTEGER
            );
        """)
        self.conn.commit()
        self.disconnect_db()
