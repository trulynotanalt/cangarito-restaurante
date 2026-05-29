from flask import Flask, render_template, request, redirect, url_for, flash, make_response, session
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
    #boa sorte bd.py, vulgo joão victor noberto tomaz santana
    # if 'roro' not in session:
    #     return redirect(url_for('cadastro'))
    return render_template('landing-page.html')

@app.route('/cadastro', methods=['GET','POST'])
def cadastro():

    #cara do bd.py q se vire aq
    if 'usuario' in session:
        return redirect(url_for('landingpage'))
    
    if request.method == 'POST':
        #aq o cara do banco de dados vai usar essas infos para fazer a confirmação e integração com o bd.py
        usuario = request.form.get('usuario')
        email = request.form.get('email')
        senha = request.form.get('senha')
        c_senha = request.form.get('c_senha')

        conexao = criar_conexao()
        cursor = conexao.cursor()

        cursor.execute("""
            INSERT INTO users
            (nome, email, password, type)
            VALUES (?, ?, ?, ?)
        
        """,(usuario, email, c_senha, 'normal'))

        conexao.commit()
        conexao.close()

        return redirect(url_for('login'))

    
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
    if 'usuario' not in session:
        return redirect(url_for('cadastro'))
    resp = make_response()
    nome_produto = request.form.get('nome_produto')
    quantidade = request.form.get('quantidade_pedido')
    observacao = request.form.get('observacao')

    pedido = {
        'nome' : nome_produto,
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

    if 'usuario' not in session:
        return redirect(url_for('cadastro'))

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

    #acaba nunca, avemaria
    if 'usuario' not in session:
        return redirect(url_for('cadastro'))
    
    return render_template('happyhour.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    conn = criar_conexao()
    
    nome_user = request.form.get("nome")
    email_user = request.form.get('email')
    passw_user = request.form.get('senha')
    user_in_bank = conn.execute("SELECT nome, email, password   FROM users WHERE nome = ? AND email = ? AND password = ?", (nome_user, email_user, passw_user)).fetchone()

    if  user_in_bank is None:
        conn.close()
        return redirect(url_for('login'))
    
    conn.close()
    # COLOCAR SESSÃO AQUI
    session['usuario'] = {
        "nome": nome_user,
        "email": email_user,
        "senha": passw_user
    }
    return redirect(url_for('landingpage'))


@app.route('/perfil', methods=['GET'])
def perfil():
    
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    pedidos_agrupados = {}
    conn = criar_conexao()
    
   
    email_usuario = session['usuario']['email']
    
  
    user_data = conn.execute("SELECT id FROM users WHERE email = ?", (email_usuario,)).fetchone()
    if not user_data:
        return redirect(url_for('login'))
    id_usuario_logado = user_data[0]

  
    query = conn.execute("""
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
    """, (id_usuario_logado,)).fetchall() 
 
    for linha in query:
        pedido_id, item_nome, item_preco, item_quantidade, item_observacao = linha

        if pedido_id not in pedidos_agrupados:
            pedidos_agrupados[pedido_id] = {
                'id_pedido': pedido_id,
                'id_observacao' : item_observacao,
                'itens_comprados' : []
            }

        pedidos_agrupados[pedido_id]['itens_comprados'].append({
            'nome': item_nome,
            'preco': item_preco,
            'quantidade': item_quantidade
        })
    
    conn.close()
    lista_pedidos = list(pedidos_agrupados.values())
    return render_template('perfil.html', lista_pedidos=lista_pedidos)


@app.route('/pedido/cancel/{id}', methods=['GET', 'POST'])
def pedido_cancelar(id):
    if 'usuario' not in session:
        return redirect(url_for('cadastro'))
    
    if request.method == 'POST':
        conn = criar_conexao()
        conn.executescript("""
        UPDATE pedidos IF EXISTS
        SET active = false
        WHERE id = ?;
        """, (id))
        conn.commit()
        conn.close()
        return redirect(url_for('perfil'))
        # PEGA O ATRIBUTO DA ROTA E DESATIVA/CANCELA O PEDIDO NO BANCO DE DADOS
    
    return render_template('perfil.html')

@app.route('/logout', methods=["POST"])
def logout():
    session.pop('usuario', None)
    return redirect(url_for('landingpage'))

@app.route('/trocarsenha', methods=['GET', 'POST'])
def trocarsenha():
    
    if 'usuario' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        nova_senha = request.form.get('novasenha')
        confirmar_senha = request.form.get('confirmarsenha')

        if nova_senha != confirmar_senha:
            return redirect(url_for('trocarsenha'))

        email_usuario = session['usuario']['email']

        conexao = criar_conexao()
        cursor = conexao.cursor()
        cursor.execute("""
            UPDATE users 
            SET password = ? 
            WHERE email = ?
        """, (nova_senha, email_usuario))
        conexao.commit()
        conexao.close()

   
        session['usuario']['senha'] = nova_senha
        return redirect(url_for('perfil'))

    return render_template('trocarsenha.html')

if __name__ == "__main__":
    app.run(debug=True)