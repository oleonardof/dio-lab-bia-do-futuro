# Base de Conhecimento

## Dados Utilizados


| Arquivo | Formato | Utilização no Agente |
|---------|---------|---------------------|
| `historico_atendimento.csv` | CSV | Contextualizar interações anteriores |
| `perfil_investidor.json` | JSON | Personalizar recomendações |
| `produtos_financeiros.json` | JSON | Sugerir produtos adequados ao perfil |
| `transacoes.csv` | CSV | Analisar padrão de gastos do cliente |

> [!TIP]
> **Quer um dataset mais robusto?** Você pode utilizar datasets públicos do [Hugging Face](https://huggingface.co/datasets) relacionados a finanças, desde que sejam adequados ao contexto do desafio.

---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

Em cada arquivo fui além do exemplo original para deixar os dados mais ricos para o agente. Aqui está um resumo do que foi adaptado:

- Transações: O exemplo original tinha só 5 linhas com categorias básicas. Expandi para 110 registros cobrindo 8 categorias (alimentação, moradia, saúde, lazer, transporte, educação, receita e outros), com valores realistas por tipo de despesa e um período de 14 meses (jan/2024 a fev/2025).
- Histórico de Atendimento: O original tinha 5 registros com 3 canais e temas genéricos. Expandi para 55 registros com 5 canais (chat, telefone, email, app, WhatsApp), 25 temas distintos e resumos contextualizados por tema — por exemplo, atendimentos sobre CDB têm resumos diferentes dos sobre PIX ou IR. Também incluí casos não resolvidos (12% dos atendimentos) para dar realismo.
- Perfis de Investidor: O exemplo tinha apenas os campos básicos. Mantive a estrutura, mas gerei 55 perfis com coerência interna — renda compatível com a profissão, reserva de emergência proporcional ao patrimônio, perfil de risco correlacionado com idade e renda, e metas financeiras com valores e prazos plausíveis para cada objetivo.
- Produtos Financeiros: O exemplo tinha 5 campos. Adicionei 3 campos novos em todos os 25 produtos: liquidez (ex: D+0, D+2, no vencimento), prazo_recomendado (curto, médio, longo prazo) e imposto_renda (booleano). Esses campos são especialmente úteis para que o agente filtre produtos adequados ao perfil e ao objetivo do usuário.


---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.

Existem duas possibilidades. Injetar os dados direo no prompt (CTRL + C, CTRL + V) ou carregar os arquivos via código, como no exemplo abaixo.

```python
import pandas as pd
import json

# JSONs
produtos = json.load(open("produtos_financeiros.json", encoding="utf-8"))
perfis = json.load(open("perfis_investidores.json", encoding="utf-8"))

#CSVs
transacoes = pd.read_csv("transacoes.csv", parse_dates=["data"])
atendimentos = pd.read_csv("historico_atendimento.csv", parse_dates=["data"])

```

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

```text
PERFIL DO CLIENTE:

{
    "nome": "João Silva",
    "idade": 31,
    "profissao": "Arquiteta",
    "renda_mensal": 9600.0,
    "perfil_investidor": "arrojado",
    "objetivo_principal": "Aumentar patrimônio a longo prazo",
    "patrimonio_total": 49900.0,
    "reserva_emergencia_atual": 20400.0,
    "aceita_risco": true,
    "metas": [
      {
        "meta": "Completar reserva de emergência",
        "valor_necessario": 18700,
        "prazo": "2025-04"
      },
      {
        "meta": "Entrada do apartamento",
        "valor_necessario": 45400,
        "prazo": "2029-01"
      }
    ]
  }

PRODUTOS DISPONÍVEIS PARA SUPORTE:

{
    "nome": "Tesouro Selic",
    "categoria": "renda_fixa",
    "risco": "baixo",
    "rentabilidade": "100% da Selic",
    "aporte_minimo": 30.0,
    "liquidez": "D+1",
    "prazo_recomendado": "Curto prazo",
    "imposto_renda": true,
    "indicado_para": "Reserva de emergência e iniciantes"
  },
  {
    "nome": "Tesouro IPCA+ 2029",
    "categoria": "renda_fixa",
    "risco": "baixo",
    "rentabilidade": "IPCA + 6,5% ao ano",
    "aporte_minimo": 30.0,
    "liquidez": "D+1 (com marcação a mercado)",
    "prazo_recomendado": "Médio a longo prazo",
    "imposto_renda": true,
    "indicado_para": "Proteção contra inflação e aposentadoria"
  }

TRANSAÇÕES DO CLIENTE:

data	descricao	categoria	valor	tipo
2024-01-06	Restaurante	alimentacao	1709.05	saida
2024-01-08	Viagem	lazer	428.28	saida
2024-01-15	Cashback	receita	1839.26	entrada
2024-01-17	Combustível	transporte	680.34	saida
2024-01-22	Conta de Luz	moradia	2248.83	saida

HISTÓRICO DE ATENDIMENTO DO CLIENTE:

data	canal	tema	resumo	resolvido
2024-01-01	email	Limite de transferência	Cliente solicitou aumento de limite TED	sim
2024-01-11	WhatsApp	Extrato	Dúvida sobre lançamento no extrato	sim
2024-02-05	email	Segurança e senha	Cliente relatou acesso suspeito	sim
2024-02-11	telefone	LCA	Cliente quis saber sobre isenção de IR	sim
2024-02-11	app	CDB	Cliente perguntou sobre rentabilidade e prazos	nao
2024-02-24	app	Cartão de crédito	Contestação de cobrança indevida	nao
```

---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

```
Dados do Cliente:
- Nome: João Silva
- Perfil: Moderado
- Saldo disponível: R$ 5.000

Últimas transações:
- 01/11: Supermercado - R$ 450
- 03/11: Streaming - R$ 55
...
```
