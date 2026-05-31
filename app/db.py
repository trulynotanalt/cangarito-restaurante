import sqlite3 as s

def criar_banco():
    conexao = s.connect('database.db')
    conexao.executescript("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY  AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL,
        type TEXT NOT NULL DEFAULT 'normal' CHECK(type IN ('normal', 'admin')),
        password TEXT NOT NULL
        );
                    
    CREATE TABLE IF NOT EXISTS pedido(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_user INTEGER NOT NULL, 
        observacao TEXT,
        subtotal NUMERIC,  -- ADICIONADO
        imposto NUMERIC,   -- ADICIONADO
        total NUMERIC,     -- ADICIONADO
        active BOOL NOT NULL DEFAULT true,
                          
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
                          
    CREATE TABLE IF NOT EXISTS item_cardapio(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price NUMERIC NOT NULL,
        desc TEXT NOT NULL,
        classificacao TEXT NOT NULL CHECK(classificacao IN ('cuscuz','campeao_vendas','bebidas', 'sobremesa'))
        );
    
    """)

def criar_conexao():
    conexao = s.connect('database.db')
    return conexao

def injecao():
    conn = criar_conexao()
    conn.executescript("""
    INSERT INTO item_cardapio (name, price, desc, classificacao) VALUES
    ('Coxinha Barata', 15.00, 'Coxinha de frango com molho especial do cangaço, temperado com cominho e coentro defumados.', 'campeao_vendas'),
    ('Bolo de Milho', 12.00, 'Receita tradicional nordestina com milho verde, leite de coco e um toque de erva-doce.', 'campeao_vendas'),
    ('Cuscuz Recheado', 18.00, 'Cuscuz de milho com carne de sol desfiada, queijo coalho derretido e manteiga da terra.', 'campeao_vendas'),
    ('Misto Nordestino', 7.00, 'Um sanduiche básico com presunto, queijo, frango, ovo e um molho da casa.', 'campeao_vendas'),
    ('Cuscuz Simples', 8.00, 'Cuscuz de milho cozido no vapor, servido puro com manteiga da terra.', 'cuscuz'),
    ('Cuscuz com Ovo', 10.00, 'Cuscuz tradicional acompanhado de ovo frito com gema mole.', 'cuscuz'),
    ('Cuscuz com Calabresa', 14.00, 'Cuscuz de milho com fatias de calabresa acebolada e manteiga da terra.', 'cuscuz'),
    ('Cuscuz com Queijo', 12.00, 'Cuscuz com generosas fatias de queijo coalho derretido por cima.', 'cuscuz'),
    ('Cuscuz com Banana', 11.00, 'Cuscuz adocicado com banana-da-terra frita e melado de rapadura.', 'cuscuz'),
    ('Cuscuz com Charque', 17.00, 'Cuscuz de milho com charque desfiada, cebola roxa e coentro fresco.', 'cuscuz'),
    ('Cuscuz Doce', 10.00, 'Cuscuz adocicado com leite condensado e coco ralado fresco.', 'cuscuz'),
    ('Cuscuz de Praia', 22.00, 'Cuscuz de milho com frutos do mar refogados no leite de coco e pimenta de cheiro.', 'cuscuz'),
    ('Cartola', 9.00, 'Banana frita com queijo coalho, coberta com açúcar e canela.', 'sobremesa'),
    ('Pudim de Leite', 17.00, 'Pudim caseiro com calda de caramelo e textura cremosa.', 'sobremesa'),
    ('Sagu com Coco', 8.00, 'Bolinhas de sagu cozidas em leite de coco, servido gelado.', 'sobremesa'),
    ('Bolo de Rolo', 10.00, 'Camadas finas de massa com goiabada, enroladas com perfeição.', 'sobremesa'),
    ('Suco de Caju', 6.00, 'Suco natural de caju com pouquíssimo açúcar e muito sabor.', 'bebidas'),
    ('Suco de Manga', 7.00, 'Bebida refrescante feita com manga da região do muro de Romerito, muito saborosa.', 'bebidas'),
    ('Cajuína', 12.00, 'Refrigerante típico do Seridó, com sabor doce e floral.', 'bebidas'),
    ('Água de Coco', 5.00, 'Água de coco natural, servida gelada direto no copo ou no coco.', 'bebidas');
    """)

