from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Função para inicializar o banco de dados e a tabela
def init_db():
    conn = sqlite3.connect("idpb.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agendamentos 
        (
            nome TEXT,
            telefone TEXT,
            evento TEXT,
            data TEXT,
            horario TEXT,
            convidados INTEGER
        )
    """)
    conn.commit()
    conn.close()

# Rota para receber dados do formulário e salvar no banco
@app.route('/agendar', methods=['GET', 'POST'])
def agendar():
    if request.method == 'POST':
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

    elif request.method == 'GET':
        # Lógica para listar agendamentos
        conn = sqlite3.connect("idpb.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM agendamentos")
        agendamentos = cursor.fetchall()
        conn.close()

        return jsonify(agendamentos)

if __name__ == '__main__':
    #init_db()  # Chama a função para inicializar o banco e a tabela
    app.run(host="0.0.0.0",port=10000,debug=True)