from flask import Flask, render_template, request, redirect, session, url_for
from database import query
import hashlib

app = Flask(__name__)
app.secret_key = "bodies_barber_secret"


def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()


def usuario_logado():
    return session.get("usuario_id")


# ──────────────────────────────────────────────
# AUTH
# ──────────────────────────────────────────────

@app.route("/")
def index():
    if usuario_logado():
        return redirect(url_for("dashboard"))
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
            session["usuario_perfil"] = usuario["role"]
            return redirect(url_for("dashboard"))
        erro = "E-MAIL OU SENHA INVÁLIDOS"
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
        telefone = request.form.get("telefone", "")
        senha = hash_senha(request.form["senha"])

        existente = query("SELECT id FROM usuarios WHERE email = %s", (email,), fetch="one")
        if existente:
            erro = "E-MAIL JÁ CADASTRADO"
        else:
            query(
                "INSERT INTO usuarios (nome, email, telefone, senha_hash, role) VALUES (%s, %s, %s, %s, 'cliente')",
                (nome, email, telefone, senha)
            )
            sucesso = "CONTA CRIADA COM SUCESSO"
    return render_template("cadastro.html", erro=erro, sucesso=sucesso)


# ──────────────────────────────────────────────
# DASHBOARD
# ──────────────────────────────────────────────

@app.route("/dashboard")
def dashboard():
    if not usuario_logado():
        return redirect(url_for("login"))
    return render_template("dashboard.html",
                           nome=session.get("usuario_nome"),
                           perfil=session.get("usuario_perfil"))


# ──────────────────────────────────────────────
# AGENDAMENTOS  (usa PROCEDURE para confirmar)
# ──────────────────────────────────────────────

@app.route("/agendamentos")
def agendamentos():
    if not usuario_logado():
        return redirect(url_for("login"))

    filtro_status = request.args.get("status", "")
    filtro_barbeiro = request.args.get("barbeiro_id", "")

    sql = """
        SELECT a.id, a.data_hora, a.status, a.observacoes,
               c.nome AS cliente, b.nome AS barbeiro,
               s.nome AS servico, s.preco
        FROM agendamentos a
        INNER JOIN usuarios c ON c.id = a.cliente_id
        INNER JOIN usuarios b ON b.id = a.barbeiro_id
        INNER JOIN servicos s  ON s.id = a.servico_id
        WHERE 1=1
    """
    params = []
    if filtro_status:
        sql += " AND a.status = %s"
        params.append(filtro_status)
    if filtro_barbeiro:
        sql += " AND a.barbeiro_id = %s"
        params.append(filtro_barbeiro)
    sql += " ORDER BY a.data_hora DESC"

    lista = query(sql, params, fetch="all") or []
    barbeiros = query("SELECT id, nome FROM usuarios WHERE role = 'barbeiro' ORDER BY nome", fetch="all") or []
    servicos = query("SELECT id, nome, preco FROM servicos ORDER BY nome", fetch="all") or []
    clientes = query("SELECT id, nome FROM usuarios WHERE role = 'cliente' ORDER BY nome", fetch="all") or []

    return render_template("agendamentos.html",
                           agendamentos=lista,
                           barbeiros=barbeiros,
                           servicos=servicos,
                           clientes=clientes,
                           filtro_status=filtro_status,
                           filtro_barbeiro=filtro_barbeiro,
                           perfil=session.get("usuario_perfil"))


@app.route("/agendamentos/novo", methods=["POST"])
def agendamento_novo():
    if not usuario_logado():
        return redirect(url_for("login"))
    query(
        """INSERT INTO agendamentos (cliente_id, barbeiro_id, servico_id, data_hora, observacoes)
           VALUES (%s, %s, %s, %s, %s)""",
        (request.form["cliente_id"], request.form["barbeiro_id"],
         request.form["servico_id"], request.form["data_hora"],
         request.form.get("observacoes", ""))
    )
    return redirect(url_for("agendamentos"))


@app.route("/agendamentos/status/<id>", methods=["POST"])
def agendamento_status(id):
    """
    Se o novo status for 'confirmado', usa a PROCEDURE sp_confirmar_agendamento.
    Para outros status, usa UPDATE direto.
    """
    if not usuario_logado():
        return redirect(url_for("login"))

    novo_status = request.form["status"]

    if novo_status == "confirmado":
        # ✅ Chama a PROCEDURE criada no banco
        query("CALL sp_confirmar_agendamento(%s)", (id,))
    else:
        query(
            "UPDATE agendamentos SET status = %s WHERE id = %s",
            (novo_status, id)
        )
    return redirect(url_for("agendamentos"))


@app.route("/agendamentos/deletar/<id>", methods=["POST"])
def agendamento_deletar(id):
    if not usuario_logado():
        return redirect(url_for("login"))
    query("DELETE FROM agendamentos WHERE id = %s", (id,))
    return redirect(url_for("agendamentos"))


# ──────────────────────────────────────────────
# RELATÓRIO  (usa a VIEW vw_agendamentos_completos)
# ──────────────────────────────────────────────

@app.route("/relatorio")
def relatorio():
    """
    Demonstra o uso da VIEW vw_agendamentos_completos.
    Consulta simples na view — sem JOINs manuais no Python.
    """
    if not usuario_logado():
        return redirect(url_for("login"))

    filtro_status = request.args.get("status", "")
    filtro_barbeiro = request.args.get("barbeiro_id", "")

    sql = "SELECT * FROM vw_agendamentos_completos WHERE 1=1"
    params = []
    if filtro_status:
        sql += " AND status = %s"
        params.append(filtro_status)
    if filtro_barbeiro:
        sql += " AND barbeiro_id::text = %s"
        params.append(filtro_barbeiro)
    sql += " ORDER BY data_hora DESC"

    registros = query(sql, params, fetch="all") or []
    barbeiros = query("SELECT id, nome FROM usuarios WHERE role = 'barbeiro' ORDER BY nome", fetch="all") or []

    # Totalizador por status (para exibir resumo)
    totais = query("""
        SELECT status, COUNT(*) AS qtd, COALESCE(SUM(preco), 0) AS total
        FROM vw_agendamentos_completos
        GROUP BY status
        ORDER BY status
    """, fetch="all") or []

    return render_template("relatorio.html",
                           registros=registros,
                           barbeiros=barbeiros,
                           totais=totais,
                           filtro_status=filtro_status,
                           filtro_barbeiro=filtro_barbeiro,
                           perfil=session.get("usuario_perfil"),
                           nome=session.get("usuario_nome"))


# ──────────────────────────────────────────────
# SERVIÇOS
# ──────────────────────────────────────────────

@app.route("/servicos", methods=["GET", "POST"])
def servicos():
    if not usuario_logado():
        return redirect(url_for("login"))

    erro = None
    if request.method == "POST":
        nome = request.form["nome"]
        preco = request.form["preco"]
        duracao = request.form["duracao_min"]
        query(
            "INSERT INTO servicos (nome, preco, duracao_min) VALUES (%s, %s, %s)",
            (nome, preco, duracao)
        )
        return redirect(url_for("servicos"))

    lista = query("SELECT * FROM servicos ORDER BY nome", fetch="all") or []
    return render_template("servicos.html", servicos=lista, erro=erro,
                           perfil=session.get("usuario_perfil"),
                           nome=session.get("usuario_nome"))


@app.route("/servicos/editar/<id>", methods=["POST"])
def servico_editar(id):
    if not usuario_logado():
        return redirect(url_for("login"))
    query(
        "UPDATE servicos SET nome = %s, preco = %s, duracao_min = %s WHERE id = %s",
        (request.form["nome"], request.form["preco"], request.form["duracao_min"], id)
    )
    return redirect(url_for("servicos"))


@app.route("/servicos/deletar/<id>", methods=["POST"])
def servico_deletar(id):
    if not usuario_logado():
        return redirect(url_for("login"))
    query("DELETE FROM servicos WHERE id = %s", (id,))
    return redirect(url_for("servicos"))


# ──────────────────────────────────────────────
# BARBEIROS  (usa FUNCTION fn_faturamento_barbeiro)
# ──────────────────────────────────────────────

@app.route("/barbeiros", methods=["GET", "POST"])
def barbeiros():
    if not usuario_logado():
        return redirect(url_for("login"))

    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        telefone = request.form.get("telefone", "")
        senha = hash_senha(request.form.get("senha", "senha123"))
        query(
            "INSERT INTO usuarios (nome, email, telefone, senha_hash, role) VALUES (%s, %s, %s, %s, 'barbeiro')",
            (nome, email, telefone, senha)
        )
        return redirect(url_for("barbeiros"))

    # LEFT JOIN: inclui barbeiros sem agendamento
    lista_raw = query("""
        SELECT b.id, b.nome, b.email, b.telefone,
               COUNT(a.id) AS total_agendamentos
        FROM usuarios b
        LEFT JOIN agendamentos a ON a.barbeiro_id = b.id
        WHERE b.role = 'barbeiro'
        GROUP BY b.id, b.nome, b.email, b.telefone
        ORDER BY b.nome
    """, fetch="all") or []

    # ✅ Chama a FUNCTION para cada barbeiro
    barbeiros_com_fat = []
    for b in lista_raw:
        fat = query(
            "SELECT fn_faturamento_barbeiro(%s) AS faturamento",
            (str(b["id"]),),
            fetch="one"
        )
        barbeiros_com_fat.append({
            **b,
            "faturamento": fat["faturamento"] if fat else 0
        })

    return render_template("barbeiros.html",
                           barbeiros=barbeiros_com_fat,
                           perfil=session.get("usuario_perfil"),
                           nome=session.get("usuario_nome"))


@app.route("/barbeiros/deletar/<id>", methods=["POST"])
def barbeiro_deletar(id):
    if not usuario_logado():
        return redirect(url_for("login"))
    query("DELETE FROM usuarios WHERE id = %s AND role = 'barbeiro'", (id,))
    return redirect(url_for("barbeiros"))


# ──────────────────────────────────────────────
# CLIENTES
# ──────────────────────────────────────────────

@app.route("/clientes")
def clientes():
    if not usuario_logado():
        return redirect(url_for("login"))

    lista = query("""
        SELECT c.id, c.nome, c.email, c.telefone,
               COUNT(a.id) AS total_agendamentos
        FROM usuarios c
        LEFT JOIN agendamentos a ON a.cliente_id = c.id
        WHERE c.role = 'cliente'
        GROUP BY c.id, c.nome, c.email, c.telefone
        ORDER BY c.nome
    """, fetch="all") or []

    return render_template("clientes.html", clientes=lista,
                           perfil=session.get("usuario_perfil"),
                           nome=session.get("usuario_nome"))


@app.route("/clientes/deletar/<id>", methods=["POST"])
def cliente_deletar(id):
    if not usuario_logado():
        return redirect(url_for("login"))
    query("DELETE FROM usuarios WHERE id = %s AND role = 'cliente'", (id,))
    return redirect(url_for("clientes"))


# ──────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)