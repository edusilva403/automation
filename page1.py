import pandas as pd
import numpy as np
import datetime as dt
from datetime import datetime
import plotly.express as px
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





#Streamlit



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
            





tab1,  tab2= st.tabs(['Tabela','Gráfico'])

var_show_filial =   db_resumo_por_filial.loc[
                    (db_resumo_por_filial['ANO'] == var_ano) & 
                    (db_resumo_por_filial['FILIAL'].isin(var_filial)) &
                    (db_resumo_por_filial['EMPRESA'].isin(var_empresa) )]

var_show_empresa =  db_resumo_por_filial.loc[
                    (db_resumo_por_filial['ANO'] == var_ano) & 
                    (db_resumo_por_filial['FILIAL'].isin(var_filial))]
    

with tab1:

        st.dataframe(var_show_filial,
               hide_index=True, use_container_width=True)

               
with tab2:
    
    
    with st.container():

        col1, col2= st.columns([1.2,3])


        with col1:
            chart_por_empresa = px.bar(var_show_empresa,x='EMPRESA',
                        y=['ESCOADO - VALOR','CARTEIRA - VALOR','VENDAS TO GO - CARTEIRA'], 
                        barmode='stack',color_discrete_sequence =['green','blue','grey'])
            chart_por_empresa.update_xaxes(tickangle=-90,categoryorder='category ascending',title=None).update_yaxes(title=None).update_layout(showlegend=False)

            #chart.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)

            st.plotly_chart(chart_por_empresa)

        with col2:
            chart_por_filial = px.bar(var_show_filial ,x='FILIAL',
                        y=['ESCOADO - VALOR','CARTEIRA - VALOR','VENDAS TO GO - CARTEIRA'], 
                        barmode='stack',color_discrete_sequence =['green','blue','grey'])
            chart_por_filial.update_xaxes(tickangle=-90,categoryorder='category ascending',title=None).update_yaxes(title=None).update_layout(showlegend=True)
            #chart.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
            
            st.plotly_chart(chart_por_filial)



  
#consolida_arquivos()
#print(db_consolidado.columns)

#print(consolida_arquivos())





