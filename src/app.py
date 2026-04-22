from flask import Flask, render_template, request, redirect, url_for, session
from database import query
import hashlib

app = Flask(__name__)
app.secret_key = "bodies_barber_secret_123"

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

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

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    erro = None
    sucesso = None
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = hash_senha(request.form["senha"])
        telefone = request.form.get("telefone", "")
        existente = query(
            "SELECT id FROM usuarios WHERE email = %s",
            (email,),
            fetch="one"
        )
        if existente:
            erro = "E-mail já cadastrado."
        else:
            query(
                """INSERT INTO usuarios (nome, email, senha_hash, role, telefone)
                   VALUES (%s, %s, %s, 'cliente', %s)""",
                (nome, email, senha, telefone)
            )
            sucesso = "Conta criada! Faça o login."
    return render_template("cadastro.html", erro=erro, sucesso=sucesso)

@app.route("/dashboard")
def dashboard():
    if "usuario_id" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", usuario=session["usuario_nome"])

# --- Agendamentos ---
@app.route("/agendamentos")
def agendamentos():
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    # INNER JOIN — só agendamentos com cliente, barbeiro e serviço válidos
    registros = query("""
        SELECT 
            a.id,
            a.data_hora,
            a.status,
            a.observacoes,
            c.nome AS cliente_nome,
            b.nome AS barbeiro_nome,
            s.nome AS servico_nome,
            s.preco
        FROM agendamentos a
        INNER JOIN usuarios c ON c.id = a.cliente_id
        INNER JOIN usuarios b ON b.id = a.barbeiro_id
        INNER JOIN servicos s ON s.id = a.servico_id
        ORDER BY a.data_hora DESC
    """, fetch="all")

    barbeiros = query("""
        SELECT id, nome FROM usuarios 
        WHERE role = 'barbeiro' 
        ORDER BY nome
    """, fetch="all")

    servicos = query("""
        SELECT id, nome, preco FROM servicos 
        WHERE ativo = TRUE 
        ORDER BY nome
    """, fetch="all")

    clientes = query("""
        SELECT id, nome FROM usuarios 
        WHERE role = 'cliente' 
        ORDER BY nome
    """, fetch="all")

    return render_template("agendamentos.html",
        agendamentos=registros,
        barbeiros=barbeiros,
        servicos=servicos,
        clientes=clientes
    )

@app.route("/agendamentos/novo", methods=["POST"])
def agendamento_novo():
    if "usuario_id" not in session:
        return redirect(url_for("login"))
    query("""
        INSERT INTO agendamentos 
            (cliente_id, barbeiro_id, servico_id, data_hora, observacoes)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        request.form["cliente_id"],
        request.form["barbeiro_id"],
        request.form["servico_id"],
        request.form["data_hora"],
        request.form.get("observacoes", "")
    ))
    return redirect(url_for("agendamentos"))

@app.route("/agendamentos/status/<id>", methods=["POST"])
def agendamento_status(id):
    if "usuario_id" not in session:
        return redirect(url_for("login"))
    query("""
        UPDATE agendamentos SET status = %s WHERE id = %s
    """, (request.form["status"], id))
    return redirect(url_for("agendamentos"))

@app.route("/agendamentos/deletar/<id>", methods=["POST"])
def agendamento_deletar(id):
    if "usuario_id" not in session:
        return redirect(url_for("login"))
    query("DELETE FROM agendamentos WHERE id = %s", (id,))
    return redirect(url_for("agendamentos"))

if __name__ == "__main__":
    app.run(debug=True)