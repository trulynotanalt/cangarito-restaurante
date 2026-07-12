from database import db

class ItemCardapio(db.Model):
    __tablename__ = 'item_cardapio'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    preco = db.Column(db.Float)
    desc = db.Column(db.String)
    classificacao = db.Column(db.String)