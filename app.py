import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from psychrometric_functions import *
from psychrometric_processes import *
from psychrometric_chart import plot_psychrometric_chart

# Função para mostrar as referências
def show_references():
    st.markdown("## [Referências](https://evandro.eng.br/grapsi-artigos)")
    st.markdown("""
    - Melo et al. GRAPSI -Programa Computacional para o Cálculo das Propriedades Psicrométricas do Ar. Engenharia na Agricultura, Viçosa, MG, v.12, n.2, 154-162, Abr./Jun., 2004.
    - Melo, E.C. O Programa Computacional GRAPSI. Edição do autor. 2011.
    """)

# Set page config
st.set_page_config(
    page_title="Grapsi - Cálculos Psicométricos",
    page_icon="🌡️",
    layout="wide"
)

# Add title and description to main content area
st.title("GRAPSI - Gráfico Psicrométrico Digital")
st.markdown("""
GRAPSI é um aplicativo que calcula as propriedades psicrométricas do ar úmido e as exibe em um gráfico na tela do computador. 
Ele pode simular processos como aquecimento, resfriamento, umidificação adiabática e mistura de fluxos de ar. 
O programa opera em uma ampla faixa de temperaturas, de -100 a 372 ºC, e altitudes de até 4.000 metros.
""")

# Initialize session state variables if they don't exist
if 'patm' not in st.session_state:
    st.session_state.patm = 101.325  # Default pressure in kPa
    
if 'results' not in st.session_state:
    st.session_state.results = None
    
if 'process_results' not in st.session_state:
    st.session_state.process_results = None
    
if 'chart_data' not in st.session_state:
    st.session_state.chart_data = None

# Sidebar for navigation
with st.sidebar:
    st.title("GRAPSI")
    st.header("Opções de Entrada")
    
    page = st.radio(
        "Selecione o tipo de cálculo:",
        ["Ponto de Estado", "Processos Psicrométricos", "Mistura de Fluxos de Ar"]
    )
    
    # Altitude input in sidebar
    altitude = st.number_input("Altitude do Local (m)", min_value=0.0, value=0.0, step=10.0)
    
    # Automatic pressure calculation
    a = 2.2556e-5
    b = 5.2559
    calculated_patm = 101.324 * (1 - a * altitude) ** b
    st.info(f"Pressão atmosférica: {calculated_patm:.2f} kPa")
    
    # Atualizar a pressão na sessão
    st.session_state.patm = calculated_patm
    patm = st.session_state.patm
    
    # Adicionar informações do autor
    st.markdown("---")
    st.markdown("Evandro de Castro Melo")
    st.markdown("[web page](https://evandro.eng.br)")

# Main content area - Header for the selected calculation type
st.header("Dados de Entrada")

# Main content area based on the selected page
if page == "Ponto de Estado":
    st.subheader("Cálculo do Ponto de Estado")
    
    # Type of calculation
    calc_type = st.selectbox(
        "Selecione o método de cálculo:",
        ["TBS e UR", "TBS e TBM", "TBS e TPO"]
    )
    
    # Create two columns
    col1, col2 = st.columns(2)
    
    with col1:
        # Forms for each calculation type
        if calc_type == "TBS e UR":
            with st.form("tbs_ur_form"):
                tbs = st.number_input("Temperatura de bulbo seco (°C)", value=25.0, step=0.1)
                ur = st.number_input("Umidade relativa (%)", value=50.0, min_value=0.0, max_value=100.0, step=0.1)
                submit = st.form_submit_button("Calcular")
                
                if submit:
                    ur_decimal = ur / 100.0
                    if ur_decimal >= 1.0:
                        ur_decimal = 0.99999
                    
                    # Call the calculation function
                    result = calculate_from_tbs_ur(tbs, ur_decimal, patm)
                    st.session_state.results = result
                    
                    # Passar informações completas para o gráfico
                    pv = result['pv']  # Pressão parcial de vapor
                    rm = result['rm'] / 1000.0  # Convertendo g/kg para kg/kg (decimal)
                    st.session_state.chart_data = {
                        'type': 'point', 
                        'tbs': tbs, 
                        'tbm': result['tbm'],
                        'pv': pv,
                        'rm': rm
                    }
        
        elif calc_type == "TBS e TBM":
            with st.form("tbs_tbm_form"):
                tbs = st.number_input("Temperatura de bulbo seco (°C)", value=25.0, step=0.1)
                tbm = st.number_input("Temperatura de bulbo molhado (°C)", value=20.0, step=0.1)
                submit = st.form_submit_button("Calcular")
                
                if submit:
                    # Call the calculation function
                    result = calculate_from_tbs_tbm(tbs, tbm, patm)
                    st.session_state.results = result
                    
                    # Passar informações completas para o gráfico
                    pv = result['pv']  # Pressão parcial de vapor
                    rm = result['rm'] / 1000.0  # Convertendo g/kg para kg/kg (decimal)
                    st.session_state.chart_data = {
                        'type': 'point', 
                        'tbs': tbs, 
                        'tbm': tbm,
                        'pv': pv,
                        'rm': rm
                    }
        
        elif calc_type == "TBS e TPO":
            with st.form("tbs_tpo_form"):
                tbs = st.number_input("Temperatura de bulbo seco (°C)", value=25.0, step=0.1)
                tpo = st.number_input("Temperatura do ponto de orvalho (°C)", value=15.0, step=0.1)
                submit = st.form_submit_button("Calcular")
                
                if submit:
                    # Call the calculation function
                    result = calculate_from_tbs_tpo(tbs, tpo, patm)
                    st.session_state.results = result
                    
                    # Passar informações completas para o gráfico
                    pv = result['pv']  # Pressão parcial de vapor
                    rm = result['rm'] / 1000.0  # Convertendo g/kg para kg/kg (decimal)
                    st.session_state.chart_data = {
                        'type': 'point', 
                        'tbs': tbs, 
                        'tbm': result['tbm'],
                        'pv': pv,
                        'rm': rm
                    }
    
    # Display results in the second column
    with col2:
        if st.session_state.results:
            st.subheader("Resultados:")
            
            # Format the results in a nice table
            results = st.session_state.results
            df = pd.DataFrame({
                'Propriedade': [
                    'Temperatura de Bulbo Seco (°C)',
                    'Temperatura de Bulbo Molhado (°C)',
                    'Temperatura de Ponto de Orvalho (°C)',
                    'Umidade Relativa (%)',
                    'Razão de Mistura (g/kg)',
                    'Pressão de Vapor Saturado (kPa)',
                    'Pressão Parcial de Vapor (kPa)',
                    'Volume Específico (m³/kg)',
                    'Entalpia (kJ/kg)'
                ],
                'Valor': [
                    f"{results['tbs']:.2f}",
                    f"{results['tbm']:.2f}",
                    f"{results['tpo']:.2f}",
                    f"{results['ur']:.2f}",
                    f"{results['rm']:.2f}",
                    f"{results['pvs']:.4f}",
                    f"{results['pv']:.4f}",
                    f"{results['ve']:.4f}",
                    f"{results['e']:.2f}"
                ]
            })
            
            st.table(df)
    
    # Plot psychrometric chart
    if st.session_state.chart_data:
        st.subheader("Carta Psicrométrica")
        fig = plot_psychrometric_chart(st.session_state.chart_data, patm)
        st.pyplot(fig)
        
        # Referências
        st.markdown("## [Referências](https://evandro.eng.br/grapsi-artigos)")
        st.markdown("""
        - Melo et al. GRAPSI -Programa Computacional para o Cálculo das Propriedades Psicrométricas do Ar. Engenharia na Agricultura, Viçosa, MG, v.12, n.2, 154-162, Abr./Jun., 2004.
        - Melo, E.C. O Programa Computacional GRAPSI. Edição do autor. 2011.
        """)

elif page == "Processos Psicrométricos":
    st.subheader("Cálculo de Processos Psicrométricos")
    
    # Type of process
    process_type = st.selectbox(
        "Selecione o tipo de processo:",
        ["Aquecimento/Resfriamento", 
         "Umidificação Adiabática (TBS)", 
         "Umidificação Adiabática (UR)",
         "Umidificação Adiabática (RM)"]
    )
    
    # Create two columns
    col1, col2 = st.columns(2)
    
    with col1:
        # Forms for each process type
        if process_type == "Aquecimento/Resfriamento":
            with st.form("aquece_resfria_form"):
                st.subheader("Ponto de Estado 1")
                tbs1 = st.number_input("Temperatura de bulbo seco (°C)", value=25.0, step=0.1, key="tbs1_aq")
                ur1 = st.number_input("Umidade relativa (%)", value=50.0, min_value=0.0, max_value=100.0, step=0.1, key="ur1_aq")
                
                st.subheader("Ponto de Estado 2")
                tbs2 = st.number_input("Temperatura de bulbo seco (°C)", value=35.0, step=0.1, key="tbs2_aq")
                
                submit = st.form_submit_button("Calcular")
                
                if submit:
                    # Call the calculation function
                    result = calculate_aquece_resfria(tbs1, ur1/100.0, tbs2, patm)
                    st.session_state.process_results = result
                    st.session_state.chart_data = {
                        'type': 'process',
                        'process': 'aquece_resfria',
                        'tbs1': tbs1,
                        'tbm1': result['point1']['tbm'],
                        'tbs2': tbs2,
                        'tbm2': result['point2']['tbm'],
                        'process_results': result
                    }
        
        elif process_type == "Umidificação Adiabática (TBS)":
            with st.form("u_adiabatica_tbs_form"):
                st.subheader("Ponto de Estado 1")
                tbs1 = st.number_input("Temperatura de bulbo seco (°C)", value=30.0, step=0.1, key="tbs1_ua")
                ur1 = st.number_input("Umidade relativa (%)", value=30.0, min_value=0.0, max_value=100.0, step=0.1, key="ur1_ua")
                
                st.subheader("Ponto de Estado 2")
                tbs2 = st.number_input("Temperatura de bulbo seco (°C)", value=25.0, step=0.1, key="tbs2_ua")
                
                submit = st.form_submit_button("Calcular")
                
                if submit:
                    # Call the calculation function
                    result = calculate_u_adiabatica_tbs(tbs1, ur1/100.0, tbs2, patm)
                    st.session_state.process_results = result
                    st.session_state.chart_data = {
                        'type': 'process',
                        'process': 'u_adiabatica',
                        'tbs1': tbs1,
                        'tbm1': result['point1']['tbm'],
                        'tbs2': tbs2,
                        'tbm2': result['point2']['tbm'],
                        'process_results': result
                    }
        
        elif process_type == "Umidificação Adiabática (UR)":
            with st.form("u_adiabatica_ur_form"):
                st.subheader("Ponto de Estado 1")
                tbs1 = st.number_input("Temperatura de bulbo seco (°C)", value=30.0, step=0.1, key="tbs1_ua_ur")
                ur1 = st.number_input("Umidade relativa (%)", value=30.0, min_value=0.0, max_value=100.0, step=0.1, key="ur1_ua_ur")
                
                st.subheader("Ponto de Estado 2")
                ur2 = st.number_input("Umidade relativa (%)", value=80.0, min_value=0.0, max_value=100.0, step=0.1, key="ur2_ua")
                
                submit = st.form_submit_button("Calcular")
                
                if submit:
                    # Call the calculation function
                    result = calculate_u_adiabatica_ur(tbs1, ur1/100.0, ur2/100.0, patm)
                    st.session_state.process_results = result
                    st.session_state.chart_data = {
                        'type': 'process',
                        'process': 'u_adiabatica',
                        'tbs1': tbs1,
                        'tbm1': result['point1']['tbm'],
                        'tbs2': result['point2']['tbs'],
                        'tbm2': result['point2']['tbm'],
                        'process_results': result
                    }
                    
        elif process_type == "Umidificação Adiabática (RM)":
            with st.form("u_adiabatica_rm_form"):
                st.subheader("Ponto de Estado 1")
                tbs1 = st.number_input("Temperatura de bulbo seco (°C)", value=30.0, step=0.1, key="tbs1_ua_rm")
                rm1 = st.number_input("Razão de mistura (g/kg)", value=10.0, min_value=0.0, step=0.1, key="rm1_ua")
                
                st.subheader("Ponto de Estado 2")
                rm2 = st.number_input("Razão de mistura (g/kg)", value=16.0, min_value=0.0, step=0.1, key="rm2_ua")
                
                submit = st.form_submit_button("Calcular")
                
                if submit:
                    # Call the calculation function
                    result = calculate_u_adiabatica_rm(tbs1, rm1, rm2, patm)
                    st.session_state.process_results = result
                    st.session_state.chart_data = {
                        'type': 'process',
                        'process': 'u_adiabatica',
                        'tbs1': tbs1,
                        'tbm1': result['point1']['tbm'],
                        'tbs2': result['point2']['tbs'],
                        'tbm2': result['point2']['tbm'],
                        'process_results': result
                    }
    
    # Display results in the second column
    with col2:
        if st.session_state.process_results:
            results = st.session_state.process_results
            
            # Point 1
            st.subheader("Ponto de Estado 1:")
            df1 = pd.DataFrame({
                'Propriedade': [
                    'Temperatura de Bulbo Seco (°C)',
                    'Temperatura de Bulbo Molhado (°C)',
                    'Temperatura de Ponto de Orvalho (°C)',
                    'Umidade Relativa (%)',
                    'Razão de Mistura (g/kg)',
                    'Pressão de Vapor Saturado (kPa)',
                    'Pressão Parcial de Vapor (kPa)',
                    'Volume Específico (m³/kg)',
                    'Entalpia (kJ/kg)'
                ],
                'Valor': [
                    f"{results['point1']['tbs']:.2f}",
                    f"{results['point1']['tbm']:.2f}",
                    f"{results['point1']['tpo']:.2f}",
                    f"{results['point1']['ur']:.2f}",
                    f"{results['point1']['rm']:.2f}",
                    f"{results['point1']['pvs']:.4f}",
                    f"{results['point1']['pv']:.4f}",
                    f"{results['point1']['ve']:.4f}",
                    f"{results['point1']['e']:.2f}"
                ]
            })
            
            st.table(df1)
            
            # Point 2
            st.subheader("Ponto de Estado 2:")
            df2 = pd.DataFrame({
                'Propriedade': [
                    'Temperatura de Bulbo Seco (°C)',
                    'Temperatura de Bulbo Molhado (°C)',
                    'Temperatura de Ponto de Orvalho (°C)',
                    'Umidade Relativa (%)',
                    'Razão de Mistura (g/kg)',
                    'Pressão de Vapor Saturado (kPa)',
                    'Pressão Parcial de Vapor (kPa)',
                    'Volume Específico (m³/kg)',
                    'Entalpia (kJ/kg)'
                ],
                'Valor': [
                    f"{results['point2']['tbs']:.2f}",
                    f"{results['point2']['tbm']:.2f}",
                    f"{results['point2']['tpo']:.2f}",
                    f"{results['point2']['ur']:.2f}",
                    f"{results['point2']['rm']:.2f}",
                    f"{results['point2']['pvs']:.4f}",
                    f"{results['point2']['pv']:.4f}",
                    f"{results['point2']['ve']:.4f}",
                    f"{results['point2']['e']:.2f}"
                ]
            })
            
            st.table(df2)
    
    # Plot psychrometric chart
    if st.session_state.chart_data and st.session_state.chart_data['type'] == 'process':
        st.subheader("Carta Psicrométrica")
        fig = plot_psychrometric_chart(st.session_state.chart_data, patm)
        st.pyplot(fig)
        
        # Referências
        st.markdown("## [Referências](https://evandro.eng.br/grapsi-artigos)")
        st.markdown("""
        - Melo et al. GRAPSI -Programa Computacional para o Cálculo das Propriedades Psicrométricas do Ar. Engenharia na Agricultura, Viçosa, MG, v.12, n.2, 154-162, Abr./Jun., 2004.
        - Melo, E.C. O Programa Computacional GRAPSI. Edição do autor. 2011.
        """)

elif page == "Mistura de Fluxos de Ar":
    st.subheader("Cálculo de Mistura de Fluxos de Ar")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.form("mistura_fluxos_form"):
            st.subheader("Fluxo de Ar 1")
            tbs1 = st.number_input("Temperatura de bulbo seco (°C)", value=30.0, step=0.1, key="tbs1_mix")
            ur1 = st.number_input("Umidade relativa (%)", value=40.0, min_value=0.0, max_value=100.0, step=0.1, key="ur1_mix")
            q1 = st.number_input("Vazão de ar (m³/h)", value=100.0, min_value=0.0, step=10.0, key="q1_mix")
            
            st.subheader("Fluxo de Ar 2")
            tbs2 = st.number_input("Temperatura de bulbo seco (°C)", value=20.0, step=0.1, key="tbs2_mix")
            ur2 = st.number_input("Umidade relativa (%)", value=60.0, min_value=0.0, max_value=100.0, step=0.1, key="ur2_mix")
            q2 = st.number_input("Vazão de ar (m³/h)", value=50.0, min_value=0.0, step=10.0, key="q2_mix")
            
            submit = st.form_submit_button("Calcular")
            
            if submit:
                # Call the calculation function
                result = calculate_mistura_fluxos(tbs1, ur1/100.0, q1, tbs2, ur2/100.0, q2, patm)
                st.session_state.process_results = result
                st.session_state.chart_data = {
                    'type': 'mixing',
                    'tbs1': tbs1,
                    'tbm1': result['point1']['tbm'],
                    'tbs2': tbs2,
                    'tbm2': result['point2']['tbm'],
                    'tbs3': result['point3']['tbs'],
                    'tbm3': result['point3']['tbm'],
                    'process_results': result
                }
    
    # Display results
    with col2:
        if st.session_state.process_results and len(st.session_state.process_results) >= 3:
            results = st.session_state.process_results
            
            # Uma única tabela com os três fluxos lado a lado
            st.subheader("Resultados da Mistura de Fluxos de Ar:")
            
            df_combined = pd.DataFrame({
                'Propriedade': [
                    'TBS (°C)',
                    'TBM (°C)',
                    'TPO (°C)',
                    'UR (%)',
                    'RM (g/kg)',
                    'PVS (kPa)',
                    'PV (kPa)',
                    'VE (m³/kg)',
                    'h (kJ/kg)',
                    'Q (m³/h)'
                ],
                'Fluxo 1': [
                    f"{results['point1']['tbs']:.2f}",
                    f"{results['point1']['tbm']:.2f}",
                    f"{results['point1']['tpo']:.2f}",
                    f"{results['point1']['ur']:.2f}",
                    f"{results['point1']['rm']:.2f}",
                    f"{results['point1']['pvs']:.4f}",
                    f"{results['point1']['pv']:.4f}",
                    f"{results['point1']['ve']:.4f}",
                    f"{results['point1']['e']:.2f}",
                    f"{results['q1']:.2f}"
                ],
                'Fluxo 2': [
                    f"{results['point2']['tbs']:.2f}",
                    f"{results['point2']['tbm']:.2f}",
                    f"{results['point2']['tpo']:.2f}",
                    f"{results['point2']['ur']:.2f}",
                    f"{results['point2']['rm']:.2f}",
                    f"{results['point2']['pvs']:.4f}",
                    f"{results['point2']['pv']:.4f}",
                    f"{results['point2']['ve']:.4f}",
                    f"{results['point2']['e']:.2f}",
                    f"{results['q2']:.2f}"
                ],
                'Fluxo M': [
                    f"{results['point3']['tbs']:.2f}",
                    f"{results['point3']['tbm']:.2f}",
                    f"{results['point3']['tpo']:.2f}",
                    f"{results['point3']['ur']:.2f}",
                    f"{results['point3']['rm']:.2f}",
                    f"{results['point3']['pvs']:.4f}",
                    f"{results['point3']['pv']:.4f}",
                    f"{results['point3']['ve']:.4f}",
                    f"{results['point3']['e']:.2f}",
                    f"{results['q3']:.2f}"
                ]
            })
            
            st.table(df_combined)
    
    # Plot psychrometric chart
    if st.session_state.chart_data and st.session_state.chart_data['type'] == 'mixing':
        st.subheader("Carta Psicrométrica")
        fig = plot_psychrometric_chart(st.session_state.chart_data, patm)
        st.pyplot(fig)
        
        # Referências
        st.markdown("## [Referências](https://evandro.eng.br/grapsi-artigos)")
        st.markdown("""
        - Melo et al. GRAPSI -Programa Computacional para o Cálculo das Propriedades Psicrométricas do Ar. Engenharia na Agricultura, Viçosa, MG, v.12, n.2, 154-162, Abr./Jun., 2004.
        - Melo, E.C. O Programa Computacional GRAPSI. Edição do autor. 2011.
        """)