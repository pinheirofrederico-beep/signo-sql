from flask import Flask, request, render_template_string
import sqlite3
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

app = Flask(__name__)
DB_PATH = Path(__file__).parent / "signos.db"
TZ_BRASILIA = ZoneInfo("America/Sao_Paulo")

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

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_pessoa TEXT NOT NULL,
            dia_pessoa INTEGER NOT NULL,
            mes_pessoa INTEGER NOT NULL,
            signo_pessoa TEXT NOT NULL,
            nome_crush TEXT NOT NULL,
            dia_crush INTEGER NOT NULL,
            mes_crush INTEGER NOT NULL,
            signo_crush TEXT NOT NULL,
            porcentagem INTEGER NOT NULL,
            data_consulta TEXT NOT NULL
        )
    """)

    cursor.execute("DELETE FROM signos")

    signos = [
        ("Áries", "♈", "21/03", "19/04", "Fogo", "Cardinal", "Marte",
         "Áries representa a iniciativa, a coragem e o impulso de começar. É o primeiro signo do zodíaco e simboliza o pioneirismo e a força de vontade.",
         "Atrai pessoas dinâmicas, aventureiras e que não tenham medo de desafios. Costuma se interessar por quem tem energia e atitude."),
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

def salvar_registro(nome_pessoa, dia_pessoa, mes_pessoa, signo_pessoa,
                    nome_crush, dia_crush, mes_crush, signo_crush, porcentagem):
    conn = get_connection()
    cursor = conn.cursor()

    # Hora real de Brasília
    agora = datetime.now(TZ_BRASILIA).strftime("%d/%m/%Y %H:%M:%S")

    cursor.execute("""
        INSERT INTO registros 
        (nome_pessoa, dia_pessoa, mes_pessoa, signo_pessoa,
         nome_crush, dia_crush, mes_crush, signo_crush, porcentagem, data_consulta)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (nome_pessoa, dia_pessoa, mes_pessoa, signo_pessoa,
          nome_crush, dia_crush, mes_crush, signo_crush, porcentagem, agora))

    conn.commit()
    conn.close()

def listar_registros():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM registros ORDER BY id DESC")
    dados = cursor.fetchall()
    conn.close()
    return dados

# ============================================================
# LÓGICA
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
# CSS MELHORADO
# ============================================================

BASE_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
    font-family: 'Poppins', sans-serif;
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    min-height: 100vh;
    color: #e8e8e8;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 30px 16px;
}

.container {
    max-width: 680px;
    width: 100%;
    background: rgba(255, 255, 255, 0.04);
    backdrop-filter: blur(16px);
    border-radius: 24px;
    padding: 36px 32px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.08);
}

h1 {
    text-align: center;
    margin-bottom: 6px;
    font-size: 1.9rem;
    font-weight: 700;
    background: linear-gradient(90deg, #ff6b6b, #ee5a24, #ff9ff3);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    text-align: center;
    color: #a0a0b0;
    margin-bottom: 28px;
    font-size: 0.92rem;
    font-weight: 300;
}

form { display: flex; flex-direction: column; gap: 16px; }
.form-row { display: flex; gap: 12px; }
.form-group { flex: 1; display: flex; flex-direction: column; gap: 6px; }

label {
    font-weight: 500;
    color: #c0c0d0;
    font-size: 0.85rem;
}

select, input {
    padding: 13px 14px;
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.12);
    background: rgba(0, 0, 0, 0.25);
    color: #fff;
    font-size: 0.95rem;
    font-family: 'Poppins', sans-serif;
    outline: none;
    transition: border-color 0.25s, box-shadow 0.25s;
}

select:focus, input:focus {
    border-color: #ff6b6b;
    box-shadow: 0 0 0 3px rgba(255, 107, 107, 0.15);
}

button {
    padding: 14px;
    border: none;
    border-radius: 12px;
    background: linear-gradient(90deg, #ff6b6b, #ee5a24);
    color: white;
    font-size: 1rem;
    font-weight: 600;
    font-family: 'Poppins', sans-serif;
    cursor: pointer;
    transition: transform 0.2s, box-shadow 0.2s;
    margin-top: 6px;
}

button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(255, 107, 107, 0.35);
}

.erro {
    background: rgba(255, 107, 107, 0.15);
    border: 1px solid #ff6b6b;
    color: #ffb3b3;
    padding: 12px 16px;
    border-radius: 12px;
    text-align: center;
    margin-bottom: 18px;
    font-size: 0.9rem;
}

.resultado { text-align: center; }

.simbolo {
    font-size: 4.8rem;
    margin: 12px 0 4px;
    filter: drop-shadow(0 0 12px rgba(255, 107, 107, 0.3));
}

.nome-signo {
    font-size: 2.1rem;
    font-weight: 700;
    color: #ff6b6b;
    margin-bottom: 4px;
}

.nome-pessoa {
    font-size: 1.05rem;
    color: #a0a0b0;
    margin-bottom: 22px;
    font-weight: 300;
}

.info-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin: 20px 0;
    text-align: left;
}

.info-item {
    background: rgba(255, 255, 255, 0.04);
    padding: 14px 16px;
    border-radius: 14px;
    border: 1px solid rgba(255, 255, 255, 0.06);
}

.info-item strong {
    display: block;
    color: #ff6b6b;
    margin-bottom: 3px;
    font-size: 0.78rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.4px;
}

.bloco {
    background: rgba(255, 255, 255, 0.04);
    padding: 18px 20px;
    border-radius: 14px;
    line-height: 1.65;
    margin-top: 14px;
    text-align: left;
    border: 1px solid rgba(255, 255, 255, 0.06);
    font-size: 0.93rem;
}

.bloco strong {
    color: #ff6b6b;
    display: block;
    margin-bottom: 8px;
    font-size: 0.88rem;
}

.links {
    margin-top: 28px;
    text-align: center;
    display: flex;
    justify-content: center;
    gap: 20px;
    flex-wrap: wrap;
}

.links a {
    color: #ff6b6b;
    text-decoration: none;
    font-weight: 500;
    font-size: 0.9rem;
    transition: opacity 0.2s;
}

.links a:hover { opacity: 0.75; }

.compat-box {
    margin-top: 28px;
    padding: 26px 20px;
    background: linear-gradient(135deg, rgba(255, 107, 107, 0.12), rgba(238, 90, 36, 0.08));
    border: 1px solid rgba(255, 107, 107, 0.3);
    border-radius: 18px;
    text-align: center;
}

.compat-porcentagem {
    font-size: 3.4rem;
    font-weight: 700;
    background: linear-gradient(90deg, #ff6b6b, #ee5a24);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 8px 0;
}

.compat-msg {
    color: #d0d0d8;
    line-height: 1.55;
    margin-top: 8px;
    font-size: 0.93rem;
}

.crush-form {
    margin-top: 28px;
    padding-top: 24px;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
}

.crush-form h3 {
    text-align: center;
    color: #ff6b6b;
    margin-bottom: 18px;
    font-size: 1.15rem;
    font-weight: 600;
}

.salvo {
    margin-top: 18px;
    color: #7dcea0;
    font-size: 0.88rem;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
}

/* Tabela histórico */
.tabela-wrap {
    overflow-x: auto;
    margin-top: 20px;
    border-radius: 14px;
    border: 1px solid rgba(255, 255, 255, 0.06);
}

.tabela {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.85rem;
}

.tabela th, .tabela td {
    padding: 12px 10px;
    text-align: left;
    white-space: nowrap;
}

.tabela th {
    background: rgba(255, 107, 107, 0.12);
    color: #ff6b6b;
    font-weight: 600;
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.3px;
}

.tabela tr:nth-child(even) {
    background: rgba(255, 255, 255, 0.02);
}

.tabela tr:hover {
    background: rgba(255, 255, 255, 0.04);
}

.tabela td strong {
    color: #ff6b6b;
}

.vazio {
    text-align: center;
    color: #888;
    margin-top: 36px;
    font-weight: 300;
}

@media (max-width: 520px) {
    .container { padding: 28px 18px; }
    .info-grid { grid-template-columns: 1fr; }
    .form-row { flex-direction: column; }
    h1 { font-size: 1.6rem; }
    .simbolo { font-size: 3.8rem; }
}
"""

# ============================================================
# TEMPLATES
# ============================================================

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

        <div class="links">
            <a href="/historico">📋 Ver histórico</a>
        </div>
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
    <title>{{ nome }} · {{ signo.nome }}</title>
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
                <div class="info-item"><strong>Elemento</strong>{{ signo.elemento }}</div>
                <div class="info-item"><strong>Qualidade</strong>{{ signo.qualidade }}</div>
                <div class="info-item"><strong>Planeta</strong>{{ signo.planeta }}</div>
                <div class="info-item"><strong>Período</strong>{{ signo.data_inicio }} – {{ signo.data_fim }}</div>
            </div>

            <div class="bloco">
                <strong>O que o signo significa</strong>
                {{ signo.significado }}
            </div>

            <div class="bloco">
                <strong>O que essa data e signo atraem</strong>
                {{ signo.atrai }}
            </div>

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
                            <label for="dia_crush">Dia</label>
                            <select name="dia_crush" id="dia_crush" required>
                                <option value="">Selecione</option>
                                {% for d in range(1, 32) %}
                                    <option value="{{ d }}">{{ d }}</option>
                                {% endfor %}
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="mes_crush">Mês</label>
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
                <a href="/">← Novo cálculo</a>
                <a href="/historico">📋 Histórico</a>
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
    <title>{{ nome }} & {{ nome_crush }}</title>
    <style>{{ css }}</style>
</head>
<body>
    <div class="container">
        <div class="resultado">
            <h1>💘 Compatibilidade</h1>
            <p class="nome-pessoa" style="margin-top:8px;">
                {{ nome }} ({{ signo_pessoa }})  +  {{ nome_crush }} ({{ signo_crush }})
            </p>

            <div class="compat-box">
                <div style="font-size:0.88rem; color:#a0a0b0;">Chance de dar certo</div>
                <div class="compat-porcentagem">{{ porcentagem }}%</div>
                <div class="compat-msg">{{ mensagem }}</div>
            </div>

            <div class="bloco" style="margin-top:22px;">
                <strong>Resumo dos signos</strong>
                <p><b>{{ nome }}</b> → {{ signo_pessoa }} ({{ elemento1 }})</p>
                <p style="margin-top:6px;"><b>{{ nome_crush }}</b> → {{ signo_crush }} ({{ elemento2 }})</p>
            </div>

            <p class="salvo">✅ Salvo no banco · Horário de Brasília</p>

            <div class="links">
                <a href="/">← Começar de novo</a>
                <a href="/historico">📋 Histórico</a>
            </div>
        </div>
    </div>
</body>
</html>
"""

TEMPLATE_HISTORICO = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Histórico</title>
    <style>{{ css }}</style>
</head>
<body>
    <div class="container">
        <h1>📋 Histórico</h1>
        <p class="subtitle">Consultas salvas com horário de Brasília</p>

        {% if registros %}
            <div class="tabela-wrap">
                <table class="tabela">
                    <thead>
                        <tr>
                            <th>Pessoa</th>
                            <th>Signo</th>
                            <th>Crush</th>
                            <th>Signo</th>
                            <th>%</th>
                            <th>Data/Hora</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for r in registros %}
                        <tr>
                            <td>{{ r.nome_pessoa }}</td>
                            <td>{{ r.signo_pessoa }}</td>
                            <td>{{ r.nome_crush }}</td>
                            <td>{{ r.signo_crush }}</td>
                            <td><strong>{{ r.porcentagem }}%</strong></td>
                            <td style="color:#999; font-size:0.8rem;">{{ r.data_consulta }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        {% else %}
            <p class="vazio">Nenhuma consulta salva ainda.</p>
        {% endif %}

        <div class="links">
            <a href="/">← Voltar ao início</a>
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

        return render_template_string(TEMPLATE_RESULTADO, css=BASE_CSS, nome=nome, signo=signo, dia=dia, mes=mes)

    except (ValueError, TypeError):
        return render_template_string(TEMPLATE_INDEX, css=BASE_CSS, erro="Preencha todos os campos corretamente.")

@app.route("/compatibilidade", methods=["POST"])
def compatibilidade():
    try:
        nome = request.form.get("nome", "").strip()
        dia = int(request.form.get("dia"))
        mes = int(request.form.get("mes"))
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

        # Salva com horário real de Brasília
        salvar_registro(
            nome_pessoa=nome,
            dia_pessoa=dia,
            mes_pessoa=mes,
            signo_pessoa=signo_pessoa,
            nome_crush=nome_crush,
            dia_crush=dia_crush,
            mes_crush=mes_crush,
            signo_crush=signo_crush,
            porcentagem=porcentagem
        )

        return render_template_string(
            TEMPLATE_COMPAT,
            css=BASE_CSS,
            nome=nome,
            nome_crush=nome_crush,
            signo_pessoa=signo_pessoa,
            signo_crush=signo_crush,
            elemento1=encontrar_signo(dia, mes)["elemento"],
            elemento2=signo_crush_obj["elemento"],
            porcentagem=porcentagem,
            mensagem=mensagem
        )

    except (ValueError, TypeError):
        return render_template_string(TEMPLATE_INDEX, css=BASE_CSS, erro="Erro ao calcular compatibilidade.")

@app.route("/historico")
def historico():
    registros = listar_registros()
    return render_template_string(TEMPLATE_HISTORICO, css=BASE_CSS, registros=registros)

# ============================================================
# INICIALIZAÇÃO
# ============================================================

if __name__ == "__main__":
    init_db()
    print("Banco criado com sucesso!")
    print("Horário usado: Brasília (America/Sao_Paulo)")
    print("Acesse: http://127.0.0.1:5000")
    app.run(debug=True, port=5000)