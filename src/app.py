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
    
# --- Serviços ---
@app.route("/servicos")
def servicos():
    if "usuario_id" not in session:
        return redirect(url_for("login"))
    registros = query("SELECT * FROM servicos ORDER BY nome", fetch="all")
    return render_template("servicos.html", servicos=registros)

@app.route("/servicos/novo", methods=["POST"])
def servico_novo():
    if "usuario_id" not in session:
        return redirect(url_for("login"))
    query("""
        INSERT INTO servicos (nome, descricao, preco, duracao_min)
        VALUES (%s, %s, %s, %s)
    """, (
        request.form["nome"],
        request.form.get("descricao", ""),
        request.form["preco"],
        request.form["duracao_min"]
    ))
    return redirect(url_for("servicos"))

@app.route("/servicos/editar/<id>", methods=["POST"])
def servico_editar(id):
    if "usuario_id" not in session:
        return redirect(url_for("login"))
    query("""
        UPDATE servicos 
        SET nome=%s, descricao=%s, preco=%s, duracao_min=%s, ativo=%s
        WHERE id=%s
    """, (
        request.form["nome"],
        request.form.get("descricao", ""),
        request.form["preco"],
        request.form["duracao_min"],
        request.form.get("ativo") == "on",
        id
    ))
    return redirect(url_for("servicos"))

@app.route("/servicos/deletar/<id>", methods=["POST"])
def servico_deletar(id):
    if "usuario_id" not in session:
        return redirect(url_for("login"))
    query("DELETE FROM servicos WHERE id=%s", (id,))
    return redirect(url_for("servicos"))
    
    # --- Barbeiros ---
@app.route("/barbeiros")
def barbeiros():
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    registros = query("""
        SELECT 
            u.id, u.nome, u.email, u.telefone,
            COUNT(a.id) AS total_agendamentos
        FROM usuarios u
        LEFT JOIN agendamentos a ON a.barbeiro_id = u.id
        WHERE u.role = 'barbeiro'
        GROUP BY u.id, u.nome, u.email, u.telefone
        ORDER BY u.nome
    """, fetch="all")
    return render_template("barbeiros.html", barbeiros=registros)

@app.route("/barbeiros/novo", methods=["POST"])
def barbeiro_novo():
    if "usuario_id" not in session:
        return redirect(url_for("login"))
    query("""
        INSERT INTO usuarios (nome, email, senha_hash, role, telefone)
        VALUES (%s, %s, %s, 'barbeiro', %s)
    """, (
        request.form["nome"],
        request.form["email"],
        __import__('hashlib').sha256(request.form["senha"].encode()).hexdigest(),
        request.form.get("telefone", "")
    ))
    return redirect(url_for("barbeiros"))

@app.route("/barbeiros/deletar/<id>", methods=["POST"])
def barbeiro_deletar(id):
    if "usuario_id" not in session:
        return redirect(url_for("login"))
    query("DELETE FROM usuarios WHERE id=%s AND role='barbeiro'", (id,))
    return redirect(url_for("barbeiros"))

# --- Clientes ---
@app.route("/clientes")
def clientes():
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    registros = query("""
        SELECT 
            u.id, u.nome, u.email, u.telefone,
            COUNT(a.id) AS total_agendamentos
        FROM usuarios u
        LEFT JOIN agendamentos a ON a.cliente_id = u.id
        WHERE u.role = 'cliente'
        GROUP BY u.id, u.nome, u.email, u.telefone
        ORDER BY u.nome
    """, fetch="all")
    return render_template("clientes.html", clientes=registros)

@app.route("/clientes/deletar/<id>", methods=["POST"])
def cliente_deletar(id):
    if "usuario_id" not in session:
        return redirect(url_for("login"))
    query("DELETE FROM usuarios WHERE id=%s AND role='cliente'", (id,))
    return redirect(url_for("clientes"))

if __name__ == "__main__":
    app.run(debug=True)