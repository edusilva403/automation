import pandas as pd
import numpy as np
import datetime as dt
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

#import time
#import openpyxl
#import os
#from time import sleep
#---------------------------------------------------------------------------------------------------------
# Retrieve the data from session state
db_consolidado = st.session_state['db_consolidado']
db_resumo_por_filial = st.session_state['db_resumo_por_filial']
db_resumo_por_empresa = st.session_state['db_resumo_por_empresa']
db_resumo_por_synap = st.session_state['db_resumo_por_synap']







# FILTROS DE SELEÇÃO
col1, col2, col3 = st.columns([2,2,1])

with col1:
            select_empresa = st.multiselect('Empresa',db_consolidado.sort_values(by=['EMPRESA'])['EMPRESA'].unique(),placeholder='Empresa',label_visibility='collapsed')           
            if len(select_empresa)>0:
                        var_empresa = select_empresa
            else: var_empresa = db_consolidado['EMPRESA'].unique()


with col2:
            select_filial = st.multiselect('Filial',db_consolidado.sort_values(by=['FILIAL']).loc[db_consolidado['EMPRESA'].isin(var_empresa)]['FILIAL'].unique(), placeholder='Filial',label_visibility='collapsed')
            if len(select_filial)>0:
                var_filial = select_filial
            else: var_filial = db_consolidado['FILIAL'].unique()



with col3:
            var_anos = db_consolidado.sort_values(by=['ANO'], ascending=False)['ANO'].unique()
            var_ano = st.slider('Ano',min_value=var_anos[-1], max_value=var_anos[0], value=var_anos[0], label_visibility='collapsed')



with st.container():
        
    var_show_filial =   db_resumo_por_filial.loc[
                        (db_resumo_por_filial['ANO'] == var_ano) & 
                        (db_resumo_por_filial['FILIAL'].isin(var_filial)) &
                        (db_resumo_por_filial['EMPRESA'].isin(var_empresa) )].reset_index(drop=True)


    var_show_empresa =   db_resumo_por_empresa.loc[
                        (db_resumo_por_empresa['ANO'] == var_ano)&
                        (db_resumo_por_empresa['EMPRESA'].isin(var_empresa))].reset_index(drop=True)

    var_show_synap =    db_resumo_por_synap.loc[
                        (db_resumo_por_synap['ANO'] == var_ano)].reset_index(drop=True)




    if  len(var_filial)!= len(db_consolidado['FILIAL'].unique()):
        var_level_selection = var_show_filial

    elif (len(var_empresa)!= len(db_consolidado['EMPRESA'].unique())) & (len(var_filial)== len(db_consolidado['FILIAL'].unique())):
        var_level_selection = var_show_empresa
    else:
        var_level_selection = var_show_synap
    

    
    
    #st.dataframe(var_show_filial,hide_index=True,  use_container_width=True)



    ordena_eixo_x = pd.DataFrame({'ANO-MES':var_level_selection['ANO-MES'].unique()})
    ordena_eixo_x['MES'] =ordena_eixo_x['ANO-MES'].str[7:].astype(int)
    ordena_eixo_x.sort_values(by='MES', inplace=True)
    ordenar = list(ordena_eixo_x['ANO-MES'])



    
    chart_por_mes = px.bar(var_level_selection,x='ANO-MES', 
                        y=['ESCOADO - VALOR ACC','CARTEIRA - VALOR ACC','VENDAS TO GO - CARTEIRA ACC'], 
                        barmode='stack',color_discrete_sequence =['green','blue','grey','pink'])


    chart_por_mes.update_xaxes(title=None,categoryorder='array', categoryarray=ordenar).update_yaxes(title=None).update_layout(showlegend=True)

    


            #chart.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    
    st.subheader(f'Meta de Faturamento Ano: {'{:,.2f} Mio'.format(var_level_selection['META FATURAMENTO'].sum())}')

    
  


    


    

    fig = go.Figure()

    

    fig.add_trace(
    go.Scatter(name='META',
        x=ordenar,
        y=var_level_selection['META FATURAMENTO ACC'],marker=dict(color='red')
    ))


    if var_ano==datetime.today().year:
        fig.add_trace(
        go.Bar(name='ESCOADO - VALOR ACC',
        x=ordenar,
        y=var_level_selection.loc[(var_level_selection['ANO']<=var_ano)&(var_level_selection['MES']<=datetime.today().month)]['ESCOADO - VALOR ACC'],marker=dict(color='green')))
   
        fig.add_trace(
        go.Bar(name='CARTEIRA - VALOR ACC',
        x=ordenar,
        y=var_level_selection.loc[(var_level_selection['ANO']<=var_ano)&(var_level_selection['MES']<=datetime.today().month)]['CARTEIRA - VALOR ACC'],marker=dict(color='blue')))
    
    else:

        fig.add_trace(
        go.Bar(name='ESCOADO - VALOR ACC',
        x=ordenar,
        y=var_level_selection.loc[var_level_selection['ANO']<=var_ano]['ESCOADO - VALOR ACC'],marker=dict(color='green')))
   
        fig.add_trace(
        go.Bar(name='CARTEIRA - VALOR ACC',
        x=ordenar,
        y=var_level_selection.loc[var_level_selection['ANO']<=var_ano]['CARTEIRA - VALOR ACC'],marker=dict(color='blue')))


    fig.update_layout(barmode='stack')

    if var_ano ==datetime.today().year:
        st.write('True')

    st.plotly_chart(fig, use_container_width=True)
  
    #st.plotly_chart(chart_por_mes)
    #print(db_consolidado.columns)

#print(consolida_arquivos())
#arquivo_excel = (r'C:\Users\s1154221\Downloads\cons_all.xlsx')
#db_resumo_por_empresa.to_excel(arquivo_excel , sheet_name='Sheet1', index=False)
