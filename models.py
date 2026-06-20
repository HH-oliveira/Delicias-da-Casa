"""
models.py
----------
Aqui ficam as classes que representam as tabelas do banco de dados.
Cada classe = uma tabela do seu diagrama UML.

Por enquanto só temos Usuario (login). As outras (Pedido, ItemPedido,
Produto, Financeiro) vamos adicionar nos próximos passos.

se vc leu vc é gay
"""

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# 'db' é o objeto que conecta o Flask ao banco de dados.
# Ele é criado aqui e importado no app.py.
db = SQLAlchemy()


class Usuario(db.Model):
    __tablename__ = "usuario"

    # Corresponde ao diagrama: id: int (pk)
    id = db.Column(db.Integer, primary_key=True)

    # Corresponde ao diagrama: usuario: String
    usuario = db.Column(db.String(80), unique=True, nullable=False)

    # Campo novo (não estava no diagrama original): permite logar com email.
    email = db.Column(db.String(120), unique=True, nullable=True)

    # Corresponde ao diagrama: senha: String
    # IMPORTANTE: nunca guardamos a senha "crua" aqui, só o hash dela.
    senha_hash = db.Column(db.String(255), nullable=False)

    def set_senha(self, senha_texto_puro):
        """Transforma a senha digitada em um hash seguro antes de salvar."""
        self.senha_hash = generate_password_hash(senha_texto_puro)

    def checar_senha(self, senha_texto_puro):
        """Compara a senha digitada no login com o hash salvo no banco."""
        return check_password_hash(self.senha_hash, senha_texto_puro)

    def __repr__(self):
        return f"<Usuario {self.usuario}>"