from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI(title="API de Integração Hospitalar - HC")

# Modelo de dados que a API espera receber (JSON)
class ChecklistInput(BaseModel):
    equipamento_id: int
    status: str  # Ex: 'OK' ou 'FALHA'
    observacao: str

# Rota inicial
@app.get("/")
def home():
    return {"mensagem": "Sistema de Integração Hospitalar Ativo"}

# Rota para Criar um Check-list (O "Pipe" de integração)
@app.post("/integracao/checklist")
def criar_checklist(dados: ChecklistInput):
    conexao = sqlite3.connect('hospital.db')
    cursor = conexao.cursor()

    # 1. Validação: O equipamento existe no banco? (Integridade Referencial)
    cursor.execute("SELECT ZEQ_ID FROM ZEQ_Equipamentos WHERE ZEQ_ID = ?", (dados.equipamento_id,))
    equipamento = cursor.fetchone()

    if not equipamento:
        conexao.close()
        raise HTTPException(status_code=404, detail="Erro: Equipamento não encontrado no ERP Protheus.")

    # 2. Inserção: Salva o check-list no banco
    try:
        cursor.execute('''
            INSERT INTO ZCK_Checklist (ZCK_STATUS, ZCK_OBSERVACAO, ZCK_EQUIP_ID)
            VALUES (?, ?, ?)
        ''', (dados.status.upper(), dados.observacao, dados.equipamento_id))
        
        conexao.commit()
        return {"status": "Sucesso", "mensagem": "Dados integrados ao ERP com sucesso!"}
    
    except Exception as e:
        return {"status": "Erro", "mensagem": str(e)}
    
    finally:
        conexao.close()

# Rota para listar todos os check-lists (Simulando consulta para Relatórios/GoodData)
@app.get("/integracao/relatorio")
def gerar_relatorio():
    conexao = sqlite3.connect('hospital.db')
    cursor = conexao.cursor()
    
    cursor.execute('''
        SELECT C.ZCK_ID, E.ZEQ_NOME, C.ZCK_STATUS, C.ZCK_DATA 
        FROM ZCK_Checklist C
        JOIN ZEQ_Equipamentos E ON C.ZCK_EQUIP_ID = E.ZEQ_ID
    ''')
    
    resultados = cursor.fetchall()
    conexao.close()
    return {"checklists": resultados}
