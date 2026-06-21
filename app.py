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

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        usuario_digitado = request.form.get("usuario", "").strip()
        email_digitado = request.form.get("email", "").strip()
        email_confirmacao = request.form.get("email_confirmacao", "").strip()
        senha_digitada = request.form.get("senha", "")
        senha_confirmacao = request.form.get("senha_confirmacao", "")

        # --- Validações, na ordem que faz mais sentido mostrar pro usuário ---

        if not usuario_digitado or not email_digitado or not senha_digitada:
            flash("Preencha todos os campos.")
            return redirect(url_for("cadastro"))

        if email_digitado != email_confirmacao:
            flash("Os emails digitados não coincidem.")
            return redirect(url_for("cadastro"))

        if senha_digitada != senha_confirmacao:
            flash("As senhas digitadas não coincidem.")
            return redirect(url_for("cadastro"))

        if len(senha_digitada) < 4:
            flash("A senha deve ter pelo menos 4 caracteres.")
            return redirect(url_for("cadastro"))

        # Verifica se usuário ou email já existem no banco
        ja_existe = Usuario.query.filter(
            (Usuario.usuario == usuario_digitado) | (Usuario.email == email_digitado)
        ).first()

        if ja_existe:
            flash("Usuário ou email já cadastrado.")
            return redirect(url_for("cadastro"))

        # Tudo certo: cria o novo usuário
        novo_usuario = Usuario(usuario=usuario_digitado, email=email_digitado)
        novo_usuario.set_senha(senha_digitada)
        db.session.add(novo_usuario)
        db.session.commit()

        flash("Cadastro realizado com sucesso! Faça login.")
        return redirect(url_for("login"))

    return render_template("cadastro.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))
 
 
if __name__ == "__main__":
    with app.app_context():
        # Cria o arquivo banco.db e as tabelas, se ainda não existirem.
        db.create_all()
    app.run(debug=True)




if __name__ == "__main__":
    with app.app_context():
        # Cria o arquivo banco.db e as tabelas, se ainda não existirem.
        db.create_all()
    app.run(debug=True)