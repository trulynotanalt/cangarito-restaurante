from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from db import *
from item_cardapio import Item_Cardapio
import json

app = Flask(__name__)
app.secret_key = "GloriaAJesus"

def construtor_itens_cardapio(lista_pedidos):
    lista_obj = []
    for i in lista_pedidos:
        obj = Item_Cardapio(i[1], i[2], i[3])
        lista_obj.append(obj)
    return lista_obj


@app.route('/')
def landingpage():
    return render_template('landing-page.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/cardapio', methods=['GET', 'POST'])
def cardapio():
    if request.method == 'GET':
        conn = criar_conexao()

        itens_cuscuz = construtor_itens_cardapio(list(conn.execute("SELECT * FROM item_cardapio WHERE classificacao = 'cuscuz'")))
        itens_sobremesa = construtor_itens_cardapio(list(conn.execute("SELECT * FROM item_cardapio WHERE classificacao = 'sobremesa'")))
        itens_campeao_vendas = construtor_itens_cardapio(list(conn.execute("SELECT * FROM item_cardapio WHERE classificacao = 'campeao_vendas'")))
        itens_bebidas = construtor_itens_cardapio(list(conn.execute("SELECT * FROM item_cardapio WHERE classificacao = 'bebidas'")))

        conn.close()

        return render_template('cardapio.html', itens_sobremesa=itens_sobremesa, itens_cuscuz=itens_cuscuz, itens_campeao_vendas=itens_campeao_vendas, itens_bebidas=itens_bebidas)
    # POST boy

    resp = make_response()
    nome_produto = request.form.get('nome_produto')
    preco_produto = request.form.get('preco_produto')
    quantidade = request.form.get('quantidade_pedido')
    observacao = request.form.get('observacao')

    pedido = {
        'nome' : nome_produto,
        'preco' : preco_produto,
        'quantidade' : quantidade,
        'observacao' : observacao,
    }

    lista_pedidos = json.loads(request.cookies.get('pedidos', '[]'))
    lista_pedidos.append(pedido)

    resp = redirect(url_for('cardapio'))
    resp.set_cookie('pedidos', json.dumps(lista_pedidos))
    return resp
    


@app.route('/carrinho', methods = ['GET', 'POST'])
def carrinho():
    if request.method == 'GET':
        lista_pedidos = json.loads(request.cookies.get('pedidos', '[]'))
        return render_template('carrinho.html', pedidos=lista_pedidos)
    
    lista_pedidos = json.loads(request.cookies.get('pedidos'))
    conn = criar_conexao()
    resp = make_response()
    cursor = conn.cursor()
    for i in lista_pedidos:                                                         
        resultado = cursor.execute('SELECT id FROM item_cardapio WHERE name == ? ', (i['nome'],)).fetchone()
        
        if resultado:
            id_item_cardapio = resultado[0]
            cursor.execute("INSERT INTO pedido (id_user, observacao)  VALUES (?, ?);", (1, i['observacao']) )# COLOCAR A SESSION PRA FUNCIONAR E TROCAR PELO '1'
            id_pedido_gerado = cursor.lastrowid # RECUPERA O ÚLTIMO ID GERADO PELO CURSOR
            cursor.execute("INSERT INTO item_cardapio_pedido (id_pedido, id_item_cardapio, quantidade)  VALUES (?, ?, ?);", (id_pedido_gerado, id_item_cardapio, i['quantidade']) )

    conn.commit()
    conn.close()
    resp = render_template('carrinho.html')
    resp.set_cookie('pedidos', '')
    return resp

@app.route('/happyhour')
def happyhour():
    return render_template('happyhour.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    conn = criar_conexao()
    
    email_user = request.form.get('name_user')
    passw_user = request.form.get('password_user')
    user_in_bank = conn.execute("SELECT email, password FROM users WHERE name LIKES ? AND password == ?", (email_user, passw_user))

    if not user_in_bank:
        conn.close()
        return redirect(url_for('login'))
    
    conn.close()
    # COLOCAR SESSÃO AQUI
    return redirect(url_for('landingpage'))


@app.route('/perfil', methods=['GET'])
def perfil():

    pedidos_agrupados = {}
    conn = criar_conexao()
    
    # CONSULTA TODAS AS LINHAS QUE LIGAM (USUARIO - PEDIDO - ITEM_PEDIDO)
    query = conn.executescript("""
        SELECT 
            pedido.id AS pedido_id,
            item_cardapio.name AS item_nome,
            item_cardapio.price AS item_preco,
            item_cardapio_pedido.quantidade AS item_quantidade,
            pedido.observacao AS item_observacao
                        
        FROM pedido
            INNER JOIN item_cardapio_pedido ON pedido.id = item_cardapio_pedido.id_pedido
            INNER JOIN item_cardapio ON item_cardapio_pedido.id_item_cardapio = item_cardapio.id
        WHERE pedido.id_user = ?;
                        
    """).fetchall() # SUBSTITUIR ESSE '1' PELO ID DO USUÁRIO SALVO NO SESSION

    # ITERA SOBRE CADA LINHA RETORNADA DA QUERY E SEPARA POR PEDIDO
    for i in query:
        pedido_id, item_nome, item_preco, item_quantidade, item_observacao = query

        if pedido_id not in pedidos_agrupados:
            pedidos_agrupados[pedido_id] = {
                'id_pedido': pedido_id,
                'id_observacao' : item_observacao,
                'itens_comprados' : []
            }

        pedidos_agrupados[pedido_id]['itens_comprados'] = {
            'nome': item_nome,
            'preco': item_preco,
            'quantidade': item_quantidade
        }
    
    lista_pedidos = list(pedidos_agrupados)
    return render_template('perfil.html', lista_pedidos=lista_pedidos)


@app.route('/pedido/cancelar/<int:id>', methods=['GET', 'POST'])
def pedido_cancelar(id):
    if request.method == 'POST':
        
        
        conn = criar_conexao()
        
        
        
        conn.execute("""
        UPDATE pedido 
        SET active = false
        WHERE id = ?;
        """, (id,))
        
        conn.commit()
        conn.close()
        return redirect(url_for('perfil'))
        # PEGA O ATRIBUTO DA ROTA E DESATIVA/CANCELA O PEDIDO NO BANCO DE DADOS
    
    return render_template('perfil.html')



if __name__ == "__main__":
    app.run(debug=True)