from flask import Flask, request, render_template_string
import sqlite3
from pathlib import Path

app = Flask(__name__)
DB_PATH = Path(__file__).parent / "signos.db"

# ============================================================
# BANCO DE DADOS
# ============================================================

def get_connection():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS signos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            simbolo TEXT NOT NULL,
            data_inicio TEXT NOT NULL,
            data_fim TEXT NOT NULL,
            elemento TEXT NOT NULL,
            qualidade TEXT NOT NULL,
            planeta TEXT NOT NULL,
            significado TEXT NOT NULL,
            atrai TEXT NOT NULL
        )
    """)

    cursor.execute("DELETE FROM signos")

    signos = [
        ("Áries", "♈", "21/03", "19/04", "Fogo", "Cardinal", "Marte",
         "Áries representa a iniciativa, a coragem e o impulso de começar. É o primeiro signo do zodíaco e simboliza o pioneirismo e a força de vontade.",
         "Atrai pessoas dinamicas, aventureiras e que não tenham medo de desafios. Costuma se interessar por quem tem energia e atitude."),
        
        ("Touro", "♉", "20/04", "20/05", "Terra", "Fixo", "Vênus",
         "Touro simboliza a estabilidade, o prazer sensorial e a construção sólida. Representa o valor das coisas materiais e o conforto.",
         "Atrai pessoas tranquilas, leais e que valorizam o conforto e a segurança. Gosta de quem transmite estabilidade e sensualidade."),
        
        ("Gêmeos", "♊", "21/05", "20/06", "Ar", "Mutável", "Mercúrio",
         "Gêmeos representa a comunicação, a dualidade e a curiosidade intelectual. É o signo da troca de ideias e da versatilidade.",
         "Atrai pessoas inteligentes, comunicativas e que gostam de conversar. Se interessa por mentes ágeis e que tenham assuntos interessantes."),
        
        ("Câncer", "♋", "21/06", "22/07", "Água", "Cardinal", "Lua",
         "Câncer simboliza o lar, a proteção emocional e a memória afetiva. Representa o instinto de cuidar e de se apegar.",
         "Atrai pessoas carinhosas, protetoras e que valorizam a família e o aconchego. Gosta de quem oferece segurança emocional."),
        
        ("Leão", "♌", "23/07", "22/08", "Fogo", "Fixo", "Sol",
         "Leão representa a criatividade, o orgulho e o desejo de brilhar. É o signo da generosidade e da autoexpressão.",
         "Atrai pessoas confiantes, carismáticas e que gostam de ser o centro das atenções. Se interessa por quem reconhece o seu valor."),
        
        ("Virgem", "♍", "23/08", "22/09", "Terra", "Mutável", "Mercúrio",
         "Virgem simboliza a análise, o aperfeiçoamento e o serviço. Representa o cuidado com os detalhes e a busca pela excelência.",
         "Atrai pessoas organizadas, inteligentes e que prestam atenção nos detalhes. Gosta de quem é prestativo e tem senso crítico."),
        
        ("Libra", "♎", "23/09", "22/10", "Ar", "Cardinal", "Vênus",
         "Libra representa o equilíbrio, a harmonia e os relacionamentos. É o signo da diplomacia e da busca pela justiça.",
         "Atrai pessoas charmosas, educadas e que buscam harmonia. Se interessa por quem tem bom gosto e sabe conversar."),
        
        ("Escorpião", "♏", "23/10", "21/11", "Água", "Fixo", "Plutão / Marte",
         "Escorpião simboliza a transformação, a intensidade e os mistérios da alma. Representa a paixão profunda e o poder regenerador.",
         "Atrai pessoas intensas, misteriosas e profundas. Gosta de quem tem presença forte e não tem medo da verdade."),
        
        ("Sagitário", "♐", "22/11", "21/12", "Fogo", "Mutável", "Júpiter",
         "Sagitário representa a expansão, a liberdade e a busca por sentido. É o signo da aventura e da filosofia de vida.",
         "Atrai pessoas otimistas, aventureiras e que gostam de viajar e aprender. Se interessa por quem tem mente aberta."),
        
        ("Capricórnio", "♑", "22/12", "19/01", "Terra", "Cardinal", "Saturno",
         "Capricórnio simboliza a ambição, a disciplina e a construção a longo prazo. Representa a maturidade e a responsabilidade.",
         "Atrai pessoas ambiciosas, sérias e que têm planos para o futuro. Gosta de quem demonstra comprometimento e estabilidade."),
        
        ("Aquário", "♒", "20/01", "18/02", "Ar", "Fixo", "Urano / Saturno",
         "Aquário representa a originalidade, a liberdade e o pensamento coletivo. É o signo da inovação e da independência.",
         "Atrai pessoas diferentes, independentes e com ideias inovadoras. Se interessa por quem respeita a liberdade individual."),
        
        ("Peixes", "♓", "19/02", "20/03", "Água", "Mutável", "Netuno / Júpiter",
         "Peixes simboliza a sensibilidade, a intuição e a conexão com o invisível. Representa o sonho, a compaixão e a arte.",
         "Atrai pessoas sensíveis, sonhadoras e compassivas. Gosta de quem tem empatia e consegue se conectar emocionalmente.")
    ]

    cursor.executemany("""
        INSERT INTO signos (nome, simbolo, data_inicio, data_fim, elemento, qualidade, planeta, significado, atrai)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, signos)

    conn.commit()
    conn.close()

# ============================================================
# LÓGICA DO SIGNO E COMPATIBILIDADE
# ============================================================

def encontrar_signo(dia: int, mes: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM signos")
    signos = cursor.fetchall()
    conn.close()

    data_nasc = mes * 100 + dia

    for signo in signos:
        inicio_dia, inicio_mes = map(int, signo["data_inicio"].split("/"))
        fim_dia, fim_mes = map(int, signo["data_fim"].split("/"))

        data_inicio = inicio_mes * 100 + inicio_dia
        data_fim = fim_mes * 100 + fim_dia

        if data_inicio > data_fim:
            if data_nasc >= data_inicio or data_nasc <= data_fim:
                return dict(signo)
        else:
            if data_inicio <= data_nasc <= data_fim:
                return dict(signo)
    return None

def calcular_compatibilidade(signo1: str, signo2: str) -> int:
    """Retorna uma porcentagem de 0 a 100 baseada em elementos e combinações clássicas."""
    
    # Tabela de compatibilidade (valores de 40 a 98)
    matriz = {
        "Áries":      {"Áries": 70, "Touro": 45, "Gêmeos": 80, "Câncer": 50, "Leão": 90, "Virgem": 55, "Libra": 75, "Escorpião": 60, "Sagitário": 95, "Capricórnio": 50, "Aquário": 85, "Peixes": 55},
        "Touro":      {"Áries": 45, "Touro": 75, "Gêmeos": 50, "Câncer": 85, "Leão": 55, "Virgem": 90, "Libra": 70, "Escorpião": 80, "Sagitário": 45, "Capricórnio": 95, "Aquário": 50, "Peixes": 85},
        "Gêmeos":     {"Áries": 80, "Touro": 50, "Gêmeos": 70, "Câncer": 55, "Leão": 85, "Virgem": 65, "Libra": 95, "Escorpião": 50, "Sagitário": 80, "Capricórnio": 45, "Aquário": 90, "Peixes": 60},
        "Câncer":     {"Áries": 50, "Touro": 85, "Gêmeos": 55, "Câncer": 75, "Leão": 60, "Virgem": 80, "Libra": 55, "Escorpião": 95, "Sagitário": 50, "Capricórnio": 75, "Aquário": 45, "Peixes": 90},
        "Leão":       {"Áries": 90, "Touro": 55, "Gêmeos": 85, "Câncer": 60, "Leão": 70, "Virgem": 50, "Libra": 80, "Escorpião": 65, "Sagitário": 95, "Capricórnio": 55, "Aquário": 75, "Peixes": 60},
        "Virgem":     {"Áries": 55, "Touro": 90, "Gêmeos": 65, "Câncer": 80, "Leão": 50, "Virgem": 75, "Libra": 70, "Escorpião": 85, "Sagitário": 55, "Capricórnio": 95, "Aquário": 60, "Peixes": 70},
        "Libra":      {"Áries": 75, "Touro": 70, "Gêmeos": 95, "Câncer": 55, "Leão": 80, "Virgem": 70, "Libra": 70, "Escorpião": 60, "Sagitário": 85, "Capricórnio": 55, "Aquário": 90, "Peixes": 65},
        "Escorpião":  {"Áries": 60, "Touro": 80, "Gêmeos": 50, "Câncer": 95, "Leão": 65, "Virgem": 85, "Libra": 60, "Escorpião": 75, "Sagitário": 55, "Capricórnio": 80, "Aquário": 50, "Peixes": 95},
        "Sagitário":  {"Áries": 95, "Touro": 45, "Gêmeos": 80, "Câncer": 50, "Leão": 95, "Virgem": 55, "Libra": 85, "Escorpião": 55, "Sagitário": 70, "Capricórnio": 50, "Aquário": 90, "Peixes": 60},
        "Capricórnio":{"Áries": 50, "Touro": 95, "Gêmeos": 45, "Câncer": 75, "Leão": 55, "Virgem": 95, "Libra": 55, "Escorpião": 80, "Sagitário": 50, "Capricórnio": 75, "Aquário": 60, "Peixes": 70},
        "Aquário":    {"Áries": 85, "Touro": 50, "Gêmeos": 90, "Câncer": 45, "Leão": 75, "Virgem": 60, "Libra": 90, "Escorpião": 50, "Sagitário": 90, "Capricórnio": 60, "Aquário": 70, "Peixes": 65},
        "Peixes":     {"Áries": 55, "Touro": 85, "Gêmeos": 60, "Câncer": 90, "Leão": 60, "Virgem": 70, "Libra": 65, "Escorpião": 95, "Sagitário": 60, "Capricórnio": 70, "Aquário": 65, "Peixes": 75},
    }

    return matriz.get(signo1, {}).get(signo2, 50)

def mensagem_compatibilidade(porcentagem: int) -> str:
    if porcentagem >= 90:
        return "Combinação excelente! Vocês têm uma química muito forte e grandes chances de dar muito certo."
    elif porcentagem >= 75:
        return "Ótima compatibilidade! Existe uma boa harmonia entre vocês e potencial para um relacionamento sólido."
    elif porcentagem >= 60:
        return "Compatibilidade boa. Com diálogo e compreensão, o relacionamento pode funcionar bem."
    elif porcentagem >= 45:
        return "Compatibilidade mediana. Vai exigir mais esforço e paciência de ambos os lados."
    else:
        return "Compatibilidade desafiadora. As diferenças são grandes, mas o amor pode superar se houver muito entendimento."

# ============================================================
# TEMPLATES
# ============================================================

BASE_CSS = """
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    min-height: 100vh;
    color: #e0e0e0;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 40px 20px;
}
.container {
    max-width: 720px;
    width: 100%;
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 40px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.1);
}
h1 {
    text-align: center;
    margin-bottom: 8px;
    font-size: 2.1rem;
    background: linear-gradient(90deg, #e94560, #ff6b6b);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.subtitle {
    text-align: center;
    color: #aaa;
    margin-bottom: 28px;
    font-size: 0.95rem;
}
form { display: flex; flex-direction: column; gap: 18px; }
.form-row { display: flex; gap: 14px; }
.form-group { flex: 1; display: flex; flex-direction: column; gap: 7px; }
label { font-weight: 600; color: #ccc; font-size: 0.9rem; }
select, input {
    padding: 12px 14px;
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.15);
    background: rgba(0, 0, 0, 0.3);
    color: #fff;
    font-size: 1rem;
    outline: none;
}
select:focus, input:focus { border-color: #e94560; }
button {
    padding: 14px;
    border: none;
    border-radius: 10px;
    background: linear-gradient(90deg, #e94560, #ff6b6b);
    color: white;
    font-size: 1.05rem;
    font-weight: 600;
    cursor: pointer;
    transition: transform 0.2s, box-shadow 0.2s;
}
button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 20px rgba(233, 69, 96, 0.4);
}
.erro {
    background: rgba(233, 69, 96, 0.2);
    border: 1px solid #e94560;
    color: #ff8a9a;
    padding: 12px;
    border-radius: 10px;
    text-align: center;
    margin-bottom: 18px;
}
.resultado { text-align: center; }
.simbolo { font-size: 4.5rem; margin: 15px 0 5px; }
.nome-signo { font-size: 2.3rem; color: #ff6b6b; margin-bottom: 5px; }
.nome-pessoa { font-size: 1.15rem; color: #ccc; margin-bottom: 20px; }
.info-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin: 22px 0;
    text-align: left;
}
.info-item {
    background: rgba(0, 0, 0, 0.25);
    padding: 14px;
    border-radius: 12px;
}
.info-item strong {
    display: block;
    color: #e94560;
    margin-bottom: 4px;
    font-size: 0.85rem;
}
.bloco {
    background: rgba(0, 0, 0, 0.25);
    padding: 18px;
    border-radius: 12px;
    line-height: 1.6;
    margin-top: 16px;
    text-align: left;
}
.bloco strong {
    color: #e94560;
    display: block;
    margin-bottom: 8px;
}
.links { margin-top: 28px; text-align: center; }
.links a {
    color: #ff6b6b;
    text-decoration: none;
    margin: 0 12px;
    font-weight: 500;
}
.links a:hover { text-decoration: underline; }

/* Compatibilidade */
.compat-box {
    margin-top: 30px;
    padding: 22px;
    background: rgba(233, 69, 96, 0.12);
    border: 1px solid rgba(233, 69, 96, 0.35);
    border-radius: 14px;
    text-align: center;
}
.compat-porcentagem {
    font-size: 3.2rem;
    font-weight: 700;
    color: #ff6b6b;
    margin: 10px 0;
}
.compat-msg {
    color: #ddd;
    line-height: 1.5;
    margin-top: 8px;
}
.crush-form {
    margin-top: 25px;
    padding-top: 20px;
    border-top: 1px solid rgba(255,255,255,0.1);
}
.crush-form h3 {
    text-align: center;
    color: #ff6b6b;
    margin-bottom: 18px;
}
"""

TEMPLATE_INDEX = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Descubra seu Signo</title>
    <style>{{ css }}</style>
</head>
<body>
    <div class="container">
        <h1>✨ Descubra seu Signo</h1>
        <p class="subtitle">Digite seu nome e data de nascimento</p>

        {% if erro %}
            <div class="erro">{{ erro }}</div>
        {% endif %}

        <form action="/descobrir" method="POST">
            <div class="form-group">
                <label for="nome">Seu nome</label>
                <input type="text" name="nome" id="nome" placeholder="Ex: Ana" required>
            </div>

            <div class="form-row">
                <div class="form-group">
                    <label for="dia">Dia</label>
                    <select name="dia" id="dia" required>
                        <option value="">Selecione</option>
                        {% for d in range(1, 32) %}
                            <option value="{{ d }}">{{ d }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="form-group">
                    <label for="mes">Mês</label>
                    <select name="mes" id="mes" required>
                        <option value="">Selecione</option>
                        <option value="1">Janeiro</option>
                        <option value="2">Fevereiro</option>
                        <option value="3">Março</option>
                        <option value="4">Abril</option>
                        <option value="5">Maio</option>
                        <option value="6">Junho</option>
                        <option value="7">Julho</option>
                        <option value="8">Agosto</option>
                        <option value="9">Setembro</option>
                        <option value="10">Outubro</option>
                        <option value="11">Novembro</option>
                        <option value="12">Dezembro</option>
                    </select>
                </div>
            </div>
            <button type="submit">Descobrir meu Signo</button>
        </form>
    </div>
</body>
</html>
"""

TEMPLATE_RESULTADO = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ nome }} - {{ signo.nome }}</title>
    <style>{{ css }}</style>
</head>
<body>
    <div class="container">
        <div class="resultado">
            <h1>Olá, {{ nome }}!</h1>
            <div class="simbolo">{{ signo.simbolo }}</div>
            <div class="nome-signo">{{ signo.nome }}</div>
            <p class="nome-pessoa">Nascido(a) em {{ "%02d"|format(dia) }}/{{ "%02d"|format(mes) }}</p>

            <div class="info-grid">
                <div class="info-item">
                    <strong>Elemento</strong>
                    {{ signo.elemento }}
                </div>
                <div class="info-item">
                    <strong>Qualidade</strong>
                    {{ signo.qualidade }}
                </div>
                <div class="info-item">
                    <strong>Planeta Regente</strong>
                    {{ signo.planeta }}
                </div>
                <div class="info-item">
                    <strong>Período</strong>
                    {{ signo.data_inicio }} a {{ signo.data_fim }}
                </div>
            </div>

            <div class="bloco">
                <strong>O que o signo significa</strong>
                {{ signo.significado }}
            </div>

            <div class="bloco">
                <strong>O que essa data e signo atraem para você</strong>
                {{ signo.atrai }}
            </div>

            <!-- Formulário do Crush -->
            <div class="crush-form">
                <h3>💘 Compatibilidade com o Crush</h3>
                <form action="/compatibilidade" method="POST">
                    <input type="hidden" name="nome" value="{{ nome }}">
                    <input type="hidden" name="dia" value="{{ dia }}">
                    <input type="hidden" name="mes" value="{{ mes }}">
                    <input type="hidden" name="signo_pessoa" value="{{ signo.nome }}">

                    <div class="form-group">
                        <label for="nome_crush">Nome do crush</label>
                        <input type="text" name="nome_crush" id="nome_crush" placeholder="Ex: João" required>
                    </div>

                    <div class="form-row">
                        <div class="form-group">
                            <label for="dia_crush">Dia de nascimento</label>
                            <select name="dia_crush" id="dia_crush" required>
                                <option value="">Selecione</option>
                                {% for d in range(1, 32) %}
                                    <option value="{{ d }}">{{ d }}</option>
                                {% endfor %}
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="mes_crush">Mês de nascimento</label>
                            <select name="mes_crush" id="mes_crush" required>
                                <option value="">Selecione</option>
                                <option value="1">Janeiro</option>
                                <option value="2">Fevereiro</option>
                                <option value="3">Março</option>
                                <option value="4">Abril</option>
                                <option value="5">Maio</option>
                                <option value="6">Junho</option>
                                <option value="7">Julho</option>
                                <option value="8">Agosto</option>
                                <option value="9">Setembro</option>
                                <option value="10">Outubro</option>
                                <option value="11">Novembro</option>
                                <option value="12">Dezembro</option>
                            </select>
                        </div>
                    </div>
                    <button type="submit">Calcular Compatibilidade</button>
                </form>
            </div>

            <div class="links">
                <a href="/">← Descobrir outro signo</a>
            </div>
        </div>
    </div>
</body>
</html>
"""

TEMPLATE_COMPAT = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Compatibilidade - {{ nome }} & {{ nome_crush }}</title>
    <style>{{ css }}</style>
</head>
<body>
    <div class="container">
        <div class="resultado">
            <h1>💘 Compatibilidade</h1>
            <p class="nome-pessoa" style="margin-top:10px;">
                {{ nome }} ({{ signo_pessoa }})  +  {{ nome_crush }} ({{ signo_crush }})
            </p>

            <div class="compat-box">
                <div style="font-size:0.95rem; color:#ccc;">Chance de dar certo</div>
                <div class="compat-porcentagem">{{ porcentagem }}%</div>
                <div class="compat-msg">{{ mensagem }}</div>
            </div>

            <div class="bloco" style="margin-top:25px;">
                <strong>Resumo dos signos</strong>
                <p><b>{{ nome }}</b> → {{ signo_pessoa }} ({{ elemento1 }})</p>
                <p style="margin-top:6px;"><b>{{ nome_crush }}</b> → {{ signo_crush }} ({{ elemento2 }})</p>
            </div>

            <div class="links">
                <a href="/">← Começar de novo</a>
            </div>
        </div>
    </div>
</body>
</html>
"""

# ============================================================
# ROTAS
# ============================================================

@app.route("/")
def index():
    return render_template_string(TEMPLATE_INDEX, css=BASE_CSS, erro=None)

@app.route("/descobrir", methods=["POST"])
def descobrir():
    try:
        nome = request.form.get("nome", "").strip()
        dia = int(request.form.get("dia"))
        mes = int(request.form.get("mes"))

        if not nome:
            return render_template_string(TEMPLATE_INDEX, css=BASE_CSS, erro="Digite seu nome.")

        if not (1 <= dia <= 31) or not (1 <= mes <= 12):
            return render_template_string(TEMPLATE_INDEX, css=BASE_CSS, erro="Data inválida.")

        signo = encontrar_signo(dia, mes)
        if not signo:
            return render_template_string(TEMPLATE_INDEX, css=BASE_CSS, erro="Não foi possível encontrar o signo.")

        return render_template_string(
            TEMPLATE_RESULTADO,
            css=BASE_CSS,
            nome=nome,
            signo=signo,
            dia=dia,
            mes=mes
        )

    except (ValueError, TypeError):
        return render_template_string(TEMPLATE_INDEX, css=BASE_CSS, erro="Preencha todos os campos corretamente.")

@app.route("/compatibilidade", methods=["POST"])
def compatibilidade():
    try:
        nome = request.form.get("nome", "").strip()
        signo_pessoa = request.form.get("signo_pessoa")
        nome_crush = request.form.get("nome_crush", "").strip()
        dia_crush = int(request.form.get("dia_crush"))
        mes_crush = int(request.form.get("mes_crush"))

        if not nome_crush:
            return render_template_string(TEMPLATE_INDEX, css=BASE_CSS, erro="Digite o nome do crush.")

        signo_crush_obj = encontrar_signo(dia_crush, mes_crush)
        if not signo_crush_obj:
            return render_template_string(TEMPLATE_INDEX, css=BASE_CSS, erro="Data do crush inválida.")

        signo_crush = signo_crush_obj["nome"]
        porcentagem = calcular_compatibilidade(signo_pessoa, signo_crush)
        mensagem = mensagem_compatibilidade(porcentagem)

        return render_template_string(
            TEMPLATE_COMPAT,
            css=BASE_CSS,
            nome=nome,
            nome_crush=nome_crush,
            signo_pessoa=signo_pessoa,
            signo_crush=signo_crush,
            elemento1=encontrar_signo(
                int(request.form.get("dia")),
                int(request.form.get("mes"))
            )["elemento"],
            elemento2=signo_crush_obj["elemento"],
            porcentagem=porcentagem,
            mensagem=mensagem
        )

    except (ValueError, TypeError):
        return render_template_string(TEMPLATE_INDEX, css=BASE_CSS, erro="Erro ao calcular compatibilidade.")

# ============================================================
# INICIALIZAÇÃO
# ============================================================

if __name__ == "__main__":
    init_db()
    print("Banco criado com sucesso!")
    print("Acesse: http://127.0.0.1:5000")
    app.run(debug=True, port=5000)