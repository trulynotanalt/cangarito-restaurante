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
    return render_template('landing-page.html')

@app.route('/cadastro', methods=['GET', 'POST'])
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
        itens_cuscuz, itens_sobremesa, itens_bebidas, itens_campeao_vendas = [], [], [], []
        itens_cuscuz = construtor_itens_cardapio(list(conn.execute("SELECT * FROM item_cardapio WHERE classificacao = 'cuscuz'").fetchall()))
        itens_sobremesa = construtor_itens_cardapio(list(conn.execute("SELECT * FROM item_cardapio WHERE classificacao = 'sobremesa'").fetchall()))
        itens_campeao_vendas = construtor_itens_cardapio(list(conn.execute("SELECT * FROM item_cardapio WHERE classificacao = 'campeao_vendas'").fetchall()))
        itens_bebidas = construtor_itens_cardapio(list(conn.execute("SELECT * FROM item_cardapio WHERE classificacao = 'bebidas'").fetchall()))

        conn.close()

        return render_template('cardapio.html', itens_sobremesa=itens_sobremesa, itens_cuscuz=itens_cuscuz, itens_campeao_vendas=itens_campeao_vendas, itens_bebidas=itens_bebidas)
    if 'usuario' not in session:
        return redirect(url_for('login'))
        
    nome_produto = request.form.get('nome_produto').replace('R$', '')
    preco_produto = request.form.get('preco_produto').replace('R$', '')
    quantidade = request.form.get('quantidade_pedido').replace('R$', '')
    observacao = request.form.get('observacao').replace('R$', '')

    lista_pedidos = request.cookies.get('pedidos', '[]')

    pedido = {
        'id_carrinho' : 0,
        'nome' : nome_produto,
        'preco' : preco_produto,
        'quantidade' : quantidade,
        'observacao' : observacao,
    }

    if lista_pedidos:
        lista_pedidos = json.loads(lista_pedidos)
        pedido['id_carrinho'] = int(len(lista_pedidos))
        lista_pedidos.append(pedido)

    resp = redirect(url_for('cardapio'))
    resp.set_cookie('pedidos', json.dumps(lista_pedidos), path = '/')
    return resp
   


@app.route('/carrinho', methods = ['GET', 'POST'])
def carrinho():

    if 'usuario' not in session:
        return redirect(url_for('cadastro'))
    
    user_id = session.get('user_id', 1)

    if request.method == 'GET':
        lista_pedidos = json.loads(request.cookies.get('pedidos', '[]'))
        subtotal = 0

        for pedido in lista_pedidos:
            subtotal += float(pedido['preco']) * int(pedido['quantidade'])

        imposto = subtotal * 0.02
        total = subtotal + imposto

        return render_template('carrinho.html', pedidos=lista_pedidos, subtotal=subtotal, imposto=imposto, total=total)
    
   
    lista_pedidos = json.loads(request.cookies.get('pedidos', '[]'))
    if not lista_pedidos:
        return redirect(url_for('cardapio'))

    conn = criar_conexao()
    cursor = conn.cursor()
    
    subtotal = 0
    observacoes = []
    for item in lista_pedidos:                                                         
        subtotal += float(item['preco']) * int(item['quantidade'])
        if item['observacao']:
            observacoes.append(f"{item['nome']}: {item['observacao']}")

    imposto = subtotal * 0.02
    total = subtotal + imposto
    observacao_geral = "; ".join(observacoes)

    
    cursor.execute("INSERT INTO pedido (id_user, observacao, subtotal, imposto, total, active) VALUES (?, ?, ?, ?, ?, ?);", 
                   (user_id, observacao_geral, subtotal, imposto, total, 1))
    id_pedido_gerado = cursor.lastrowid

  
    for item in lista_pedidos:
      
        resultado = cursor.execute(
            'SELECT id FROM item_cardapio WHERE LOWER(TRIM(name)) = LOWER(TRIM(?))', 
            (item['nome'].strip(),)
        ).fetchone()
        
        if resultado:
            id_item_cardapio = resultado[0]
            cursor.execute("INSERT INTO item_cardapio_pedido (id_pedido, id_item_cardapio, quantidade) VALUES (?, ?, ?);", 
                           (id_pedido_gerado, id_item_cardapio, item['quantidade']))

    conn.commit()
    conn.close()
    

    resp = redirect(url_for('perfil'))
    resp.set_cookie('pedidos', '[]', path ='/')
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
    email_user = request.form.get('name_user')
    passw_user = request.form.get('password_user')
   
    user_in_bank = conn.execute("SELECT id, email FROM users WHERE email = ? AND password == ?", (email_user, passw_user)).fetchone()

    if  user_in_bank is None:
        conn.close()
        return redirect(url_for('login'))

    session['user_id'] = user_in_bank[0]
    conn.close()
    # COLOCAR SESSÃO AQUI
    session['usuario'] = {
        
        "email": email_user,
        "senha": passw_user
    }
    return redirect(url_for('landingpage'))


@app.route('/perfil', methods=['GET'])
def perfil():
    
    if 'usuario' not in session:
        return redirect(url_for('login'))

    user_id = session.get('user_id', 1)
    
    pedidos_agrupados = {}
    conn = criar_conexao()
    
   
  
    query = conn.execute("""
        SELECT 
            pedido.id AS pedido_id,
            pedido.total AS pedido_total,
            pedido.active AS pedido_ativo,
            item_cardapio.name AS item_nome,
            item_cardapio.price AS item_preco,
            item_cardapio_pedido.quantidade AS item_quantidade,
            pedido.observacao AS item_observacao
        FROM pedido
            INNER JOIN item_cardapio_pedido ON pedido.id = item_cardapio_pedido.id_pedido
            INNER JOIN item_cardapio ON item_cardapio_pedido.id_item_cardapio = item_cardapio.id
        WHERE pedido.id_user = ? ORDER BY pedido.id ASC;
    """, (user_id,)).fetchall()

    for i in query:
        pedido_id, pedido_total, pedido_ativo, item_nome, item_preco, item_quantidade, item_observacao = i

        if pedido_id not in pedidos_agrupados:
            pedidos_agrupados[pedido_id] = {
                'id_pedido': pedido_id,
                'total': pedido_total,
                'ativo': int(pedido_ativo),
                'observacao' : item_observacao,
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

@app.route('/carrinho/remove/<int:id>')
def carrinho_remove(id):
    lista_pedidos = request.cookies.get('pedidos', '[]')

    if lista_pedidos:
        lista_pedidos = json.loads(lista_pedidos)
        for pedido in lista_pedidos:
            if int(pedido['id_carrinho']) == int(id):
                lista_pedidos.remove(pedido)
                break
    

    resp = redirect(url_for('carrinho'))
    resp.set_cookie('pedidos', json.dumps(lista_pedidos), path = '/')

    return resp

@app.route('/pedido/cancelar/<int:id>', methods=['GET', 'POST'])
def pedido_cancelar(id):
    user_id = session.get('user_id', 1)
        
    conn = criar_conexao()
    conn.execute("""
        UPDATE pedido 
        SET active = 0
        WHERE id = ? AND id_user = ?;
    """, (id, user_id))
        
    conn.commit()
    conn.close()
    return redirect(url_for('perfil'))

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