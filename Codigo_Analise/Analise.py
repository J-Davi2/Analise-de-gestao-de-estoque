# =========================
# 1.0 VISÃO GERAL
# ========================= 

# ========================= 
'''
Objetivo:
Identificar padrões de vendas e auxiliar decisões
de estoque com base em dados mensais, baseados nas vendas diárias .
'''
# =========================

#%%

# ===================================================
# 1.1 - Importação de Bibliotecas e limpeza de dados
# 1.2 - Buscando o arquivo necessario para analise e fazendo ajustes do "Sep" 
# ===================================================

import pandas as pd

df = pd.read_csv("../data/Vendas_RP1.csv", sep = ";", encoding="latin1")
df

# %%

# 1.3 - Como o aquivo mostrou algumas colunas com valores nulos, o processo agora é de limpeza desses valores

df.dropna(axis=1, how="all", inplace=True)

# %%

# ============================================================
# 2.0 - Adcionando Colunas de valores e representação de mês
# ============================================================

#%%

# 2.1 - adicionando uma nova coluna, transformando a data no valor respctivo apenas ao mês. Convertendo de String pra data
# Exmeplo: 01/12/2025 = 12-2025, Representando dezembro de 2025,

df['Data'] = pd.to_datetime(df["Data"], dayfirst=True)
df["Mes_Ano"] = df["Data"].dt.to_period("M")
df



# %%

# 2.2 - Adcionando coluna do valor total, calculado da quantidade de vendas X o valor individual

df['ValorTotal'] = df['ValorUnitario'] * df['QtdeProduto']
df

# %%

# 2.3 - Organizando as colunas em uma ordem mais viável para análise 

colunas = ["Id_venda", "Data", "Mes_Ano", "Marca", "Modelo", "ValorUnitario", "QtdeProduto", "ValorTotal", "Pagamento_forma"]
new_df = df[colunas]
new_df

# %%

# ==========================
# 3.0 - Começando análise 
# ==========================

#%%

# 3.1 - quantidade de produtos vendidos: 183 vendas

new_df["QtdeProduto"].sum()

# %%

# 3.2 -Faturamento total completo: R$ 264.315,00

new_df["ValorTotal"].sum()

# %%

# 3.3 - Mês que vendeu mais: 
# Pegando a quantidade de vendas por mês, para saber: Qual vendeu mais e quantas vendas ocorreram.

mensal_Vendas = new_df.groupby("Mes_Ano")["QtdeProduto"].sum().sort_values(ascending=False)
mensal_Vendas

# Mês que vendeu mais: 3(Março) 
# Quantidade de vendas = 60 vendas

#%%

# 3.4 - Usando a mesma lógica para saber: Qual mês mais teve faturamento e de Quanto foi o faturamento.

mensal_faturamento = new_df.groupby("Mes_Ano")["ValorTotal"].sum().sort_values(ascending=False)
mensal_faturamento

# Mês com Maior faturamento: 3(Março) 
# Valor do faturamento = R$ 85.400

# %%

# 3.5 - Ordem de modelos que mais foram vendidos

new_df.groupby("Modelo")["QtdeProduto"].sum().sort_values(ascending=False)

# Top 3 modelos mais vendidos: 
'''
A07 = 17
Note 60X = 15
Redmi 15 = 13
'''

# %%

# 3.6 -  Ordem dos produtos menos vendidos
# Top 3 Modelos menos vendidos: 
'''
12 Pro Max    1
14 Pro Max    1
17 Pro Max    1
'''

new_df.groupby("Modelo")["QtdeProduto"].sum().sort_values().head(3)

# %%

# 3.7 Procurar saber qual Marca mais gerou faturamento com base nas vendas

new_df.groupby("Marca")["QtdeProduto"].sum().sort_values(ascending=False)

# Marca que vendeu mais gerando mais faturamento: Redmi 
# Quantidade de celulares vendidos = 58 Celulares

# %%

# 3.8 - Preço médio das vendas: 1573.30

ticket_medio = new_df["ValorTotal"].mean()
ticket_medio

# O ticket médio das vendas ficou em aproximadamente R$ 1600,00,
# indicando maior concentração de compras em smartphones intermediários.

# %%

# 3.9 - A ordem dos modelos que vendem mais e seus respectivos faturamentos 

modelo_fat = (new_df.groupby("Modelo").agg({
    "ValorTotal" : "sum",
    "QtdeProduto" : "sum"
}).sort_values(by="QtdeProduto", ascending=False))

modelo_fat

# Sendo eles A07, Note 60X e Redmi 15, os mais vendidos dentre esses meses

# %%

# 4.0 - Lucro, Giro e estoque. Quais são eles?
# Criando uma função pra saber como classificar cada um dos produtos por cada modelo 

limite_qtde = modelo_fat["QtdeProduto"].quantile(0.75)
limite_valor = modelo_fat["ValorTotal"].quantile(0.75)

def classificar(row):
    if row["QtdeProduto"] > limite_qtde and row["ValorTotal"] > limite_valor:
        return "🆗Estoque"
    elif row["QtdeProduto"] > limite_qtde:
        return "💱Giro"
    elif row["ValorTotal"] > limite_valor:
        return "💲Lucro"
    else:
        return "✅normal"
    
modelo_fat["categoria"] = modelo_fat.apply(classificar, axis=1)

modelo_fat["categoria"]
# %%

"""
Conclusão Final:

A análise mostrou que modelos como A07,
Note 60X e Redmi 15 apresentaram maior
volume de vendas e consistência.

Além disso, observou-se que smartphones
na faixa intermediária possuem melhor
equilíbrio entre giro e faturamento.

Portanto, recomenda-se manter foco em
modelos de entrada/intermediários das
marcas com maior presença nas vendas.
"""

new_df.to_csv("dados_tratados.csv", index=False)

# %%
