import sqlite3

def inicializar_banco():
    # Conecta ao banco de dados (cria o arquivo hospital.db automaticamente)
    conexao = sqlite3.connect('hospital.db')
    cursor = conexao.cursor()

    print("Criando tabelas no padrão Protheus...")

    # 1. Tabela de Setores (ZST)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ZST_Setores (
            ZST_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            ZST_NOME TEXT NOT NULL,
            ZST_LOCAL TEXT
        )
    ''')

    # 2. Tabela de Equipamentos (ZEQ)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ZEQ_Equipamentos (
            ZEQ_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            ZEQ_NOME TEXT NOT NULL,
            ZEQ_STATUS TEXT DEFAULT 'ATIVO',
            ZEQ_SETOR_ID INTEGER,
            FOREIGN KEY (ZEQ_SETOR_ID) REFERENCES ZST_Setores(ZST_ID)
        )
    ''')

    # 3. Tabela de Check-lists (ZCK)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ZCK_Checklist (
            ZCK_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            ZCK_DATA DATETIME DEFAULT CURRENT_TIMESTAMP,
            ZCK_STATUS TEXT NOT NULL,
            ZCK_OBSERVACAO TEXT,
            ZCK_EQUIP_ID INTEGER,
            FOREIGN KEY (ZCK_EQUIP_ID) REFERENCES ZEQ_Equipamentos(ZEQ_ID)
        )
    ''')
    
    # --- INSERÇÃO DE DADOS DE TESTE ---
    # Limpa dados antigos de teste para não duplicar toda vez que rodar
    cursor.execute("DELETE FROM ZST_Setores WHERE ZST_ID = 1")
    cursor.execute("DELETE FROM ZEQ_Equipamentos WHERE ZEQ_ID = 1")

    # Insere o Centro Rebouças (Exemplo)
    cursor.execute('''
        INSERT INTO ZST_Setores (ZST_ID, ZST_NOME, ZST_LOCAL) 
        VALUES (1, 'Centro de Convenções Rebouças', 'Pavilhão Principal')
    ''')

    # Insere um equipamento atrelado ao Centro Rebouças
    cursor.execute('''
        INSERT INTO ZEQ_Equipamentos (ZEQ_ID, ZEQ_NOME, ZEQ_SETOR_ID) 
        VALUES (1, 'Ar-Condicionado Central Model X', 1)
    ''')

    conexao.commit()
    conexao.close()
    print("✅ Banco hospital.db pronto e povoado com dados de teste!")

if __name__ == "__main__":
    inicializar_banco()
