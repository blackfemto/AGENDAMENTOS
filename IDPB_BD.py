import sqlite3

# Conectar ao banco (cria um arquivo se não existir)
conn = sqlite3.connect("idpb.db")
cursor = conn.cursor()

# Criar tabela de agendamentos
cursor.execute("""
CREATE TABLE IF NOT EXISTS agendamentos 
(
    nome TEXT NOT NULL,
    telefone TEXT NOT NULL,
    evento TEXT NOT NULL,
    data TEXT NOT NULL,
    horario TEXT NOT NULL,
    convidados INTEGER NOT NULL
)
""")

conn.commit()
conn.close()

print("Banco de dados criado com sucesso!")
