import sqlite3
# Conectar ao banco de dados
conn = sqlite3.connect("idpb.db")
cursor = conn.cursor()

# Verificar a estrutura da tabela
cursor.execute("PRAGMA table_info(agendamentos);")
tabela_info = cursor.fetchall()

# Mostrar a estrutura da tabela
for coluna in tabela_info:
    print(coluna)
    
conn.close()
