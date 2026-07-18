from database import db
class Item_Cardapio(db.Model):
    __tablename__ = "item_cardapio"

    id = db.Column(db.Integer, primary_key =True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Numeric,nullable=False)
    desc = db.Column(db.String,nullable=False)
    classificacao = db.Column(db.String,nullable=False)