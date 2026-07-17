from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, nome, email, senha,type='normal', id=None, senha_hash=False):
        self.id = id
        self.nome = nome
        self.email = email
        self.type = type
        self.senha = senha if senha_hash else generate_password_hash(senha)
        
    def save(self, conexao):
        with conexao:
            cursor = conexao.execute(
                """
                INSERT INTO users (nome, email, type, password)
                VALUES (?, ?, ?, ?)
                """,
                (self.nome, self.email, self.type, self.senha),
            )
            self.id = cursor.lastrowid

    def validar_senha(self, senha):
        return check_password_hash(self.senha, senha)

    def get_id(self):
        return str(self.id)

    @classmethod
    def buscar_email(cls, conexao, email):
        usuario = conexao.execute(
            "SELECT id, nome, email, type, password FROM users WHERE email = ?",
            (email,),
        ).fetchone()

        if usuario is None:
            return None

        return cls(
            id=usuario["id"],
            nome=usuario["nome"],
            email=usuario["email"],
            type=usuario["type"],
            senha=usuario["password"],
            senha_hash=True,
        )

    @classmethod
    def buscar_id(cls, conexao, id):
        usuario = conexao.execute(
            "SELECT id, nome, email, type, password FROM users WHERE id = ?",
            (id,),
        ).fetchone()

        if usuario is None:
            return None

        return cls(
            id=usuario["id"],
            nome=usuario["nome"],
            email=usuario["email"],
            type=usuario["type"],
            senha=usuario["password"],
            senha_hash=True,
        )
