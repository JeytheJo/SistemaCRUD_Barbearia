from flask import Flask, render_template, request, redirect, url_for, session
from database import query
import hashlib

app = Flask(__name__)
app.secret_key = "bodies_barber_secret_123"

# --- Utilidade ---
def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

# --- Rotas de autenticação ---
@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    erro = None
    if request.method == "POST":
        email = request.form["email"]
        senha = hash_senha(request.form["senha"])
        usuario = query(
            "SELECT * FROM usuarios WHERE email = %s AND senha_hash = %s",
            (email, senha),
            fetch="one"
        )
        if usuario:
            session["usuario_id"] = str(usuario["id"])
            session["usuario_nome"] = usuario["nome"]
            session["usuario_role"] = usuario["role"]
            return redirect(url_for("dashboard"))
        else:
            erro = "E-mail ou senha incorretos."
    return render_template("login.html", erro=erro)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/dashboard")
def dashboard():
    if "usuario_id" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", usuario=session["usuario_nome"])

if __name__ == "__main__":
    app.run(debug=True)