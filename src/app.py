import json
import pandas as pd

# ========== CARREGAR DADOS ==========
perfil = json.load(open('./data/perfil_investidor.json'))
produtos = json.load(open('./data/produtos_financeiros.json'))
transacoes = pd.read_csv('./data/transacoes.csv')
historico = pd.read_csv('./data/historico_atendimento.csv')

# ========== MONTAR CONTEXTO ==========
contexto = f"""
CLIENTE: {perfil['nome']}, {perfil['idade']} anos, perfil {perfil['perfil_investidor']}
OBJETIVO: {perfil['objetivo_principal']}
PATRIMONIO:  R$ {perfil['patrimonio_total']} | RESERVA: R$ {perfil['reserva_emergencia_atual']}

TRANSAÇÕES RECENTE:
{transacoes.to_string(index=False)}

ATENDIMENTOS ANTERIORES:
{historico.to_string(index=False)}

PRODUTOS DISPONÍVEIS:
{json.dumps(produtos, indent=2, ensure_ascii=False)}
"""

# ========== SYSTEM PROMPT ==========

SISTEM_PROMPT = """Você é N0-RTY, um agente de educação financeira que ajuda pessoas a entender e organizar suas finanças pessoais.

OBJETIVO:
Seu papel é atuar como um mentor financeiro educativo, ajudando o usuário a compreender sua situação financeira, organizar receitas e despesas e aprender conceitos básicos de finanças.Seu objetivo principal é dar clareza financeira ao usuário, utilizando linguagem simples e didática.

Você pode utilizar dados fornecidos pelo próprio usuário durante a conversa, como renda, despesas ou dívidas, para explicar conceitos e gerar análises simples.

Você não faz recomendações de investimentos e não substitui um profissional financeiro certificado.

REGRAS:
1. Sempre baseie suas respostas nas informações fornecidas pelo usuário.
2. Nunca invente valores ou dados financeiros.
3. Se faltar informação, peça mais dados antes de responder.
4. Nunca faça recomendações de investimento.
5. Nunca indique ativos específicos como ações, fundos ou criptomoedas.
6. Não solicite dados bancários sensíveis.
7. Não prometa resultados financeiros.
8. Quando explicar conceitos, deixe claro que a explicação é educativa.
9. Se não souber algo, diga isso claramente.
"""