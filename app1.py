from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# Função para inicializar o banco de dados e a tabela
def init_db():
    db_path = "idpb.db"
    
    # Verifique se o banco de dados existe, caso contrário, crie
    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
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
        print("Banco de dados e tabela criados com sucesso!")

# Rota principal
@app.route('/')
def index():
    return "Bem-vindo ao sistema de agendamento de eventos!"

# Rota para receber dados do formulário e salvar no banco
@app.route('/agendar', methods=['GET', 'POST'])
def agendar():
    if request.method == 'POST':
        dados = request.form  # Recebe os dados do formulário HTML
        
        # Verifique se os dados estão sendo recebidos corretamente
        print(f"Dados recebidos: {dados}")

        try:
            # Conecta ao banco e insere os dados
            conn = sqlite3.connect("idpb.db")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO agendamentos (nome, telefone, evento, data, horario, convidados)
                VALUES (?,?,?,?,?,?)
            """, (dados['nome'], dados['telefone'], dados['evento'], dados['data'], dados['horario'], dados['convidados']))

            conn.commit()
            conn.close()
            
            # Retorna sucesso
            return jsonify({"mensagem": "Agendamento realizado com sucesso!"})
        except Exception as e:
            # Caso algum erro ocorra durante a inserção no banco
            return jsonify({"erro": f"Erro ao realizar agendamento: {str(e)}"}), 500

    elif request.method == 'GET':
        # Lógica para listar agendamentos
        try:
            conn = sqlite3.connect("idpb.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM agendamentos")
            agendamentos = cursor.fetchall()
            conn.close()
            
            # Retorna os agendamentos como uma resposta JSON
            return jsonify(agendamentos)
        except Exception as e:
            return jsonify({"erro": f"Erro ao recuperar agendamentos: {str(e)}"}), 500

if __name__ == '__main__':
    init_db()  # Chama a função para inicializar o banco e a tabela
    app.run(host="0.0.0.0", port=10000, debug=True)
