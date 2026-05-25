import sqlite3 as s

def criar_banco():
    conexao = s.connect('database.db')
    conexao.executescript("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY  AUTOINCREMENT,
        nome TEXT NOT NULL,
        type ENUM CHECK('status' IN ('normal', 'admin')) NOT NULL
        );
                    
    CREATE TABLE IF NOT EXISTS pedido(
        id INTEGER PRIMARY KEY  AUTOINCREMENT,
        id_user INTEGER, 
        
        FOREIGN KEY (id_user) REFERENCES users(id)
        );
                    
    CREATE TABLE IF NOT EXISTS item_cardapio_pedido(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_pedido INTEGER NOT NULL, 
        id_item_cardapio INTEGER NOT NULL,
        quantidade INTEGER DEFAULT 1 NOT NULL,
                    
        FOREIGN KEY (id_pedido) REFERENCES pedido(id),
        FOREIGN KEY (id_item_cardapio) REFERENCES item_cardapio(id)
        );
    
    CREATE TABLE IF NOT EXISTS pedido(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        desc TEXT)
    
    """)

def criar_conexao():
    conexao = s.connect('database.db')
    return conexao

