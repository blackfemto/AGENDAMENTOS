from flask import Flask, request, jsonify, render_template_string
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    # HTML do formulário dentro do Flask
    html = '''
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Agendamento de Eventos</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #001530;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .container {
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.2);
                width: 350px;
            }
            h2 {
                text-align: center;
                color: #333;
            }
            label {
                font-weight: bold;
                display: block;
                margin-top: 10px;
                color: #555;
            }
            input, select, textarea {
                width: 100%;
                padding: 10px;
                margin-top: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
                font-size: 14px;
            }
            button {
                width: 100%;
                padding: 12px;
                background: #007bff;
                color: white;
                border: none;
                border-radius: 5px;
                margin-top: 15px;
                cursor: pointer;
                font-size: 16px;
            }
            button:hover {
                background: #0056b3;
            }
            .error {
                color: red;
                font-size: 12px;
                display: none;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Agende seu Evento</h2>
            <form id="form-agendamento" method="POST" action="/agendar">
                <label for="nome">Nome do Responsável:</label>
                <input type="text" id="nome" name="nome" required>
                <span class="error" id="erro-nome">Por favor, insira seu nome.</span>

                <label for="telefone">Telefone do Responsável:</label>
                <input type="tel" id="telefone" name="telefone" required>
                <span class="error" id="erro-telefone">Por favor, insira um telefone válido.</span>

                <label for="evento">Tipo de Evento:</label>
                <select id="evento" name="evento" required>
                    <option value="">Selecione</option>
                    <option value="Casamento">Casamento</option>
                    <option value="Aniversário">Aniversário</option>
                    <option value="Reunião Corporativa">Reunião Corporativa</option>
                    <option value="Outro">Outro</option>
                </select>

                <label for="data">Data do Evento:</label>
                <input type="date" id="data" name="data" required>

                <label for="horario">Horário do Evento:</label>
                <input type="time" id="horario" name="horario" required>

                <label for="convidados">Número de Convidados:</label>
                <input type="number" id="convidados" name="convidados" min="1" required>

                <button type="submit">Enviar Pedido</button>
            </form>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html)

@app.route('/agendar', methods=['POST'])
def agendar():
    dados = request.form  # Recebe os dados do formulário HTML

    # Conecta ao banco e insere os dados
    conn = sqlite3.connect("idpb.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO agendamentos (nome, telefone, evento, data, horario, convidados)
        VALUES (?,?,?,?,?,?)
    """, (dados['nome'], dados['telefone'], dados['evento'], dados['data'], dados['horario'], dados['convidados']))

    conn.commit()
    conn.close()

    return jsonify({"mensagem": "Agendamento realizado com sucesso!"})

@app.route('/listar', methods=['GET'])
def listar_agendamentos():
    # Conecta ao banco e recupera os agendamentos
    conn = sqlite3.connect("idpb.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nome, telefone, evento, data, horario, convidados FROM agendamentos")
    agendamentos = cursor.fetchall()
    conn.close()

    # Converte os dados para um formato adequado
    lista_agendamentos = [
        {"nome": agendamento[0], "telefone": agendamento[1], "evento": agendamento[2], 
         "data": agendamento[3], "horario": agendamento[4], "convidados": agendamento[5]}
        for agendamento in agendamentos
    ]

    # Exibe a lista no navegador
    html = '<h2>Lista de Agendamentos</h2><ul>'
    for agendamento in lista_agendamentos:
        html += f'<li><strong>Nome:</strong> {agendamento["nome"]} - <strong>Evento:</strong> {agendamento["evento"]} - <strong>Data:</strong> {agendamento["data"]} - <strong>Convidados:</strong> {agendamento["convidados"]}</li>'
    html += '</ul>'

    return render_template_string(html)

if __name__ == '__main__':
    app.run(debug=True)
