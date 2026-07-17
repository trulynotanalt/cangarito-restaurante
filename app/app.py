import json
from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import login_manager, login_required, login_user
from database import db
from db import alimentar_banco, criar_conexao
from item_cardapio import Item_Cardapio
import json

app = Flask(__name__)
app.secret_key = "GloriaAJesus"
login_manager.init_app(app)
login_manager.login_view = "cadastro"

@login_manager.user_loader
def load_user(user_id):
    return User.buscar_id(criar_conexao(), user_id)

# pega lista do banco e transforma em objetos
def construtor_itens_cardapio(lista_pedidos):
    lista_obj = []
    for i in lista_pedidos:
        obj = Item_Cardapio(i[1], i[2], i[3])  # monta objeto
        lista_obj.append(obj)
    return lista_obj

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app) 

from modelos.User import *
from modelos.item_cardapio import *
from modelos.pedido import *

# cria e injeta os itens ao cardapio
alimentar_banco(app)


@app.route('/')
def landingpage():
    return render_template('landing-page.html')


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
   
    if 'usuario' in session:
        return redirect(url_for('landingpage'))
    
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        email = request.form.get('email')
        senha = request.form.get('senha')
        c_senha = request.form.get('c_senha')

        # salva o usuario
        novo_usuario = User(nome=usuario, email=email, senha=c_senha, type='normal')
        db.session.add(novo_usuario)
        db.session.commit()

        return redirect(url_for('login'))
    
    return render_template('cadastro.html')


@app.route('/cardapio', methods=['GET', 'POST'])
@login_required
def cardapio():

    if request.method == 'GET':
        # busca itens pela categoria
        itens_cuscuz = ItemCardapio.query.filter_by(classificacao='cuscuz').all()
        itens_sobremesa = ItemCardapio.query.filter_by(classificacao='sobremesa').all()
        itens_campeao_vendas = ItemCardapio.query.filter_by(classificacao='campeao_vendas').all()
        itens_bebidas = ItemCardapio.query.filter_by(classificacao='bebidas').all()
        
        return render_template(
            'cardapio.html',
            itens_sobremesa=itens_sobremesa,
            itens_cuscuz=itens_cuscuz,
            itens_campeao_vendas=itens_campeao_vendas,
            itens_bebidas=itens_bebidas
        )
    
        
    nome_produto = request.form.get('nome_produto').replace('R$', '')
    preco_produto = request.form.get('preco_produto').replace('R$', '')
    quantidade = request.form.get('quantidade_pedido').replace('R$', '')
    observacao = request.form.get('observacao').replace('R$', '')
    
    lista_pedidos = request.cookies.get('pedidos', '[]')
    
    pedido = {
        'id_carrinho': 0,
        'nome': nome_produto,
        'preco': preco_produto,
        'quantidade': quantidade,
        'observacao': observacao,
    }

    # transforma cookie em lista e adiciona item
    if lista_pedidos:
        lista_pedidos = json.loads(lista_pedidos)
        pedido['id_carrinho'] = int(len(lista_pedidos))
        lista_pedidos.append(pedido)
   
    resp = redirect(url_for('cardapio'))
    resp.set_cookie('pedidos', json.dumps(lista_pedidos), path='/')
    return resp


@app.route('/carrinho', methods=['GET', 'POST'])
@login_required
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

        return render_template(
            'carrinho.html',
            pedidos=lista_pedidos,
            subtotal=subtotal,
            imposto=imposto,
            total=total
        )
    
    lista_pedidos = json.loads(request.cookies.get('pedidos', '[]'))

    if not lista_pedidos:
        return redirect(url_for('cardapio'))

    subtotal = 0
    observacoes = []

    # soma valores e junta observações
    for item in lista_pedidos:
        subtotal += float(item['preco']) * int(item['quantidade'])
        if item['observacao']:
            observacoes.append(f"{item['nome']}: {item['observacao']}")

    imposto = subtotal * 0.02
    total = subtotal + imposto
    observacao_geral = "; ".join(observacoes)
    
    # salva pedido
    novo_pedido = Pedido(id_user=user_id, observacao=observacao_geral, subtotal=subtotal, imposto=imposto, total=total, active=1)
    db.session.add(novo_pedido)
    db.session.flush()
    id_pedido_gerado = novo_pedido.id

    # salva itens do pedido 
    for item in lista_pedidos:
        # busca o produto correto
        item_db = ItemCardapio.query.filter_by(name=item['nome']).first()

        if item_db:
            id_item_cardapio = item_db.id
            # cria pedido
            novo_item_pedido = ItemCardapioPedido(id_pedido=id_pedido_gerado, id_item_cardapio=id_item_cardapio, quantidade=item['quantidade'])
            db.session.add(novo_item_pedido)

    db.session.commit()
    
    resp = redirect(url_for('perfil'))
    resp.set_cookie('pedidos', '[]', path='/')
    return resp


@app.route('/happyhour')
@login_required
def happyhour():
    if 'usuario' not in session:
        return redirect(url_for('cadastro'))
    
    return render_template('happyhour.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        nome_user = request.form['nome']
        email_user = request.form['email']
        passw_user = request.form['senha']
        with criar_conexao() as conexao:
            user = User.buscar_email(conexao, email_user)

        if user is None or user.nome != nome_user or not user.validar_senha(passw_user):
            return redirect(url_for('login'))
        
        login_user(user)
        return redirect(url_for('landingpage'))
    
    return render_template('login.html')

@app.route("/pesquisar-itens")
def pesquisar_itens():
    input = request.args.get("input").lower().strip()
    
    conn = criar_conexao()

    itens_cuscuz = construtor_itens_cardapio(
        list(conn.execute("SELECT * FROM item_cardapio WHERE classificacao = 'cuscuz' AND name LIKE ?", (f"%{input}%",)).fetchall())
    )
    itens_sobremesa = construtor_itens_cardapio(
        list(conn.execute("SELECT * FROM item_cardapio WHERE classificacao = 'sobremesa' AND name LIKE ?", (f"%{input}%",)).fetchall())
    )
    itens_campeao_vendas = construtor_itens_cardapio(
        list(conn.execute("SELECT * FROM item_cardapio WHERE classificacao = 'campeao_vendas' AND name LIKE ?", (f"%{input}%",)).fetchall())
    )
    itens_bebidas = construtor_itens_cardapio(
        list(conn.execute("SELECT * FROM item_cardapio WHERE classificacao = 'bebidas' AND name LIKE ?", (f"%{input}%",)).fetchall())
    )

    conn.close()

        
    return render_template(
        'cardapio.html',
        itens_sobremesa=itens_sobremesa,
        itens_cuscuz=itens_cuscuz,
        itens_campeao_vendas=itens_campeao_vendas,
        itens_bebidas=itens_bebidas
    )





@app.route('/perfil', methods=['GET'])
@login_required
def perfil():
    
    if 'usuario' not in session:
        return redirect(url_for('login'))

    user_id = session.get('user_id', 1)
    pedidos_agrupados = {}
   
    # faz o join entre as tabelas do sqlalchemy
    query = db.session.query(
        Pedido.id,
        Pedido.total,
        Pedido.active,
        ItemCardapio.name,
        ItemCardapio.preco,
        ItemCardapioPedido.quantidade,
        Pedido.observacao
    ).join(ItemCardapioPedido, Pedido.id == ItemCardapioPedido.id_pedido)\
     .join(ItemCardapio, ItemCardapioPedido.id_item_cardapio == ItemCardapio.id)\
     .filter(Pedido.id_user == user_id)\
     .order_by(Pedido.id.asc())\
     .all()

    # organiza pedidos por ID 
    for i in query:
        pedido_id, pedido_total, pedido_ativo, item_nome, item_preco, item_quantidade, item_observacao = i

        if pedido_id not in pedidos_agrupados:
            pedidos_agrupados[pedido_id] = {
                'id_pedido': pedido_id,
                'total': pedido_total,
                'ativo': int(pedido_ativo),
                'observacao': item_observacao,
                'itens_comprados': []
            }

        pedidos_agrupados[pedido_id]['itens_comprados'].append({
            'nome': item_nome,
            'preco': item_preco,
            'quantidade': item_quantidade
        })

    lista_pedidos = list(pedidos_agrupados.values())
    return render_template('perfil.html', lista_pedidos=lista_pedidos)


@app.route('/carrinho/remove/<int:id>')
def carrinho_remove(id):

    # remove item do cookie do carrinho 
    lista_pedidos = request.cookies.get('pedidos', '[]')

    if lista_pedidos:
        lista_pedidos = json.loads(lista_pedidos)

        for pedido in lista_pedidos:
            if int(pedido['id_carrinho']) == int(id):
                lista_pedidos.remove(pedido)
                break

    resp = redirect(url_for('carrinho'))
    resp.set_cookie('pedidos', json.dumps(lista_pedidos), path='/')
    return resp


@app.route('/pedido/cancelar/<int:id>', methods=['GET', 'POST'])
def pedido_cancelar(id):

    user_id = session.get('user_id', 1)

    # atualiza o status do pedido
    pedido = Pedido.query.filter_by(id=id, id_user=user_id).first()
    if pedido:
        pedido.active = 0
        db.session.commit()

    return redirect(url_for('perfil'))


@app.route('/logout', methods=["POST"])
def logout():
    session.pop('usuario', None)
    session.pop('user_id', None)
    return redirect(url_for('landingpage'))


@app.route('/trocarsenha', methods=['GET', 'POST'])
# bloqueia se não estiver logado
@login_required
def trocarsenha():

    if request.method == 'POST':
        # pega nova senha
        nova_senha = request.form.get('novasenha')
        confirmar_senha = request.form.get('confirmarsenha')
        
        if nova_senha != confirmar_senha:
            return redirect(url_for('trocarsenha'))

        email_usuario = session['usuario']['email']

        # atualiza a senha do usuario
        usuario_db = User.query.filter_by(email=email_usuario).first()
        if usuario_db:
            usuario_db.senha = nova_senha
            db.session.commit()

        session['usuario']['senha'] = nova_senha
        return redirect(url_for('perfil'))

    return render_template('trocarsenha.html')


if __name__ == "__main__":
    app.run(debug=True)