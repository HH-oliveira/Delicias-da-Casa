"""
testar_backend.py
-------------------
Testa a lógica do banco de dados e do login SEM precisar de HTML
nem de navegador. Roda direto no terminal.

Como rodar:
    python testar_backend.py
"""

from app import app
from models import db, Usuario

with app.app_context():
    db.create_all()  # garante que a tabela existe

    print("=== Testando login por usuário ===\n")

    usuario_digitado = "admin"
    senha_digitada = "1234"

    usuario = Usuario.query.filter(
        (Usuario.usuario == usuario_digitado) | (Usuario.email == usuario_digitado)
    ).first()

    if usuario is None:
        print(f"Usuário '{usuario_digitado}' não encontrado no banco.")
        print("Rode antes: python criar_usuario.py")
    elif usuario.checar_senha(senha_digitada):
        print(f"Login OK! Bem-vindo(a), {usuario.usuario}.")
    else:
        print("Usuário existe, mas a senha está errada.")

    print("\n=== Testando login por email ===\n")

    email_digitado = "admin@deliciasdacasa.com"
    usuario_por_email = Usuario.query.filter(
        (Usuario.usuario == email_digitado) | (Usuario.email == email_digitado)
    ).first()

    if usuario_por_email and usuario_por_email.checar_senha(senha_digitada):
        print(f"Login por email OK! Bem-vindo(a), {usuario_por_email.usuario}.")
    else:
        print("Login por email falhou (rode 'python criar_usuario.py' para atualizar o email).")

    print("\n=== Testando senha errada de propósito ===\n")
    if usuario and not usuario.checar_senha("senha_errada_de_proposito"):
        print("Confirmado: senha errada foi rejeitada corretamente.")