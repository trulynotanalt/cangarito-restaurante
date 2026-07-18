from database import db

class Pedido(db.Model):
    __tablename__ = 'pedido'
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'))
    observacao = db.Column(db.Text)
    subtotal = db.Column(db.Float)
    imposto = db.Column(db.Float)
    total = db.Column(db.Float)
    active = db.Column(db.Boolean)

class ItemCardapioPedido(db.Model):
    __tablename__ = 'item_cardapio_pedido'
    id_pedido = db.Column(db.Integer, db.ForeignKey('pedido.id'), primary_key=True)
    id_item_cardapio = db.Column(db.Integer, db.ForeignKey('item_cardapio.id'), primary_key=True)
    quantidade = db.Column(db.Integer)