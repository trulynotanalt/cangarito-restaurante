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
    quantidade = request.form.get('quantidade_pedido')
    observacao = request.form.get('observacao')

    pedido = {
        'nome' : nome_produto,
        'quantidade' : quantidade,
        'observacao' : observacao,
    }

    lista_pedidos = json.loads(request.cookies.get('pedidos'))
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
        resultado = cursor.execute('SELECT id FROM item_cardapio WHERE name == ? ', (i['name'])).fetchone()
        
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

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/perfil')
def perfil():
    return render_template('perfil.html')

if __name__ == "__main__":
    app.run(debug=True)