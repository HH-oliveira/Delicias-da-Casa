"""
criar_usuario.py
-----------------
Script simples para cadastrar um usuário direto no banco,
já que ainda não temos uma tela de cadastro.

Como rodar:
    python criar_usuario.py
"""

from app import app
from models import db, Usuario

NOME_USUARIO = "admin"
EMAIL_USUARIO = "admin@deliciasdacasa.com"
SENHA = "1234"  # troque por uma senha sua

with app.app_context():
    db.create_all()  # garante que as tabelas existem

    existente = Usuario.query.filter_by(usuario=NOME_USUARIO).first()
    if existente:
        # Se o usuário já existe mas ainda não tem email salvo, atualiza.
        if not existente.email:
            existente.email = EMAIL_USUARIO
            db.session.commit()
            print(f"Usuário '{NOME_USUARIO}' já existia. Email adicionado: {EMAIL_USUARIO}")
        else:
            print(f"Usuário '{NOME_USUARIO}' já existe. Nada foi feito.")
    else:
        novo_usuario = Usuario(usuario=NOME_USUARIO, email=EMAIL_USUARIO)
        novo_usuario.set_senha(SENHA)
        db.session.add(novo_usuario)
        db.session.commit()
        print(f"Usuário '{NOME_USUARIO}' criado com sucesso!")