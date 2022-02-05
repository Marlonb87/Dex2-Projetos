# -*- coding: utf-8 -*-
"""Data preparation - ImovelWeb.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1L1-mKilGhfm5nCVgA9mqHWZ5O5vPQcvJ

## **Para ler excel**
"""

pip uninstall xlrd

pip uninstall openpyxl

pip install xlrd

pip install openpyxl

"""#**Importando dados**

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
from matplotlib import pyplot 
from google.colab import drive

drive.mount('/content/drive', force_remount= True)

df = pd.read_excel('/content/drive/MyDrive/IMOVELWEB/Carteiras Totais - DNC _V3.xlsx')

"""#**Codigos auxiliares**

"""

In [25]: pd.set_option('display.float_format', lambda x: '%.3f' % x)

"""# **Tratando Dados**

"""

#Criando coluna de variação de "valor hoje" - "valor mensal"
df['VH - VM'] = df['VALOR HOJE'] - df['VALOR MENSAL']

#Transformando os nomes das colunas maisculo
df.columns = df.columns.str.upper()

df_select = df.drop(['ID CRM', 'ID NAVPLAT', 'CIDADE','BAIRRO','VALOR HOJE' ,'FATURAMENTO', 'LEADS TOTAL','TOTAL DE LISTINGS','FAIXA LISTINGS' ], axis =1)

df_select.head()

#Substituir regiões com outras nomeclaturas
df_select['REGIÃO'].replace({'São Paulo': 'SP', 'SAO PAULO': 'SP', 'Acre' : 'AC', 'Alagoas': 'AL',
                      'Amapá': 'AP', 'Amazonas':'AM', 'Banhia': 'BA', 'Espírito Santo' : 'ES', 'Goiás' : 'GO',
                      'Mina Gerais' : 'MG', 'Minas Gerais' : 'MG', 'Mato Grosso do Sul' : 'MS',
                      'Mato Grosso' : 'MT', 'Ceará' : 'CE', 'Maranhão' : 'MA', 'Pará' : 'PA',
                      'Paraíba' : 'PB', 'Pernambuco' : 'PE', 'Piauí' : 'PI', 'Paraná' : 'PR',
                      'Rio De Janeiro' : 'RJ', 'Rio Grande Do Norte' : 'RN', 'Roraima' : 'RR',
                      'Distrito Federal' : 'DF', 'Rio Grande Do Sul' : 'RS', 'Tocantins' : 'TO',
                      'Santa Catarina' : 'SC', 'Sergipe' : 'SE' ,}, inplace=True)
       
df_select['REGIÃO'].replace({'Banhia' : 'BA', 'Sao Paulo' : 'SP', 'Mato Grosso Do Sul' : 'MS',
                            'Rio de Janeiro' : 'RJ', 'Rio de janeiro' : 'RJ', 'RIO DE JANEIRO' : 'RJ',
                            'Paraná' : 'PR','Paraná ' : 'PR', 'Bastos': 'SP'}, inplace = True)

df_select['REGIÃO'].replace({'Brasília' : 'DF', 'Paraná' : 'PR', 'FORTALEZA' : 'CE', 'Fortaleza' : 'CE',
                            'Porto Belo' : 'SC', 'Porto Alegre' : 'RS', 'Mogi das Cruzes' : 'SP',
                           'Mairiporã' : 'SP', 'Canoas' : 'RS', 'Cotia' : 'SP', 'CAMPINAS' : 'SP',
                            'Duque de Caxias' : 'RJ', 'Belo Horizonte' : 'MG', 'Caruaru' : 'PE',
                            'Diadema' : 'SP', 'Curitiba' : 'PR', 'Bahia' : 'BA'}, inplace=True)

#Preenche os 0 e os "outros paises" por np.nan
df_select['REGIÃO'].replace({0:np.nan,'Outros Paises':np.nan},inplace = True)

#Preenche os np.nan por valores que tem o mesmo id sap
df_select['REGIÃO'] = df_select.groupby('ID SAP')['REGIÃO'].ffill().bfill()

#Colocando em maiusculo as strings
df_select['UPSALE/DOWNSALE'] = df_select['UPSALE/DOWNSALE'].str.upper()

#substituir valores nulos das 'CONTRATADO FREEMIUM' e 'UTILIZADO FREEMIUM' por zero
df_select['UTILIZADO FREEMIUM'] = df_select['UTILIZADO FREEMIUM'].fillna(0)
df_select['CONTRATADO FREEMIUM'] = df_select['CONTRATADO FREEMIUM'].fillna(0)

#Colocando em maiusculo as strings
df_select['EQUIPE'] = df_select['EQUIPE'].str.upper()

#Colocando em maiusculo as strings
df_select['STATUS FINAL'] = df_select['STATUS FINAL'].str.upper()

"""#**Analisando Dados**"""

#Substituir os valores de UPSELL e DOWNSELL POR OK
df_select['UPSALE/DOWNSALE'].replace({'UPSELL': 'OK', 'DOWNSELL' : 'OK'}, inplace = True)

df_select['VALOR MENSAL'].describe(percentiles = [0.001, .01, .1, .25, .5, .75, .9, .99, .999])
#Valores abaixo de 57 (plan minimo) estão certos?
#Valores muito altos também?

b = pd.DataFrame(df_select[['UPSALE/DOWNSALE', 'TIPO DE PLANO']])
b['UPSALE/DOWNSALE'] = b['UPSALE/DOWNSALE'].replace({'UPSELL': 'OK', 'ILIMITADO': 'OK', 'PACK' : 'OK', 'DOWNSELL': 'OK'})
teste = b.groupby(['UPSALE/DOWNSALE','TIPO DE PLANO']).size()
teste
teste.plot(kind='bar')

# Plotar gráfico de quantidade de UPSELL/DOWNSELL, CHURN E OK
fig = plt.figure()

sns.set_theme(style="whitegrid")
ax = sns.barplot(x= df_select['UPSALE/DOWNSALE'].unique(), y=df_select['UPSALE/DOWNSALE'].value_counts(normalize = True), data= df_select)

plt.ylabel('')
plt.title("% Status Churn", loc = 'left', )

# Plotar gráfico de quantidade de cada status
fig = plt.figure(figsize = (20, 6))

sns.set_theme(style="whitegrid")
ax = sns.barplot(x= df_select['STATUS FINAL'].unique(), y=df_select['STATUS FINAL'].value_counts(normalize = True), data= df_select)
plt.ylabel('')
plt.title("% Status Cliente", loc = 'left')

# Criar dataframe só com churns
df_churn = df_select[df_select['UPSALE/DOWNSALE'] == 'CHURN']

# Plotar gráfico de churn/tipo de plano
fig = plt.figure(figsize = (5, 4))

sns.set_theme(style="whitegrid")
ax = sns.barplot(x= df_churn['TIPO DE PLANO'].unique(), y=df_churn['TIPO DE PLANO'].value_counts(normalize = True), data= df_select)
plt.ylabel('')
plt.title("% Churn/Tipo de Plano", loc = 'left')

# Plotar gráfico de  quantidade de tipo de plano
fig = plt.figure(figsize = (5, 4))

sns.set_theme(style="whitegrid")
ax = sns.barplot(x= df_select['TIPO DE PLANO'].unique(), y= df_select['TIPO DE PLANO'].value_counts(normalize = True), data= df_select)
plt.ylabel('')
plt.title("% Tipo de Plano", loc = 'left')

# Plotar gráfico de churn/equipe
fig = plt.figure(figsize = (10, 4))

ax = sns.barplot(x= df_churn['EQUIPE'].unique(), y=df_churn['EQUIPE'].value_counts(normalize = True), data= df_select)
plt.ylabel('')
plt.title("% Churn/Equipe", loc = 'left')

# Plotar gráfico de  quantidade de equipe
fig = plt.figure(figsize = (10, 4))

sns.set_theme(style="whitegrid")
ax = sns.barplot(x= df_select['EQUIPE'].unique(), y= df_select['EQUIPE'].value_counts(normalize = True), data= df_select)
plt.ylabel('')
plt.title("% Equipe", loc = 'left')

# Plotar gráfico de churn/tipo de cancelamento
fig = plt.figure(figsize = (10, 4))

sns.set_theme(style="whitegrid")
ax = sns.barplot(x= df_churn['STATUS FINAL'].unique(), y=df_churn['STATUS FINAL'].value_counts(normalize = True), data= df_select)
plt.ylabel('')
plt.title("% Churn/Tipo de Cancelamento", loc = 'left')

# Plotar gráfico de churn/mês
fig = plt.figure(figsize = (10, 4))

sns.set_theme(style="whitegrid")
sns.lineplot(x=df_churn['MÊS'].unique(), y=df_churn['MÊS'].value_counts())
plt.ylabel('')
plt.title("Churn por Mês", loc = 'left')

# Criar dataframe só com 'CANCELADO POR SOLICITACAO'
df_cancelado = df_select[df_select['STATUS FINAL'] == 'CANCELADO POR SOLICITACAO']

# Plotar gráfico de 'CANCELADO POR SOLICITACAO'/tipo de plano
fig = plt.figure(figsize = (5, 4))

sns.set_theme(style="whitegrid")
ax = sns.barplot(x= df_cancelado['TIPO DE PLANO'].unique(), y=df_cancelado['TIPO DE PLANO'].value_counts(normalize = True), data= df_select)
plt.ylabel('')
plt.title("% Cancelamento Solicitado/Tipo de Plano", loc = 'left')

# Plotar gráfico de 'CANCELADO POR SOLICITACAO'/equipe
fig = plt.figure(figsize = (10, 4))

sns.set_theme(style="whitegrid")
ax = sns.barplot(x= df_cancelado['EQUIPE'].unique(), y=df_cancelado['EQUIPE'].value_counts(normalize = True), data= df_select)
plt.ylabel('')
plt.title("% Cancelamento Solicitado/Equipe", loc = 'left')

# Plotar gráfico de 'CANCELADO POR SOLICITACAO'/Região
fig = plt.figure(figsize = (10, 4))

sns.set_theme(style="whitegrid")
ax = sns.barplot(x= df_cancelado['REGIÃO'].unique(), y=df_cancelado['REGIÃO'].value_counts(normalize = True), data= df_select)
plt.ylabel('')
plt.title("% Cancelamento Solicitado/Região", loc = 'left')