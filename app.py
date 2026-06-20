"""
app.py
------
Arquivo principal da aplicação Flask.

Como rodar:
    python app.py

Depois abra no navegador: http://127.0.0.1:5000
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db, Usuario

app = Flask(__name__)

# Chave secreta usada pelo Flask para proteger a sessão do usuário logado.
# Em produção isso deveria vir de uma variável de ambiente, não ficar fixo no código.
app.config["SECRET_KEY"] = "troque-esta-chave-depois"

# Onde o arquivo do banco SQLite vai ser criado (na mesma pasta do projeto).
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///banco.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


@app.route("/")
def home():
    # Se não tiver usuário na sessão, manda pro login.
    if "usuario_id" not in session:
        return redirect(url_for("login"))
    return f"Bem-vindo(a), {session['usuario_nome']}! (área interna ainda vai ser construída)"


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login_digitado = request.form.get("login", "").strip()
        senha_digitada = request.form.get("senha", "")

        # Aceita tanto nome de usuário quanto email no mesmo campo.
        usuario = Usuario.query.filter(
            (Usuario.usuario == login_digitado) | (Usuario.email == login_digitado)
        ).first()

        if usuario and usuario.checar_senha(senha_digitada):
            # Login certo: guarda o id do usuário na sessão
            session["usuario_id"] = usuario.id
            session["usuario_nome"] = usuario.usuario
            return redirect(url_for("home"))
        else:
            flash("Usuário ou senha inválidos.")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    with app.app_context():
        # Cria o arquivo banco.db e as tabelas, se ainda não existirem.
        db.create_all()
    app.run(debug=True)