#!/usr/bin/env python
# coding: utf-8

# In[1026]:


import pandas as pd
from connect import PostgreSQL
from tqdm import tqdm
import datetime as dt
from datetime import date
import time
import plotly.graph_objs as go
import pywhatkit as pwk
from html2image import Html2Image
import shutil
import pyautogui as gui

print('Iniciando o envio as ' + dt.datetime.now().strftime('%H:%M:%S'))


# In[1027]:


def proportion_size(pixels:int=None, size:int=None, padrao:int=2160):
    sizing = float(pixels / (padrao / size))
    return sizing


# In[1028]:


def bg_colors(dataframe, datetime:str, dia_util:str):
    
    colors = []
    date_colors = []
    destak_color = []
    

    for i in dataframe.index:
        if dataframe.loc[i, dia_util] == 'Não':
            date_colors.append('#DEEFFF')
            destak_color.append('#DEEFFF')

        elif dataframe.loc[i, datetime].strftime('%d/%m/%Y') == dt.datetime.now().strftime('%d/%m/%Y'):
            date_colors.append('#F7F7F7')
            destak_color.append('#F7F7F7')
            
        else:
            date_colors.append('#FFFFFF')
            destak_color.append('#F7F7F7')

    date_colors.append('#E5E5E5')
    destak_color.append('#E5E5E5')


    for coluna in dataframe.columns:
        colors.append(date_colors)

    colors[2] = destak_color
    colors[3] = destak_color
    colors[6] = destak_color
    colors[9] = destak_color

    return colors


# In[1029]:


def font_projecao_mensal(dataframe, datetime:str, dia_util:str, principal_color:str):
    
    colors = []
    date_colors = []
    

    for i in dataframe.index:
        if dataframe.loc[i, datetime] > dt.datetime.now():
            if dataframe.loc[i, dia_util] == 'Não':
                date_colors.append('#DEEFFF')
                
            else:
                date_colors.append('#FFFFFF')

        else:
            if dataframe.loc[i, dia_util] == 'Não':
                date_colors.append('#DEEFFF')
                
            else:
                date_colors.append(principal_color)

    date_colors.append('#118DFF')


    for coluna in dataframe.columns:
        colors.append(date_colors)

    return colors


# In[1030]:


def font_rendimento(dataframe, percents:str, datetime:str, dia_util:str, principal_color:str):
    
    colors = []
    date_colors = []
    

    for i in dataframe.index:
        if dataframe.loc[i, datetime] != ' ':
            if dataframe.loc[i, dia_util] == 'Não':
                    date_colors.append('#DEEFFF')

            elif dataframe.loc[i, datetime] < dt.datetime.now():
                if dataframe.loc[i, percents] >= 1:
                    date_colors.append('#00B050')

                elif dataframe.loc[i, percents] < 0.95:
                    date_colors.append('#FF0000')

                elif dataframe.loc[i, percents] < 1:
                    date_colors.append('#FFC000')
                    
            else:
                date_colors.append('#FFFFFF')

        else:
                date_colors.append(principal_color)

    date_colors.append('#E5E5E5')

    for coluna in dataframe.columns:
        colors.append(date_colors)

    return colors[0]


# # Parâmetros

# In[1031]:


_schema = 'H-1'


# In[10]:


_pixels = 890

pixels_width = 2060 #int((_pixels/9) * 17)
pixels_height = int(_pixels)

print(f'Taxa de proporção: \n ⇳: {pixels_height} ⬄: {pixels_width}')


# In[1033]:


date_query = date(int((dt.datetime.now().strftime('%Y-%m-%d').split('-')[0])), int((dt.datetime.now().strftime('%Y-%m-%d').split('-')[1])), 1).strftime('%Y-%m-%d')


# In[1034]:


codigos_kaizen = [(         'PECISTA', '02608'),

                  (    'CLIENTE VALE', '00270'),
    
                  ('KAIZEN ASA NORTE', '13996'),
                  (     'USO INTERNO', '20690'),

                  ('KAIZEN CEILÂNDIA', '16100'),
                  (     'USO INTERNO', '20691'),

                  (     'KAIZEN GAMA', '18400'),
                  (     'USO INTERNO', '20692'),

                  (  'KAIZEN SOF SUL', '20000'),
                  (     'USO INTERNO', '20693')]


# In[1035]:


lista_lojas = [('01',             'CD', '#000000', 'ⒸⒹ', False),
               ('02',               '', '#000000', '', False),
               ('03',  '04. ASA NORTE', '#881798', 'ⒶⓈⒶ ⓃⓄⓇⓉⒺ', True),
               ('04',  '02. CEILÂNDIA', '#008080', 'ⒸⒺⒾⓁⒶⓃⒹⒾⒶ', True),
               ('05',       '03. GAMA', '#E74856', 'ⒼⒶⓂⒶ', True),
               ('06',    '01. SOF SUL', '#00B050', 'ⓈⓄⒻ ⓈⓊⓁ', True),
               ('VO', '05. E-COMMERCE', '#FFC000', 'Ⓔ-ⒸⓄⓂⓂⒺⓇⒸⒺ', True)]


# In[1036]:


dias_semana = [(   'Sunday',       'Domingo'),
               (   'Monday', 'Segunda-feira'),
               (  'Tuesday',   'Terça-feira'),
               ('Wednesday',  'Quarta-feira'),
               ( 'Thursday',  'Quinta-feira'),
               (   'Friday',   'Sexta-feira'),
               ( 'Saturday',        'Sábado')]


# In[1037]:


relatorio = 'TESTE'

relatorio_lower = relatorio.lower()
relatorio_msg = relatorio_lower.replace(relatorio_lower.split()[0], relatorio_lower.split()[0].title())


# In[1038]:


caminho_imagem = 'Y:\\COMPRAS\\arquivo temporario analise atualizado\\DEPARTAMENTO COMPRAS\\10. CARLOS\\REPORT'


# In[1039]:


contatos = [('PrimeiraFoto', 'https://chat.whatsapp.com/LK4LDajkH52BNydoLGGD2d', True),
            ('Dados e Int',  'https://chat.whatsapp.com/JxY14kWarG70MxB2jzb5pc', False),
            ('Dream Team',   'https://chat.whatsapp.com/Hb0KMgYnuFB8coTPlFKTzJ', False),
            ('Report Di',    'https://chat.whatsapp.com/G4p8qdUIUblCNPS80244RQ', False),
            ('API',          'https://chat.whatsapp.com/EBLX0fxYfvuHL7jZ9CZECQ', True),
            ('Teste Python', 'https://chat.whatsapp.com/I4y7EAVfns629NvfoLUtGI', True)]


# #

# # DataFrames

# ## Clientes

# In[1040]:


df_cliente = PostgreSQL.read_postgres(name_table='cliente', schema=_schema)


# In[1041]:


df_cli_ped = PostgreSQL.read_postgres(name_table='cli_ped', schema=_schema, query=f'WHERE DT_CADASTR >= \'{date_query}\'')


# ## Pedidos

# In[1042]:


df_pedido = PostgreSQL.read_postgres(name_table='pedido', schema=_schema, query=f'WHERE DT_EMISSAO >= \'{date_query}\'')


# In[1043]:


df_pedido['VALOR_TOT'] = df_pedido['VALOR_TOT'].astype(float)


# In[1044]:


for (kaizen, codcli_kaizen) in tqdm(codigos_kaizen):
    print(f'Excluindo {kaizen} - {codcli_kaizen}')
    df_pedido = df_pedido[df_pedido['CODCLI'] != codcli_kaizen]


# In[1045]:


df_pedido = df_pedido[df_pedido['CODVDE'] != '0001']
df_pedido = df_pedido[df_pedido['CODVDE'] != '0100']


# In[1046]:


df_pedido = df_pedido[df_pedido['TIPPED'] == 'V']


# In[1047]:


df_pedido = df_pedido[df_pedido['OBSERVA'].str.contains('REQ') != True]
df_pedido = df_pedido[df_pedido['OBSERVA2'].str.contains('REQ') != True]


# In[1048]:


for i in tqdm(df_pedido.index):
    if df_pedido.loc[i, 'FORMA_PGTO'] == 'M':
        df_pedido.loc[i, 'COD_LOJA'] = 'VO'
    else:
        df_pedido.loc[i, 'COD_LOJA'] = df_pedido.loc[i, 'CD_LOJA']


# In[1049]:


for i in tqdm(df_pedido.index):
    if df_pedido.loc[i, 'COD_LOJA'] == 'VO':
        df_pedido.loc[i, 'NU_CPFCNPJ'] = list(df_cli_ped[(df_cli_ped['CD_LOJA'] == df_pedido.loc[i, 'CD_LOJA']) &
                                             (df_cli_ped['SG_PEDIDO'] == df_pedido.loc[i, 'SERIE']) &
                                             (df_cli_ped['NU_PEDIDO'] == df_pedido.loc[i, 'NU_NOTA'])]['NU_CPFCNPJ'])[0]


# In[1050]:


df_pedido = pd.merge(df_pedido, df_cliente, how='inner', on='CODCLI')


# In[1051]:


for i in tqdm(df_pedido.index):

    if df_pedido.loc[i, 'COD_LOJA'] == 'VO':
        identify = df_pedido.loc[i, 'NU_CPFCNPJ']
    else:
        identify = df_pedido.loc[i, 'CPF_CGC']

    if df_pedido.loc[i, 'CODAREA'] == '104':
        df_pedido.loc[i, 'TIPO_CLIENTE'] = 'CNPJ*'
    elif len(identify) < 14:
        df_pedido.loc[i, 'TIPO_CLIENTE'] = 'CPF'
    else:
        df_pedido.loc[i, 'TIPO_CLIENTE'] = 'CNPJ'


# ## Devolução

# In[1052]:


df_prod_ent = PostgreSQL.read_postgres(full_query=f'select a.*, (a.VL_PRECO*a.QT_DEVOLVE) as VL_TOTAL_DEV, b.IN_CLIFOR as IN_CLIFOR1, b.IN_CANCELA, UPPER(b.NFEENVSTAT) as NFEENVSTAT, c.FORMA_PGTO from "{_schema}".prod_ent a inner join "{_schema}".entrada b on a.CD_LOJA = b.CD_LOJA and a.SG_SERIE = b.SG_SERIE and a.NU_NOTA = b.NU_NOTA inner join "{_schema}".venda c on a.CD_LOJA = c.CD_LOJA and a.SG_ORIGEM = c.SERIE and a.NU_ORIGEM = c.NU_NOTA where a.DT_EMISSAO >= \'{date_query}\'')


# In[1053]:


for (kaizen, codcli_kaizen) in tqdm(codigos_kaizen):
    print(f'Excluindo {kaizen} - {codcli_kaizen}')
    df_prod_ent = df_prod_ent[df_prod_ent['CD_CLIENTE'] != codcli_kaizen]


# In[1054]:


df_prod_ent = df_prod_ent[(df_prod_ent['IN_CANCELA'] == 'N') &
                          (df_prod_ent['IN_CLIFOR1'] == 'C') &
                          (df_prod_ent['CD_CFOP'] != '1949') &
                          (df_prod_ent['CD_CFOP'] != '2949') &
                          (df_prod_ent['CD_CFOP'] != '1603') &
                          (df_prod_ent['NFEENVSTAT'].str.contains('DENEG') != True)]


# In[1055]:


for i in tqdm(df_prod_ent.index):
    if df_prod_ent.loc[i, 'FORMA_PGTO'] == 'M':
        df_prod_ent.loc[i, 'COD_LOJA'] = 'VO'
    else:
        df_prod_ent.loc[i, 'COD_LOJA'] = df_prod_ent.loc[i, 'CD_LOJA']


# In[1056]:


df_prod_ent['VL_TOTAL_DEV'] = df_prod_ent['VL_TOTAL_DEV'].astype(float)


# In[1057]:


df_prod_ent = df_prod_ent.rename(columns={'CD_CLIENTE':'CODCLI'})
df_prod_ent = pd.merge(df_prod_ent, df_cliente, how='inner', on='CODCLI')


# In[1058]:


for i in tqdm(df_prod_ent.index):

    identify = df_prod_ent.loc[i, 'CPF_CGC']

    if df_prod_ent.loc[i, 'CODAREA'] == '104':
        df_prod_ent.loc[i, 'TIPO_CLIENTE'] = 'CNPJ*'
    elif len(identify) < 14:
        df_prod_ent.loc[i, 'TIPO_CLIENTE'] = 'CPF'
    else:
        df_prod_ent.loc[i, 'TIPO_CLIENTE'] = 'CNPJ'


# ## Metas

# In[1059]:


df_metas = pd.read_excel('Y:\\COMPRAS\\arquivo temporario analise atualizado\\DEPARTAMENTO COMPRAS\\10. CARLOS\\PROJETOS\\EXCEL\\BASES\\DATAS.xlsx', sheet_name='Metas')


# In[1060]:


df_data = pd.read_excel('Y:\\COMPRAS\\arquivo temporario analise atualizado\\DEPARTAMENTO COMPRAS\\10. CARLOS\\PROJETOS\\EXCEL\\BASES\\DATAS.xlsx', sheet_name='Datas')


# In[1061]:


df_proporcional = pd.read_excel('Y:\\COMPRAS\\arquivo temporario analise atualizado\\DEPARTAMENTO COMPRAS\\10. CARLOS\\PROJETOS\\EXCEL\\BASES\\DATAS.xlsx', sheet_name='Proporcional')


# In[1062]:


df_datas = df_data[df_data['Mês - Ano'] == df_data[df_data['Data'] == date_query]['Mês - Ano'].values[0]].reset_index(drop=True)


# In[1063]:


df_meta_mes = df_metas[df_metas['Mês - Ano'] == df_datas['Mês - Ano'][0]]


# In[1064]:


df_meta_data = df_datas.drop(columns=['Dia', 'Mês', 'Ano', 'Dia da Semana', 'Nome - Mês', 'Semestre', 'Trimestre', 'Sequencial - Dia da Semana', 'Dias Úteis']).merge(df_meta_mes.drop(columns=['Mês', 'Ano', 'Dias Úteis', 'Qtd Sábados', 'Nome - Mês', 'Loja']), how='inner', on='Mês - Ano').rename(columns={'Cd_Loja': 'CD_LOJA'})


# In[1065]:


df_meta_data = df_meta_data.merge(df_proporcional, how='left', on=['CD_LOJA', 'Data'])

df_meta_data['%'] = df_meta_data['%'].fillna(1)


# In[1066]:


for i in df_meta_data.index:
    if df_meta_data.loc[i, 'Dia Útil'] == 'Sim':
        df_meta_data.loc[i, 'Meta'] = df_meta_data.loc[i, 'Meta Diária']
    
    elif df_meta_data.loc[i, 'Dia Útil'] == 'Meio':
        df_meta_data.loc[i, 'Meta'] = df_meta_data.loc[i, 'Meta Sábado']

    else:
        df_meta_data.loc[i, 'Meta'] = 0

    df_meta_data.loc[i, 'Meta'] = df_meta_data.loc[i, 'Meta'] * df_meta_data.loc[i, '%']

df_meta_data = df_meta_data.rename(columns={'Data':'DT_EMISSAO'})


# # Cálculo

# In[1067]:


df_venda_bruta = df_pedido.groupby(['COD_LOJA', 'DT_EMISSAO']).sum()[['VALOR_TOT']].reset_index().rename(columns={'COD_LOJA':'CD_LOJA'})


# In[1068]:


df_devolucao = df_prod_ent.groupby(['COD_LOJA', 'DT_EMISSAO']).sum()[['VL_TOTAL_DEV']].reset_index().rename(columns={'COD_LOJA':'CD_LOJA'})


# In[1069]:


df_venda_bruta_cnpj = df_pedido[df_pedido['TIPO_CLIENTE'] != 'CPF'].groupby(['COD_LOJA', 'DT_EMISSAO']).sum()[['VALOR_TOT']].reset_index().rename(columns={'COD_LOJA':'CD_LOJA'})
df_devolucao_cnpj = df_prod_ent[df_prod_ent['TIPO_CLIENTE'] != 'CPF'].groupby(['COD_LOJA', 'DT_EMISSAO']).sum()[['VL_TOTAL_DEV']].reset_index().rename(columns={'COD_LOJA':'CD_LOJA'})


# In[1070]:


df_venda_bruta_cpf = df_pedido[df_pedido['TIPO_CLIENTE'] == 'CPF'].groupby(['COD_LOJA', 'DT_EMISSAO']).sum()[['VALOR_TOT']].reset_index().rename(columns={'COD_LOJA':'CD_LOJA'})
df_devolucao_cpf = df_prod_ent[df_prod_ent['TIPO_CLIENTE'] == 'CPF'].groupby(['COD_LOJA', 'DT_EMISSAO']).sum()[['VL_TOTAL_DEV']].reset_index().rename(columns={'COD_LOJA':'CD_LOJA'})


# In[1071]:


df_final = pd.merge(df_venda_bruta, df_devolucao, how='outer', on=['CD_LOJA', 'DT_EMISSAO'])

df_final = df_final.sort_values(by=['DT_EMISSAO', 'CD_LOJA'])
df_final = df_final.reset_index(drop=True)

df_final = pd.merge(df_meta_data, df_final, how='left', on=['CD_LOJA', 'DT_EMISSAO'])


# In[1072]:


df_final = df_final.fillna(0)


# In[1073]:


df_hoje = df_final
df_hoje = df_hoje.rename(columns={'VALOR_TOT':'VENDA BRUTA', 'VL_TOTAL_DEV':'DEVOLUÇÃO', 'Meta':'META'})

for i in tqdm(df_hoje.index):
    df_hoje.loc[i, 'VENDA LÍQUIDA'] = (df_hoje.loc[i, 'VENDA BRUTA'] - df_hoje.loc[i, 'DEVOLUÇÃO'])
    
    if df_hoje.loc[i, 'CD_LOJA'] == 'VO':

        client_cgc = list(df_pedido[(df_pedido['DT_EMISSAO'] == df_hoje.loc[i, 'DT_EMISSAO']) &
                         (df_pedido['COD_LOJA'] == df_hoje.loc[i, 'CD_LOJA']) &
                         (df_pedido['TIPO_CLIENTE'] != 'CPF')]['NU_CPFCNPJ'].drop_duplicates().dropna())

        client_cpf = list(df_pedido[(df_pedido['DT_EMISSAO'] == df_hoje.loc[i, 'DT_EMISSAO']) &
                         (df_pedido['COD_LOJA'] == df_hoje.loc[i, 'CD_LOJA']) &
                         (df_pedido['TIPO_CLIENTE'] == 'CPF')]['NU_CPFCNPJ'].drop_duplicates().dropna())
    
    else:

        client_cgc = list(df_pedido[(df_pedido['DT_EMISSAO'] == df_hoje.loc[i, 'DT_EMISSAO']) &
                         (df_pedido['COD_LOJA'] == df_hoje.loc[i, 'CD_LOJA']) &
                         (df_pedido['TIPO_CLIENTE'] != 'CPF')]['CPF_CGC'].drop_duplicates())

        client_cpf = list(df_pedido[(df_pedido['DT_EMISSAO'] == df_hoje.loc[i, 'DT_EMISSAO']) &
                         (df_pedido['COD_LOJA'] == df_hoje.loc[i, 'CD_LOJA']) &
                         (df_pedido['TIPO_CLIENTE'] == 'CPF')]['CPF_CGC'].drop_duplicates())

    venda_cgc = list(df_pedido[(df_pedido['DT_EMISSAO'] == df_hoje.loc[i, 'DT_EMISSAO']) &
                    (df_pedido['COD_LOJA'] == df_hoje.loc[i, 'CD_LOJA']) &
                    (df_pedido['TIPO_CLIENTE'] != 'CPF')]['VALOR_TOT'])

    venda_cpf = list(df_pedido[(df_pedido['DT_EMISSAO'] == df_hoje.loc[i, 'DT_EMISSAO']) &
                    (df_pedido['COD_LOJA'] == df_hoje.loc[i, 'CD_LOJA']) &
                    (df_pedido['TIPO_CLIENTE'] == 'CPF')]['VALOR_TOT'])

    devol_cgc = list(df_prod_ent[(df_prod_ent['DT_EMISSAO'] == df_hoje.loc[i, 'DT_EMISSAO']) &
                    (df_prod_ent['COD_LOJA'] == df_hoje.loc[i, 'CD_LOJA']) &
                    (df_prod_ent['TIPO_CLIENTE'] != 'CPF')]['VL_TOTAL_DEV'])

    devol_cpf = list(df_prod_ent[(df_prod_ent['DT_EMISSAO'] == df_hoje.loc[i, 'DT_EMISSAO']) &
                    (df_prod_ent['COD_LOJA'] == df_hoje.loc[i, 'CD_LOJA']) &
                    (df_prod_ent['TIPO_CLIENTE'] == 'CPF')]['VL_TOTAL_DEV'])

    if sum(devol_cgc) > 0 and sum(venda_cgc) > 0:
        percent_cgc = sum(devol_cgc) / sum(venda_cgc)
    else:
        percent_cgc = 0

    if sum(devol_cpf) > 0 and sum(venda_cpf) > 0:
        percent_cpf = sum(devol_cpf) / sum(venda_cpf)
    else:
        percent_cpf = 0

    df_hoje.loc[i, 'VENDA_CNPJ'] = (sum(venda_cgc) - sum(devol_cgc))
    df_hoje.loc[i, 'DEVOL_CNPJ'] = sum(devol_cgc)
    df_hoje.loc[i, '% DEV CNPJ'] = percent_cgc
    df_hoje.loc[i, 'CNPJ'] = len(client_cgc)

    df_hoje.loc[i, 'VENDA_CPF'] = (sum(venda_cpf) - sum(devol_cpf))
    df_hoje.loc[i, 'DEVOL_CPF'] = sum(devol_cpf)
    df_hoje.loc[i, '% DEV CPF'] = percent_cpf
    df_hoje.loc[i, 'CPF'] = len(client_cpf)

    if df_hoje.loc[i, 'VENDA LÍQUIDA'] == 0:
        df_hoje.loc[i, '% META DIA'] = 0
    else:
        df_hoje.loc[i, '% META DIA'] = df_hoje.loc[i, 'VENDA LÍQUIDA'] / df_hoje.loc[i, 'META']

    if df_hoje.loc[i, 'DEVOLUÇÃO'] == 0:
        df_hoje.loc[i, '% DEV'] = 0
    else:
        df_hoje.loc[i, '% DEV'] = df_hoje.loc[i, 'DEVOLUÇÃO'] / df_hoje.loc[i, 'VENDA BRUTA']


# In[1074]:


df_hoje = df_hoje.fillna(0)


# # 

# In[1075]:


def print_plot(principal_dataframe:str = None,
               lojas = None,
               loja_ = '',
               save_image = ''):
    
    if len(loja_) > 0:
        df_print = principal_dataframe[principal_dataframe['CD_LOJA'] == loja_].reset_index(drop=True)

        if loja_ == 'VO':
            client_cgc_mes_vo = []
            client_cgc_mes = list(df_pedido[(df_pedido['COD_LOJA'] == loja_) &
                                 (df_pedido['TIPO_CLIENTE'] != 'CPF')]['NU_CPFCNPJ'].drop_duplicates().dropna())
        else:
            client_cgc_mes_vo = []
            client_cgc_mes = list(df_pedido[(df_pedido['COD_LOJA'] == loja_) &
                                 (df_pedido['TIPO_CLIENTE'] != 'CPF')]['CPF_CGC'].drop_duplicates())


        df_print = df_print[['DT_EMISSAO',
                             'Dia Útil',
                             'Nome - Dia da Semana',
                             'CD_LOJA',
                             'META',
                             'VENDA BRUTA',
                             'VENDA LÍQUIDA',
                             'DEVOLUÇÃO',
                             'VENDA_CNPJ',
                             'DEVOL_CNPJ',
                             'CNPJ',
                             'VENDA_CPF',
                             'DEVOL_CPF',
                             'CPF']]

    else:
        df_print = principal_dataframe.groupby(['DT_EMISSAO', 'Dia Útil', 'Nome - Dia da Semana']).sum(['META',
                                                                                                        'VENDA BRUTA',
                                                                                                        'DEVOLUÇÃO',
                                                                                                        'VENDA LÍQUIDA',
                                                                                                        'VENDA_CNPJ',
                                                                                                        'DEVOL_CNPJ',
                                                                                                        'CNPJ',
                                                                                                        'VENDA_CPF',
                                                                                                        'DEVOL_CPF',
                                                                                                        'CPF']).reset_index()


        client_cgc_mes = list(df_pedido[(df_pedido['TIPO_CLIENTE'] != 'CPF')]['CPF_CGC'].drop_duplicates())
        client_cgc_mes_vo = list(df_pedido[df_pedido['TIPO_CLIENTE'] != 'CPF']['NU_CPFCNPJ'].drop_duplicates().dropna())

    
        df_print = df_print[['DT_EMISSAO',
                             'Dia Útil',
                             'Nome - Dia da Semana',
                             'META',
                             'VENDA BRUTA',
                             'VENDA LÍQUIDA',
                             'DEVOLUÇÃO',
                             'VENDA_CNPJ',
                             'DEVOL_CNPJ',
                             'CNPJ',
                             'VENDA_CPF',
                             'DEVOL_CPF',
                             'CPF']]

    for i in df_print.index:
        if df_print.loc[i, 'DEVOLUÇÃO'] == 0:
            df_print.loc[i, '% DEV'] = 0
        else:
            df_print.loc[i, '% DEV'] = df_print.loc[i, 'DEVOLUÇÃO'] / df_print.loc[i, 'VENDA BRUTA']

        
        if df_print.loc[i, 'DEVOL_CNPJ'] == 0:
            df_print.loc[i, '% DEV CNPJ'] = 0
        else:
            df_print.loc[i, '% DEV CNPJ'] = df_print.loc[i, 'DEVOL_CNPJ'] / df_print.loc[i, 'VENDA_CNPJ']


        if df_print.loc[i, 'DEVOL_CPF'] == 0:
            df_print.loc[i, '% DEV CPF'] = 0
        else:
            df_print.loc[i, '% DEV CPF'] = df_print.loc[i, 'DEVOL_CPF'] / df_print.loc[i, 'VENDA_CPF']

        if df_print.loc[i, 'VENDA LÍQUIDA'] == 0:
            df_print.loc[i, '% META DIA'] = 0
        else:
            df_print.loc[i, '% META DIA'] = df_print.loc[i, 'VENDA LÍQUIDA'] / df_print.loc[i, 'META']

    venda_mtd = []
    meta_mtd = []

    for i in df_print.index:

        venda_mtd.append(list(df_print.loc[:i, 'VENDA LÍQUIDA']))
        df_print.loc[i, 'VENDA_MTD'] = sum(venda_mtd[i])

        meta_mtd.append(list(df_print.loc[:i, 'META']))
        df_print.loc[i, 'META_MTD'] = sum(meta_mtd[i])

        if df_print.loc[i, 'VENDA_MTD'] == 0:
            df_print.loc[i, '% META MÊS'] = 0
        else:
            df_print.loc[i, '% META MÊS'] = df_print.loc[i, 'VENDA_MTD'] / df_print.loc[i, 'META_MTD']






    for i in df_print.index:

        df_print.loc[i, 'PROJEÇÃO MÊS'] = df_print.loc[i, '% META MÊS'] * round(float(sum(list(df_print['META']))), 2)

    df_print = df_print.rename(columns={'DT_EMISSAO': 'Data',
                                        'META': 'Meta',
                                        'VENDA BRUTA': 'Venda\nSIAC',
                                        'VENDA LÍQUIDA': 'Venda\nLíquida',
                                        'DEVOLUÇÃO': 'Devolução',
                                        '% DEV': '%\nDev',
                                        'VENDA_CNPJ': 'Venda\nCNPJ',
                                        'CNPJ': 'Clientes\nCNPJ',
                                        '% DEV CNPJ': '% Dev\nCNPJ',
                                        'VENDA_CPF': 'Venda\nCPF',
                                        'CPF': 'Clientes\nCPF',
                                        '% DEV CPF': '% Dev\nCPF',
                                        '% META DIA': '%\nDia',
                                        '% META MÊS': '%\nMês',
                                        'PROJEÇÃO MÊS': 'Projeção\nmensal'})


    background_color = bg_colors(df_print, 'Data', 'Dia Útil')
    fonts_color = font_projecao_mensal(df_print, 'Data', 'Dia Útil', '#000000')
    day_rending_color = font_rendimento(df_print, '%\nDia', 'Data', 'Dia Útil', '#FFFFFF')
    mon_rending_color = font_rendimento(df_print, '%\nMês', 'Data', 'Dia Útil', '#FFFFFF')


    percent_total_dev = (round(float(sum(list(df_print['Devolução']))), 2) / round(float(sum(list(df_print['Venda\nSIAC']))), 2))
    percent_total_dev_pj = (round(float(sum(list(df_print['DEVOL_CNPJ']))), 2) / round(float(sum(list(df_print['Venda\nCNPJ']))), 2))
    percent_total_dev_pf = (round(float(sum(list(df_print['DEVOL_CPF']))), 2) / round(float(sum(list(df_print['Venda\nCPF']))), 2))


    df_print.loc[len(df_print), 'Data'] = ' '


    df_print = df_print.fillna(0)

    df_print.loc[len(df_print) - 1, 'Meta'] = round(float(sum(list(df_print['Meta']))), 2)
    df_print.loc[len(df_print) - 1, 'Venda\nSIAC'] = round(float(sum(list(df_print['Venda\nSIAC']))), 2)
    df_print.loc[len(df_print) - 1, 'Venda\nLíquida'] = round(float(sum(list(df_print['Venda\nLíquida']))), 2)
    df_print.loc[len(df_print) - 1, 'Devolução'] = round(float(sum(list(df_print['Devolução']))), 2)
    df_print.loc[len(df_print) - 1, '%\nDev'] = percent_total_dev
    df_print.loc[len(df_print) - 1, 'Venda\nCNPJ'] = round(float(sum(list(df_print['Venda\nCNPJ']))), 2)
    df_print.loc[len(df_print) - 1, 'Clientes\nCNPJ'] = round(float(len(client_cgc_mes) + len(client_cgc_mes_vo)), 2)  #round(float(sum(list(df_print['Clientes\nCNPJ']))), 2)
    df_print.loc[len(df_print) - 1, '% Dev\nCNPJ'] = percent_total_dev_pj
    df_print.loc[len(df_print) - 1, 'Venda\nCPF'] = round(float(sum(list(df_print['Venda\nCPF']))), 2)
    df_print.loc[len(df_print) - 1, 'Clientes\nCPF'] = round(float(sum(list(df_print['Clientes\nCPF']))), 2)
    df_print.loc[len(df_print) - 1, '% Dev\nCPF'] = percent_total_dev_pf
    df_print.loc[len(df_print) - 1, '%\nDia'] = df_print.loc[len(df_print) - 1, 'Venda\nLíquida'] / df_print.loc[len(df_print) - 1, 'Meta']
    df_print.loc[len(df_print) - 1, '%\nMês'] = df_print.loc[len(df_print) - 1, 'Venda\nLíquida'] / df_print.loc[len(df_print) - 1, 'Meta']
    df_print.loc[len(df_print) - 1, 'Projeção\nmensal'] = 0






    df_print = df_print[['Data',
                         'Meta',
                         'Venda\nSIAC',
                         'Venda\nLíquida',
                         'Devolução',
                         '%\nDev',
                         'Venda\nCNPJ',
                         'Clientes\nCNPJ',
                         '% Dev\nCNPJ',
                         'Venda\nCPF',
                         'Clientes\nCPF',
                         '% Dev\nCPF',
                         '%\nDia',
                         '%\nMês',
                         'Projeção\nmensal']]



    for i in df_print.index:
        df_print.loc[i, 'Meta'] = 'R$ {:_.2f}'.format(df_print.loc[i, 'Meta']).replace('.',',').replace('_','.')
        df_print.loc[i, 'Venda\nSIAC'] = 'R$ {:_.2f}'.format(df_print.loc[i, 'Venda\nSIAC']).replace('.',',').replace('_','.')
        df_print.loc[i, 'Devolução'] = 'R$ {:_.2f}'.format(df_print.loc[i, 'Devolução']).replace('.',',').replace('_','.')
        df_print.loc[i, '%\nDev'] = '{:_.2%}'.format(df_print.loc[i, '%\nDev']).replace('.',',').replace('_','.')
        df_print.loc[i, 'Venda\nCNPJ'] = 'R$ {:_.2f}'.format(df_print.loc[i, 'Venda\nCNPJ']).replace('.',',').replace('_','.')
        df_print.loc[i, '% Dev\nCNPJ'] = '{:_.2%}'.format(df_print.loc[i, '% Dev\nCNPJ']).replace('.',',').replace('_','.')
        df_print.loc[i, 'Clientes\nCNPJ'] = '{:_.0f}'.format(df_print.loc[i, 'Clientes\nCNPJ']).replace('.',',').replace('_','.')
        df_print.loc[i, 'Venda\nCPF'] = 'R$ {:_.2f}'.format(df_print.loc[i, 'Venda\nCPF']).replace('.',',').replace('_','.')
        df_print.loc[i, '% Dev\nCPF'] = '{:_.2%}'.format(df_print.loc[i, '% Dev\nCPF']).replace('.',',').replace('_','.')
        df_print.loc[i, 'Clientes\nCPF'] = '{:_.0f}'.format(df_print.loc[i, 'Clientes\nCPF']).replace('.',',').replace('_','.')
        df_print.loc[i, '%\nDia'] = '{:_.2%}'.format(df_print.loc[i, '%\nDia']).replace('.',',').replace('_','.')
        df_print.loc[i, '%\nMês'] = '{:_.2%}'.format(df_print.loc[i, '%\nMês']).replace('.',',').replace('_','.')
        df_print.loc[i, 'Projeção\nmensal'] = 'R$ {:_.2f}'.format(df_print.loc[i, 'Projeção\nmensal']).replace('.',',').replace('_','.')

        if df_print.loc[i, 'Venda\nLíquida'] < 0:
            df_print.loc[i, 'Venda\nLíquida'] = '-R$ {:_.2f}'.format(df_print.loc[i, 'Venda\nLíquida'] * -1).replace('.',',').replace('_','.')
        else:
            df_print.loc[i, 'Venda\nLíquida'] = 'R$ {:_.2f}'.format(df_print.loc[i, 'Venda\nLíquida']).replace('.',',').replace('_','.')

        if df_print.loc[i, 'Data'] == ' ':
            df_print.loc[i, 'Data'] = 'Total'
        else:
            df_print.loc[i, 'Data'] = df_print.loc[i, 'Data'].strftime('%d/%m/%Y, %A')


        for (english, portuguese) in dias_semana:
            if english in df_print.loc[i, 'Data']:
                df_print.loc[i, 'Data'] = df_print.loc[i, 'Data'].replace(english, portuguese)



    df_print = df_print.replace('inf%', '').replace('-inf%', '').replace('0,00%', '').replace('R$ 0,00', '').replace('0', '')


    table = go.Figure(go.Table(header={'values':list(df_print.columns),
                                       'fill_color': '#E5E5E5',
                                       'line_color': '#E5E5E5',
                                       'line_width': 3,
                                       'align': 'center',
                                       'font_color': ['#000000',
                                                      '#000000',
                                                      '#118DFF',
                                                      '#000000',
                                                      '#FF0000',
                                                      '#FF0000',
                                                      '#E04392',
                                                      '#000000',
                                                      '#FF0000',
                                                      '#E04392',
                                                      '#000000',
                                                      '#FF0000',
                                                      '#000000',
                                                      '#000000',
                                                      '#000000'],
                                       'font_family': 'Segoe UI Semibold',
                                       'font_size': proportion_size(pixels=_pixels, size=32)
                                       },
                                        
                                cells={'values':[list(df_print['Data']),
                                                 list(df_print['Meta']),
                                                 list(df_print['Venda\nSIAC']),
                                                 list(df_print['Venda\nLíquida']),
                                                 list(df_print['Devolução']),
                                                 list(df_print['%\nDev']),
                                                 list(df_print['Venda\nCNPJ']),
                                                 list(df_print['Clientes\nCNPJ']),
                                                 list(df_print['% Dev\nCNPJ']),
                                                 list(df_print['Venda\nCPF']),
                                                 list(df_print['Clientes\nCPF']),
                                                 list(df_print['% Dev\nCPF']),
                                                 list(df_print['%\nDia']),
                                                 list(df_print['%\nMês']),
                                                 list(df_print['Projeção\nmensal'])],
                                       'fill_color': background_color,
                                       'line_color': background_color,
                                       'line_width': 2,
                                       'align': ['left', 'center'],
                                       'font_color': ['#000000',
                                                      '#000000',
                                                      '#118DFF',
                                                      '#000000',
                                                      '#FF0000',
                                                      '#FF0000',
                                                      '#E04392',
                                                      '#000000',
                                                      '#FF0000',
                                                      '#E04392',
                                                      '#000000',
                                                      '#FF0000',
                                                      day_rending_color,
                                                      mon_rending_color,
                                                      fonts_color[0]],
                                       'font_family': 'Segoe UI Semibold',
                                       'font_size': proportion_size(pixels=_pixels, size=32)
                                       },

                               domain={'y': [0, 1]
                                       },

                          columnwidth=[proportion_size(pixels=_pixels, size=25),
                                       proportion_size(pixels=_pixels, size=16),
                                       proportion_size(pixels=_pixels, size=16),
                                       proportion_size(pixels=_pixels, size=16),
                                       proportion_size(pixels=_pixels, size=16),
                                       proportion_size(pixels=_pixels, size=10),
                                       proportion_size(pixels=_pixels, size=16),
                                       proportion_size(pixels=_pixels, size=13),
                                       proportion_size(pixels=_pixels, size=12),
                                       proportion_size(pixels=_pixels, size=16),
                                       proportion_size(pixels=_pixels, size=12),
                                       proportion_size(pixels=_pixels, size=10),
                                       proportion_size(pixels=_pixels, size=7),
                                       proportion_size(pixels=_pixels, size=7),
                                       proportion_size(pixels=_pixels, size=16)]
                                )
    )

    for (cod_loja, loja, cor, crypto, logico) in lojas:
        if cod_loja == loja_:
            print_loja = loja[4:5] + loja[5:].lower()
            print_loja = loja[4:]
            print_cor = cor
            print_crypto = crypto
            save_loja = f'{cod_loja} '

    if len(loja_) > 0:
        text_title = f'◙'*int(10) + ' 🡆 ' + print_loja + ' 🡄 ' + f'◙'*int(76) + ' ' + print_crypto + ' ' + f'◙'*int(10)
    else:
        text_title = f'◙'*int(10) + ' 🡆 ' + 'KAIZEN' + ' 🡄 ' + f'◙'*int(76) + ' ' + 'ⓀⒶⒾⓏⒺⓃ' + ' ' + f'◙'*int(10)
        print_cor = '#00A5AC'
        save_loja = f''

    table = table.update_layout(

        #Title config ---------------------------------------------------------------------------------------------------------------------#
        title  = {'text': text_title,
                  'font_color': print_cor,
                  'font_family': 'Jost',
                  'x': 0.50,
                  'y': 0.95,
                  'font_size': proportion_size(pixels=_pixels, size=60),
                  'yanchor': 'bottom'
                  },

        #Size plot config -----------------------------------------------------------------------------------------------------------------#
        width  = pixels_width,
        height = pixels_height
    )

    table.show()
    time.sleep(5)
    table.write_html(f'{save_image}\\RESUMO MENSAL_html\\{relatorio} {save_loja}TABLE.html')


    hti = Html2Image()
    hti.screenshot(
        html_file=f'{save_image}\\RESUMO MENSAL_html\\{relatorio} {save_loja}TABLE.html',
        save_as=f'{relatorio} {save_loja}TABLE.png',
        size=(pixels_width, pixels_height)
    )

    shutil.move(f'{relatorio} {save_loja}TABLE.png',
                f'{save_image}\\{relatorio} {save_loja}TABLE.png')


    return print(f'{relatorio} {save_loja}TABLE.png\n')


# In[1100]:


date_msg = dt.datetime.now().strftime('%d-%m-%Y')

print_plot(principal_dataframe=df_hoje,
            lojas=lista_lojas,
            save_image=caminho_imagem)

gui.hotkey('ctrl', 'w')

for (contato, link, logico) in contatos:
    if logico:
        print(f'{date_msg} {contato} - {link}')
        pwk.sendwhats_image(link.replace('https://chat.whatsapp.com/', ''),
                            f'{caminho_imagem}\\{relatorio} TABLE.png',
                            f'Resumo mensal | Grupo - {date_msg}',
                            tab_close=True,
                            wait_time=10)


# In[1076]:


for (cod_loja, loja, cor, crypto, logico) in lista_lojas:

    if logico:
        print(f'\n• \'{cod_loja}\' {loja[4:]}\n')
        print_plot(principal_dataframe=df_hoje,
                   lojas=lista_lojas,
                   loja_=cod_loja,
                   save_image=caminho_imagem)

        msg_loja = loja.replace('Â', 'A')

        gui.hotkey('ctrl', 'w')

        for (contato, link, logico) in contatos:
            if logico:
                print(f'{date_msg} {contato} - {link}')
                pwk.sendwhats_image(link.replace('https://chat.whatsapp.com/', ''),
                                    f'{caminho_imagem}\\{relatorio} {cod_loja} TABLE.png',
                                    f'Resumo mensal | {msg_loja[4:]} - {date_msg}',
                                    tab_close=True,
                                    wait_time=10)