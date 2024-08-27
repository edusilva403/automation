import pandas as pd
import datetime as dt
from datetime import datetime
import plotly.express as px
import streamlit as st
st. set_page_config(layout="wide")
st.markdown(" <style> div[class^='block-container']{padding-top: 3rem; padding-bottom: 5rem; padding-left: 1rem; padding-right: 1rem;}  </style> ", unsafe_allow_html=True)



about_page1 = st.Page(

    page="views/page1.py", default=True
)

about_page2 = st.Page(

    page="views/page2.py"
)


pg = st.navigation(
    {'Home':[about_page1],
    'Pages': [about_page2]})

st.logo('assets\\logo_synap.png')



# base de dados


#db1------------
@st.cache_data
def consolida_arquivos():
    db_consolidado  = pd.read_excel(r'C:\Users\s1154221\OneDrive - Syngenta\Codigos\relatorio_personalizado.xlsx')    
    #Ordena por ano-mes
    db_consolidado.sort_values(['ANO','MES'],ascending=True,inplace=True, ignore_index=True)

    #Formata valores
    columns_to_be_formatted = ['CARTEIRA - VALOR','ESCOADO - VALOR', 'ESCOADO + CARTEIRA - VALOR', 'META CONSULTOR','META FATURAMENTO', 'PLANO PEC - VALOR', 'PLANO  S&OP - VALOR','VPM MAPEADO R$', 'VPM TOTAL R$']
    
    for i in db_consolidado.columns:
           if i in columns_to_be_formatted:                  
                db_consolidado[i] = db_consolidado[i].apply(lambda x: x/1000000)
                #db_consolidado[i] = db_consolidado[i].map('{:,.3f}M'.format, na_action='ignore')
    

    #Tratando os meses
    db_consolidado['MES']=db_consolidado['MES'].map(
           {'Jan':1, 'Fev':2,'Mar':3,'Abr':4,'Mai':5,'Jun':6,'Jul':7,'Ago':8,'Set':9,'Out':10,'Nov':11,'Dez':12}, na_action='ignore')    
    db_consolidado['ANO-MES'] = db_consolidado['ANO'].astype(str)+' | ' + db_consolidado['MES'].astype(str)
    

    #Substitui os PRYMES
    db_consolidado['FILIAL'] = db_consolidado['FILIAL'].apply(lambda x: str(x).replace('PRYME PR - ', '').replace('PRYME RS - ', '').replace('PRYME SC - ', ''))
    

    #Adiciona colunas TO GO
    db_consolidado.loc[db_consolidado['META FATURAMENTO']==0,'VENDAS TO GO'] = 0
    db_consolidado.loc[db_consolidado['META FATURAMENTO']>0,'VENDAS TO GO'] = db_consolidado['META FATURAMENTO'] - db_consolidado['ESCOADO - VALOR']

    db_consolidado.loc[db_consolidado['META FATURAMENTO']==0,'VENDAS TO GO - CARTEIRA'] = 0
    db_consolidado.loc[db_consolidado['META FATURAMENTO']>0,'VENDAS TO GO - CARTEIRA'] = db_consolidado['VENDAS TO GO'] - db_consolidado['CARTEIRA - VALOR']
    
    #Adiciona YTD Flag
    db_consolidado.loc[db_consolidado['MES']<= datetime.now().month , 'YTD Flag'] = True

       
    return db_consolidado



#db4--------------------------------
db_resumo_por_synap = consolida_arquivos().groupby(
       ['ANO','MES', 'ANO-MES'])[['CARTEIRA - VALOR','ESCOADO - VALOR','META FATURAMENTO','VENDAS TO GO','VENDAS TO GO - CARTEIRA']].sum().reset_index()[
               ['ANO','MES','ANO-MES','META FATURAMENTO', 'ESCOADO - VALOR','VENDAS TO GO','CARTEIRA - VALOR','VENDAS TO GO - CARTEIRA']]

#Adiciona colunas ACC
var_agrupamento = db_resumo_por_synap.groupby(['ANO'])

db_resumo_por_synap['META FATURAMENTO ACC'] = var_agrupamento['META FATURAMENTO'].cumsum()
db_resumo_por_synap['ESCOADO - VALOR ACC'] = var_agrupamento['ESCOADO - VALOR'].cumsum()
db_resumo_por_synap['VENDAS TO GO ACC'] = var_agrupamento['VENDAS TO GO'].cumsum()
db_resumo_por_synap['CARTEIRA - VALOR ACC'] = var_agrupamento['CARTEIRA - VALOR'].cumsum()
db_resumo_por_synap['VENDAS TO GO - CARTEIRA ACC'] = var_agrupamento['VENDAS TO GO - CARTEIRA'].cumsum()


#Adiciona colunas TO GO
db_resumo_por_synap.loc[db_resumo_por_synap['META FATURAMENTO']==0,'VENDAS TO GO'] = 0
db_resumo_por_synap.loc[db_resumo_por_synap['META FATURAMENTO']>0,'VENDAS TO GO'] = db_resumo_por_synap['META FATURAMENTO'] - db_resumo_por_synap['ESCOADO - VALOR']
  
db_resumo_por_synap.loc[db_resumo_por_synap['META FATURAMENTO']==0,'VENDAS TO GO - CARTEIRA'] = 0
db_resumo_por_synap.loc[db_resumo_por_synap['META FATURAMENTO']>0,'VENDAS TO GO - CARTEIRA'] = db_resumo_por_synap['VENDAS TO GO'] - db_resumo_por_synap['CARTEIRA - VALOR']



db_resumo_por_synap.loc[db_resumo_por_synap['META FATURAMENTO ACC']==0,'VENDAS TO GO ACC'] = 0
db_resumo_por_synap.loc[db_resumo_por_synap['META FATURAMENTO ACC']>0,'VENDAS TO GO ACC'] = db_resumo_por_synap['META FATURAMENTO ACC'] - db_resumo_por_synap['ESCOADO - VALOR ACC']
  
db_resumo_por_synap.loc[db_resumo_por_synap['META FATURAMENTO ACC']==0,'VENDAS TO GO - CARTEIRA ACC'] = 0
db_resumo_por_synap.loc[db_resumo_por_synap['META FATURAMENTO ACC']>0,'VENDAS TO GO - CARTEIRA ACC'] = db_resumo_por_synap['VENDAS TO GO ACC'] - db_resumo_por_synap['CARTEIRA - VALOR ACC']















#db2--------------------------------
db_resumo_por_empresa = consolida_arquivos().groupby(
       ['EMPRESA','ANO','MES', 'ANO-MES'])[['CARTEIRA - VALOR','ESCOADO - VALOR','META FATURAMENTO','VENDAS TO GO','VENDAS TO GO - CARTEIRA']].sum().reset_index()[
               ['EMPRESA','ANO','MES','ANO-MES','META FATURAMENTO', 'ESCOADO - VALOR','VENDAS TO GO','CARTEIRA - VALOR','VENDAS TO GO - CARTEIRA']]

#Adiciona colunas ACC
var_agrupamento = db_resumo_por_empresa.groupby(['EMPRESA','ANO'])

db_resumo_por_empresa['META FATURAMENTO ACC'] = var_agrupamento['META FATURAMENTO'].cumsum()
db_resumo_por_empresa['ESCOADO - VALOR ACC'] = var_agrupamento['ESCOADO - VALOR'].cumsum()
db_resumo_por_empresa['VENDAS TO GO ACC'] = var_agrupamento['VENDAS TO GO'].cumsum()
db_resumo_por_empresa['CARTEIRA - VALOR ACC'] = var_agrupamento['CARTEIRA - VALOR'].cumsum()
db_resumo_por_empresa['VENDAS TO GO - CARTEIRA ACC'] = var_agrupamento['VENDAS TO GO - CARTEIRA'].cumsum()


#Adiciona colunas TO GO
db_resumo_por_empresa.loc[db_resumo_por_empresa['META FATURAMENTO']==0,'VENDAS TO GO'] = 0
db_resumo_por_empresa.loc[db_resumo_por_empresa['META FATURAMENTO']>0,'VENDAS TO GO'] = db_resumo_por_empresa['META FATURAMENTO'] - db_resumo_por_empresa['ESCOADO - VALOR']
  
db_resumo_por_empresa.loc[db_resumo_por_empresa['META FATURAMENTO']==0,'VENDAS TO GO - CARTEIRA'] = 0
db_resumo_por_empresa.loc[db_resumo_por_empresa['META FATURAMENTO']>0,'VENDAS TO GO - CARTEIRA'] = db_resumo_por_empresa['VENDAS TO GO'] - db_resumo_por_empresa['CARTEIRA - VALOR']



db_resumo_por_empresa.loc[db_resumo_por_empresa['META FATURAMENTO ACC']==0,'VENDAS TO GO ACC'] = 0
db_resumo_por_empresa.loc[db_resumo_por_empresa['META FATURAMENTO ACC']>0,'VENDAS TO GO ACC'] = db_resumo_por_empresa['META FATURAMENTO ACC'] - db_resumo_por_empresa['ESCOADO - VALOR ACC']
  
db_resumo_por_empresa.loc[db_resumo_por_empresa['META FATURAMENTO ACC']==0,'VENDAS TO GO - CARTEIRA ACC'] = 0
db_resumo_por_empresa.loc[db_resumo_por_empresa['META FATURAMENTO ACC']>0,'VENDAS TO GO - CARTEIRA ACC'] = db_resumo_por_empresa['VENDAS TO GO ACC'] - db_resumo_por_empresa['CARTEIRA - VALOR ACC']






#db3--------------------------------
db_resumo_por_filial = consolida_arquivos().groupby(
       ['EMPRESA','FILIAL','ANO','MES', 'ANO-MES'])[['CARTEIRA - VALOR','ESCOADO - VALOR','META FATURAMENTO','VENDAS TO GO','VENDAS TO GO - CARTEIRA']].sum().reset_index()[
               ['EMPRESA','FILIAL','ANO','MES','ANO-MES','META FATURAMENTO', 'ESCOADO - VALOR','VENDAS TO GO','CARTEIRA - VALOR','VENDAS TO GO - CARTEIRA']]

#Adiciona colunas ACC
var_agrupamento = db_resumo_por_filial.groupby(['EMPRESA','FILIAL','ANO'])

db_resumo_por_filial['META FATURAMENTO ACC'] = var_agrupamento['META FATURAMENTO'].cumsum()
db_resumo_por_filial['ESCOADO - VALOR ACC'] = var_agrupamento['ESCOADO - VALOR'].cumsum()
db_resumo_por_filial['VENDAS TO GO ACC'] = var_agrupamento['VENDAS TO GO'].cumsum()
db_resumo_por_filial['CARTEIRA - VALOR ACC'] = var_agrupamento['CARTEIRA - VALOR'].cumsum()
db_resumo_por_filial['VENDAS TO GO - CARTEIRA ACC'] = var_agrupamento['VENDAS TO GO - CARTEIRA'].cumsum()


#Adiciona colunas TO GO
db_resumo_por_filial.loc[db_resumo_por_filial['META FATURAMENTO']==0,'VENDAS TO GO'] = 0
db_resumo_por_filial.loc[db_resumo_por_filial['META FATURAMENTO']>0,'VENDAS TO GO'] = db_resumo_por_filial['META FATURAMENTO'] - db_resumo_por_filial['ESCOADO - VALOR']
  
db_resumo_por_filial.loc[db_resumo_por_filial['META FATURAMENTO']==0,'VENDAS TO GO - CARTEIRA'] = 0
db_resumo_por_filial.loc[db_resumo_por_filial['META FATURAMENTO']>0,'VENDAS TO GO - CARTEIRA'] = db_resumo_por_filial['VENDAS TO GO'] - db_resumo_por_filial['CARTEIRA - VALOR']



db_resumo_por_filial.loc[db_resumo_por_filial['META FATURAMENTO ACC']==0,'VENDAS TO GO ACC'] = 0
db_resumo_por_filial.loc[db_resumo_por_filial['META FATURAMENTO ACC']>0,'VENDAS TO GO ACC'] = db_resumo_por_filial['META FATURAMENTO ACC'] - db_resumo_por_filial['ESCOADO - VALOR ACC']
  
db_resumo_por_filial.loc[db_resumo_por_filial['META FATURAMENTO ACC']==0,'VENDAS TO GO - CARTEIRA ACC'] = 0
db_resumo_por_filial.loc[db_resumo_por_filial['META FATURAMENTO ACC']>0,'VENDAS TO GO - CARTEIRA ACC'] = db_resumo_por_filial['VENDAS TO GO ACC'] - db_resumo_por_filial['CARTEIRA - VALOR ACC']








# Check if you've already initialized the data

if 'db_consolidado' not in st.session_state:
    # Get the data if you haven't
    df1 = consolida_arquivos()
    # Save the data to session state
    st.session_state['db_consolidado'] = df1

if 'db_resumo_por_filial' not in st.session_state:
    # Get the data if you haven't
    df2 = db_resumo_por_filial
    # Save the data to session state
    st.session_state['db_resumo_por_filial'] = df2

if 'db_resumo_por_empresa' not in st.session_state:
    # Get the data if you haven't
    df3 = db_resumo_por_empresa
    # Save the data to session state
    st.session_state['db_resumo_por_empresa'] = df3

if 'db_resumo_por_synap' not in st.session_state:
    # Get the data if you haven't
    df4 = db_resumo_por_synap
    # Save the data to session state
    st.session_state['db_resumo_por_synap'] = df4

    


# Check if you've already initialized the data



pg.run()

