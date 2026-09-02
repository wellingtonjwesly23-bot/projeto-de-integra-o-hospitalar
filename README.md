## 📸 Demonstração Visual e Fluxo de Integração (Swagger UI)

A API foi desenvolvida com documentação interativa automática, facilitando o teste e a homologação por parte das equipas de infraestrutura e desenvolvimento do hospital. Abaixo estão os testes reais de integração:

### 1. Health Check do Sistema (Rota Inicial)
O sistema possui uma rota de verificação de disponibilidade, garantindo que o servidor Uvicorn e a API estão online e prontos para receber requisições dos sistemas satélites.

<img width="766" height="580" alt="image" src="https://github.com/user-attachments/assets/204c3b76-10c6-4a1a-929e-286aa5909c95" />


### 2. Pipe de Integração: Inserção de Check-list de Equipamento
Esta é a rota principal de integração (`POST /integracao/checklist`). O sistema recebe um ficheiro JSON com os dados do equipamento e o seu estado. 
**Diferencial de Segurança:** Antes de inserir no banco de dados, a API faz uma validação de integridade. Se o `equipamento_id` não estiver cadastrado no ERP (simulado pela tabela de equipamentos), a requisição é negada. Na imagem abaixo, vemos a integração a ocorrer com sucesso (Código 200) para um equipamento válido.

<img width="780" height="672" alt="image" src="https://github.com/user-attachments/assets/db21a626-abfa-454b-871e-ae42f73ace3e" />


### 3. Extração de Dados para Analytics e Relatórios
Para atender à necessidade de exportação de dados para ferramentas de tomada de decisão (como Analytics GoodData ou Grafana), foi desenvolvida a rota `GET /integracao/relatorio`. Esta rota faz um `JOIN` nas tabelas relacionais e devolve um JSON estruturado com o histórico de manutenções e o estado dos equipamentos de cada setor.

<img width="776" height="718" alt="image" src="https://github.com/user-attachments/assets/b6941350-8fc0-4ee6-aa32-c94f27bce70b" />
