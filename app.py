#______________________________________________________________________________________________________________________

## IMPORTA BIBLIOTECAS PARA O PYTHON ##

import pandas as pd
import streamlit as st
import re
import os

#______________________________________________________________________________________________________________________

## INPUTS DA PÁGINA DO STREAMLIT ##

st.set_page_config(
     page_title="PMI - Confere processo ALF",
     page_icon=('./dados/favicon.png'),
 )

#______________________________________________________________________________________________________________________

## EXTRAI INFORMAÇÕES DO APROVA ##

# Input box do aprova
logo_image = ('./dados/logo.png')
st.sidebar.image(logo_image, width=200)
st.sidebar.subheader('Verificação do processo:')
texto_aprova = st.sidebar.text_input('CTRL+  V da página do APROVA:','',key="inputbox1")

if texto_aprova != "":
    #Separa o texto do aprova entre os trechos viabilidade e estabelecimento
    texto_aprova_split = re.sub(' +', ' ',texto_aprova).split(' ')
    #itens_analise=['Viabilidade','Estabelecimento','Bairro','Logradouro','Número','Social', 'Nome','PRINT']
    index_aprova1=texto_aprova_split.index('Selecione')
    index_aprova2=texto_aprova_split.index('Horário')
    
    ##Inscrição imobiliária no Aprova Digital
    
    inscricao_aprova = re.findall(r'\d\d\d.\d\d\d.\d\d.\d\d\d\d.\d\d\d\d.\d\d\d', texto_aprova)
    inscricao_aprova = inscricao_aprova[0]

    trecho_aprova = " ".join(texto_aprova_split[index_aprova1:index_aprova2])

    #Separa o texto do aprova em espaços para retornar a razão social
    itens_analise=['Razao','Horário']
    index_aprova3=texto_aprova_split.index('Razao')
    index_aprova4=texto_aprova_split.index('Horário')
    
    trecho_aprova_split2 = texto_aprova_split[index_aprova3:index_aprova4]
    itens_analise=['Social','Nome']
    index_aprova5=trecho_aprova_split2.index('Social')+1
    index_aprova6=trecho_aprova_split2.index('Nome')
    razao_social_aprova = " ".join(trecho_aprova_split2[index_aprova5:index_aprova6])
     

    #Separa o texto do aprova em espaços para retornar o endereço
    itens_analise=['REGIN','Razao']
    index_aprova7=texto_aprova_split.index('REGIN')
    index_aprova8=texto_aprova_split.index('Razao')
    trecho_aprova_split3 = texto_aprova_split[index_aprova7:index_aprova8]
    itens_analise=['Bairro','Logradouro']
    index_aprova9=trecho_aprova_split3.index('Bairro')+1
    index_aprova10=trecho_aprova_split3.index('Logradouro')
    index_aprova11=trecho_aprova_split3.index('Logradouro')+1
    index_aprova12=trecho_aprova_split3.index('Número')
    index_aprova13=trecho_aprova_split3.index('Predial')+1
    index_aprova14=trecho_aprova_split3.index('CEP')
    bairro_aprova = " ".join(trecho_aprova_split3[index_aprova9:index_aprova10])
    logradouro_aprova = " ".join(trecho_aprova_split3[index_aprova11:index_aprova12])
    numero_aprova = " ".join(trecho_aprova_split3[index_aprova13:index_aprova14])

    index_aprova17=trecho_aprova_split3.index('Sala)')
    index_aprova18=trecho_aprova_split3.index('(Sala)')
    index_aprova19=trecho_aprova_split3.index('(Box)')
    index_aprova20=trecho_aprova_split3.index('Telefone')
    complemento1_aprova = " ".join(trecho_aprova_split3[index_aprova17+1:index_aprova18-2])
    complemento2_aprova = " ".join(trecho_aprova_split3[index_aprova18+1:index_aprova19-2])
    complemento3_aprova = " ".join(trecho_aprova_split3[index_aprova19+1:index_aprova20])

    #Extrai as informações do trecho
    cnaes_aprova = re.findall(r'\d\d.\d\d-\d-\d\d', texto_aprova)
    cnaes_aprova=list(set(cnaes_aprova))

    itens_analise=['Razao','Horário']
    index_aprova15=texto_aprova_split.index('Razao')
    index_aprova16=texto_aprova_split.index('Horário')
    trecho_aprova_split4 = texto_aprova_split[index_aprova15:index_aprova16]
    trecho_aprova_cnpj = " ".join(trecho_aprova_split4)
    cnpj_aprova = re.findall(r'\d\d.\d\d\d.\d\d\d/\d\d\d\d-\d\d', trecho_aprova_cnpj)


else:
    cnpj_aprova =""       

#______________________________________________________________________________________________________________________

## EXTRAI INFORMAÇÕES DO CNPJ ##

# Input box do CNPJ
texto_cnpj = st.sidebar.text_input('CTRL + V do CNPJ:','',key="inputbox3")

if texto_cnpj != "":
    cnaes_cnpj = re.findall(r'\d\d.\d\d-\d-\d\d', texto_cnpj)
    cnae_principal_cnpj=cnaes_cnpj[0]
    numero_cnpj = re.findall(r'\d\d.\d\d\d.\d\d\d/\d\d\d\d-\d\d', texto_cnpj)
    texto_cnpj_split = re.sub(' +', ' ',texto_cnpj).split(' ')

    #Separa o cartão cnpj em elementos separado por espaços para extração de textos específicos
    itens_analise=['EMPRESARIAL','TÍTULO', 'LOGRADOURO','NÚMERO']
    index_cnpj1=texto_cnpj_split.index('EMPRESARIAL')+1
    index_cnpj2=texto_cnpj_split.index('TÍTULO')
    razao_social_cnpj = " ".join(texto_cnpj_split[index_cnpj1:index_cnpj2])

    #Separa o primeiro split para puxar o endereço
    index_cnpj3=texto_cnpj_split.index('NATUREZA')+1
    index_cnpj4=texto_cnpj_split.index('ESPECIAL')
    texto_cnpj_split2 = texto_cnpj_split[index_cnpj3:index_cnpj4] #função que separa o primeiro split
    
    index_cnpj5=texto_cnpj_split2.index('LOGRADOURO')+1
    index_cnpj6=texto_cnpj_split2.index('NÚMERO')
    logradouro_cnpj = " ".join(texto_cnpj_split2[index_cnpj5:index_cnpj6])
    
    index_cnpj7=texto_cnpj_split2.index('NÚMERO')+1
    index_cnpj8=texto_cnpj_split2.index('COMPLEMENTO')
    numeropredial_cnpj = " ".join(texto_cnpj_split2[index_cnpj7:index_cnpj8])
    
    index_cnpj9=texto_cnpj_split2.index('COMPLEMENTO')+1
    index_cnpj10=texto_cnpj_split2.index('CEP')
    complemento_cnpj = " ".join(texto_cnpj_split2[index_cnpj9:index_cnpj10])
    
    index_cnpj11=texto_cnpj_split2.index('BAIRRO/DISTRITO')+1
    index_cnpj12=texto_cnpj_split2.index('MUNICÍPIO')
    bairro_cnpj = " ".join(texto_cnpj_split2[index_cnpj11:index_cnpj12])
     
#_____________________________________________________________________________________________________________________

## BOTÃO LIMPAR ##

def clear_text():
    st.session_state["inputbox1"] = ""
    st.session_state["inputbox2"] = ""
    st.session_state["inputbox3"] = ""
    st.session_state["inputbox4"] = ""
st.sidebar.button("Limpar", on_click=clear_text)

     
#_____________________________________________________________________________________________________________________

## ESTRUTURA PAGINA VERIFICAÇÃO DE PROCESSOS ##

st.title('Confere processos ALF')
if (texto_aprova) == '':
     st.markdown(str('<<< Copie e cole as informações na barra lateral esquerda.'))
     
#_____________________________________________________________________________________________________________________
 
## PÁGINA - CONFERÊNCIA DO PROCESSO ##

try:
    if texto_aprova != "":
        #Printa o resumo do processo
        st.text('____________________________________________________________________________________________________________')
        st.subheader('Resumo do processo')
        st.text('RAZÃO SOCIAL: '+razao_social_aprova+', CNPJ: '+cnpj_aprova[0])
        st.text(logradouro_cnpj+', '+bairro_cnpj+', '+numeropredial_cnpj+', '+complemento_cnpj)
        st.text('INSCRIÇÃO IMOBILIÁRIA: '+str(inscricao_aprova[0:15]))
        endereço_split = re.sub(' +', ' ',logradouro_aprova).split(' ')
        logradouro_google = "+".join(endereço_split)
        st.markdown('MAPS: '+str('https://www.google.com/maps/place/')+logradouro_google+str(',+')+str(numero_aprova)+str('+,+Itaja%C3%AD+-+SC'))
        
        #Printa a verificação do cnpj
        st.text('____________________________________________________________________________________________________________')
        st.subheader('Verificação do CNPJ')

        if (numero_cnpj[0] == cnpj_aprova[0]):
            st.text('Ok! Número CNPJ inserido corretamente no Aprova.')
        else:
            st.text('VERIFICAR! Número CNPJ NÃO coincide')

        #Printa a verificação da razão social
        st.text('____________________________________________________________________________________________________________')
        st.subheader('Verificação da RAZÃO SOCIAL')
        if (razao_social_cnpj == razao_social_aprova.upper()):
            st.text('Ok! A razão social inserida corretamento no Aprova.')
        else:
            st.text('VERIFICAR! A razão social NÃO coincide com o Aprova.')
                
        #Printa a verificação do endereço
        st.text('____________________________________________________________________________________________________________')
        st.subheader('Verificação do ENDEREÇO')
        st.text('** Verifique manualmente os endereços abaixo:')
        st.text('Endereço no APROVA: '+logradouro_aprova+', '+bairro_aprova+', '+numero_aprova+', '+complemento1_aprova+', '+complemento2_aprova+', '+complemento3_aprova)
        st.text('Endereço no CNPJ: '+logradouro_cnpj+', '+bairro_cnpj+', '+numeropredial_cnpj+', '+complemento_cnpj)

        #Printa a verificação dos cnaes
        st.text('____________________________________________________________________________________________________________')
        st.subheader('Verificação dos CNAES')


        if (set(cnaes_cnpj) == set(cnaes_aprova)):
             st.text('Conferência dos CNAEs do CNPJ com o APROVA: Ok! CNAES coincidem.')
        else:
            st.text('Conferência dos CNAEs do CNPJ com o APROVA: VERIFICAR! CNAES não coincidem.')
                
      
        st.text('ATENÇÃO! Verifique manualmente se não houve inserção REPETIDA de CNAES no Aprova Digital. Abaixo o número de atividades por valores únicos (exclui repetidos)')
        nome_contagem = pd.Series(['Aprova Digital', 'Cartão CNPJ'])      
        n_cnaes=([len(cnaes_aprova),len(cnaes_cnpj)
        st.dataframe({'LOCAL':nome_contagem,'Nº DE CNAES':n_cnaes})

            
        if (set(cnaes_cnpj) == set(cnaes_aprova)):
            st.text('TABELA DE CNAES')
            tabela_cnaes = pd.DataFrame({ 'CNAES APROVA': cnaes_aprova, 'CNAES CNPJ': cnaes_cnpj })
            st.dataframe(tabela_cnaes)
        else:
            st.text('   ** CNAE principal: '+cnaes_cnpj[0])
            st.text('   ** CNAES não inseridos no APROVA: '+str(set(cnaes_cnpj)-set(cnaes_aprova)))
            verif_cnaes = set(cnaes_aprova)-set(cnaes_cnpj)
            if verif_cnaes == set():
                verif_cnaes = ""
            st.text('   ** CNAES inseridos no APROVA que não estão no CNPJ: '+str(verif_cnaes))
            st.text('CNAES do APROVA')
            st.dataframe(cnaes_aprova)
            st.text('CNAES do CNPJ')
            st.dataframe(cnaes_cnpj)
            
        #Printa outras verificações
        st.text('____________________________________________________________________________________________________________')
        st.subheader('Verificação de documentos complementares')
        
        #Tabelas com CNAES
        
        tabela_cnaes = pd.read_csv('./dados/grau_risco_maio_2021.xlsx - Página2.csv', sep=',')       
        cnaes_cnpj = pd.DataFrame(cnaes_cnpj)
        
        nova_tabela=tabela_cnaes.merge(cnaes_cnpj,left_on='codigo', right_on=0)
        nova_tabela.drop([0], axis=1, inplace=True)
        nova_tabela
        
        #Verificação armas de fogo
        
        cnae1 = '47.89-0-09'
        if cnae1 in cnaes_aprova:
            st.text('*** APRESENTA CNAE para comércio de ARMAS DE FOGO, solicitar documentação extra.')
        if cnae1 not in cnaes_aprova:
            st.text('*** NÃO apresenta CNAE para comércio de armas de fogo.')     
            
        #Verificação SPE
        
        cnae2 = '41.10-7-00'      
        cnae3 = '41.20-4-00'
        
        if (cnae2 or cnae3) in cnaes_aprova:
           st.text('*** APRESENTA CNAE para construção ou incorporação, verificar se é uma SPE.')
        if (cnae2 or cnae3) not in cnaes_aprova:
           st.text('*** NÃO apresenta CNAE para incorporação imobiliária ou construção (SPE).')

        #Verificação transporte escolar
        
        cnae4 = '49.24-8-00'
        if cnae4 in cnaes_cnpj:
            st.text('*** APRESENTA CNAE para TRANSPORTE ESCOLAR, solicitar documentação extra.')
        if cnae4 not in cnaes_cnpj:
            st.text('*** NÃO apresenta CNAE para transporte escolar.')
            
        #Verificação transporte por cabotagem
        cnae5 = '50.11-4-02'
        if cnae5 in cnaes_cnpj:
            st.text('*** APRESENTA CNAE para transporte por CABOTAGEM, solicitar autorização da ANTAC.')
        if cnae5 not in cnaes_cnpj:
            st.text('*** NÃO apresenta CNAE para transporte de cabotagem.')
               
        #Printa outras verificações
        st.text('____________________________________________________________________________________________________________')
        st.subheader('Verificação do grau de risco')
     
        tabela_risco = pd.read_csv('./dados/Decreto 11.985 - Grau de risco.csv', sep=',')
          
        cnaes_cnpj = pd.DataFrame(cnaes_cnpj)        
        nova_tabela3=tabela_risco.merge(cnaes_cnpj,left_on='CÓDIGO', right_on=0)
        nova_tabela3.drop([0], axis=1, inplace=True)
        nova_tabela3
     
        
        
except:
  pass
