import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
from psychrometric_functions import *
from psychrometric_processes import *
from psychrometric_chart import plot_psychrometric_chart
from translations import get_text

# Função para mostrar as referências
def show_references(lang='pt'):
    st.markdown(f"## [{get_text('references', lang)}](https://evandro.eng.br/grapsi-artigos)")
    st.markdown(get_text('references_content', lang))

# Set page config
st.set_page_config(
    page_title="Grapsi - Cálculos Psicométricos",
    page_icon="🌡️",
    layout="wide"
)

# Get language setting (before we use it in the title)
if 'language' not in st.session_state:
    st.session_state.language = 'pt'  # Default to Portuguese
    
# Add title and description to main content area
st.title(get_text('app_title', st.session_state.language))
st.markdown(get_text('app_description', st.session_state.language))

# Initialize session state variables if they don't exist
if 'patm' not in st.session_state:
    st.session_state.patm = 101.325  # Default pressure in kPa
    
if 'results' not in st.session_state:
    st.session_state.results = None
    
if 'process_results' not in st.session_state:
    st.session_state.process_results = None
    
if 'chart_data' not in st.session_state:
    st.session_state.chart_data = None
    
# Initialize language preference
if 'language' not in st.session_state:
    st.session_state.language = 'pt'  # Default to Portuguese

# Sidebar for navigation
with st.sidebar:
    st.title(get_text('sidebar_title', st.session_state.language))
    st.header(get_text('input_options', st.session_state.language))
    
    page_options = {
        'pt': [
            get_text('state_point', 'pt'),
            get_text('psychrometric_processes', 'pt'),
            get_text('air_flow_mixing', 'pt')
        ],
        'en': [
            get_text('state_point', 'en'),
            get_text('psychrometric_processes', 'en'),
            get_text('air_flow_mixing', 'en')
        ],
        'es': [
            get_text('state_point', 'es'),
            get_text('psychrometric_processes', 'es'),
            get_text('air_flow_mixing', 'es')
        ]
    }
    
    page = st.radio(
        get_text('select_calculation', st.session_state.language),
        page_options[st.session_state.language]
    )
    
    # Altitude input in sidebar
    altitude = st.number_input(
        get_text('site_altitude', st.session_state.language), 
        min_value=0.0, value=0.0, step=10.0
    )
    
    # Automatic pressure calculation
    a = 2.2556e-5
    b = 5.2559
    calculated_patm = 101.324 * (1 - a * altitude) ** b
    st.info(get_text('atm_pressure', st.session_state.language, pressure=calculated_patm))
    
    # Atualizar a pressão na sessão
    st.session_state.patm = calculated_patm
    patm = st.session_state.patm
    
    # Seletor de idioma
    st.markdown("---")
    st.subheader(get_text("language", st.session_state.language))
    language_options = {
        'pt': get_text('portuguese', st.session_state.language),
        'en': get_text('english', st.session_state.language),
        'es': get_text('spanish', st.session_state.language)
    }
    
    # Determinar o índice correto com base no idioma atual
    language_index = 0  # Default para português
    if st.session_state.language == 'en':
        language_index = 1
    elif st.session_state.language == 'es':
        language_index = 2
    
    selected_language = st.selectbox(
        get_text('select_language', st.session_state.language),
        options=list(language_options.keys()),
        format_func=lambda x: language_options[x],
        index=language_index
    )
    
    # Atualizar idioma na sessão se for alterado
    if selected_language != st.session_state.language:
        st.session_state.language = selected_language
        st.rerun()  # Recarregar a página com o novo idioma
    
    # Adicionar informações do autor
    st.markdown("---")
    st.markdown(get_text('author_info', st.session_state.language))
    st.markdown(get_text('author_website', st.session_state.language))

# Main content area - Header for the selected calculation type
st.header(get_text('data_input', st.session_state.language))

# Main content area based on the selected page
if page == get_text('state_point', st.session_state.language):
    st.subheader(get_text('state_point_calc', st.session_state.language))
    
    # Type of calculation
    calc_options = {
        'pt': [
            "TBS e UR", "TBS e TBM", "TBS e TPO"
        ],
        'en': [
            "DBT and RH", "DBT and WBT", "DBT and DPT"
        ],
        'es': [
            "TBS y HR", "TBS y TBH", "TBS y TPR"
        ]
    }
    
    calc_type_label = get_text('select_calculation_method', st.session_state.language)
    calc_type = st.selectbox(
        calc_type_label,
        calc_options[st.session_state.language]
    )
    
    # Create two columns
    col1, col2 = st.columns(2)
    
    with col1:
        # Forms for each calculation type
        if calc_type == "TBS e UR" or calc_type == "DBT and RH" or calc_type == "TBS y HR":
            with st.form("tbs_ur_form"):
                tbs = st.number_input(get_text('dry_bulb_temp', st.session_state.language), value=25.0, step=0.1)
                ur = st.number_input(get_text('relative_humidity', st.session_state.language), value=50.0, min_value=0.0, max_value=100.0, step=0.1)
                submit = st.form_submit_button(get_text('calculate', st.session_state.language))
                
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
        
        elif calc_type == "TBS e TBM" or calc_type == "DBT and WBT" or calc_type == "TBS y TBH":
            with st.form("tbs_tbm_form"):
                tbs = st.number_input(get_text('dry_bulb_temp', st.session_state.language), value=25.0, step=0.1)
                tbm = st.number_input(get_text('wet_bulb_temp', st.session_state.language), value=20.0, step=0.1)
                submit = st.form_submit_button(get_text('calculate', st.session_state.language))
                
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
        
        elif calc_type == "TBS e TPO" or calc_type == "DBT and DPT" or calc_type == "TBS y TPR":
            with st.form("tbs_tpo_form"):
                tbs = st.number_input(get_text('dry_bulb_temp', st.session_state.language), value=25.0, step=0.1)
                tpo = st.number_input(get_text('dew_point_temp', st.session_state.language), value=15.0, step=0.1)
                submit = st.form_submit_button(get_text('calculate', st.session_state.language))
                
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
            st.subheader(get_text('results', st.session_state.language))
            
            # Format the results in a nice table
            results = st.session_state.results
            df = pd.DataFrame({
                get_text('property', st.session_state.language): [
                    get_text('dbt_long', st.session_state.language),
                    get_text('wbt_long', st.session_state.language),
                    get_text('dpt_long', st.session_state.language),
                    get_text('rh_long', st.session_state.language),
                    get_text('mr_long', st.session_state.language),
                    get_text('svp_long', st.session_state.language),
                    get_text('vp_long', st.session_state.language),
                    get_text('sv_long', st.session_state.language),
                    get_text('enthalpy_long', st.session_state.language)
                ],
                get_text('value', st.session_state.language): [
                    f"{results['tbs']:.2f}",
                    f"{results['tbm']:.2f}",
                    f"{results['tpo']:.2f}",
                    f"{results['ur']:.2f}",
                    f"{results['rm']:.2f}",
                    f"{results['pvs']:.2f}",
                    f"{results['pv']:.2f}",
                    f"{results['ve']:.3f}",
                    f"{results['e']:.2f}"
                ]
            })
            
            st.table(df)
    
    # Plot psychrometric chart
    if st.session_state.chart_data:
        st.subheader(get_text('psychrometric_chart', st.session_state.language))
        
        # Gráfico Matplotlib estático
        fig = plot_psychrometric_chart(st.session_state.chart_data, patm, altitude, st.session_state.language)
        st.pyplot(fig)
        
        # Mostrar referências
        show_references(st.session_state.language)

elif page == get_text('psychrometric_processes', st.session_state.language):
    st.subheader(get_text('process_calc', st.session_state.language))
    
    # Type of process
    process_options = {
        'pt': [
            "Aquecimento/Resfriamento", 
            "Umidificação Adiabática (dado UR ponto 2)",
            "Umidificação Adiabática (dado RM ponto 2)"
        ],
        'en': [
            "Heating/Cooling", 
            "Adiabatic Humidification (RH point 2)",
            "Adiabatic Humidification (MR point 2)"
        ],
        'es': [
            "Calentamiento/Enfriamiento", 
            "Humidificación Adiabática (HR punto 2)",
            "Humidificación Adiabática (RM punto 2)"
        ]
    }
    
    process_type = st.selectbox(
        get_text('select_process', st.session_state.language),
        process_options[st.session_state.language]
    )
    
    # Create two columns
    col1, col2 = st.columns(2)
    
    with col1:
        # Forms for each process type
        if process_type == "Aquecimento/Resfriamento" or process_type == "Heating/Cooling" or process_type == "Calentamiento/Enfriamiento":
            with st.form("aquece_resfria_form"):
                st.subheader(get_text('state_point_1', st.session_state.language))
                tbs1 = st.number_input(get_text('dry_bulb_temp', st.session_state.language), value=25.0, step=0.1, key="tbs1_aq")
                ur1 = st.number_input(get_text('relative_humidity', st.session_state.language), value=50.0, min_value=0.0, max_value=100.0, step=0.1, key="ur1_aq")
                
                st.subheader(get_text('state_point_2', st.session_state.language))
                tbs2 = st.number_input(get_text('dry_bulb_temp', st.session_state.language), value=35.0, step=0.1, key="tbs2_aq")
                
                submit = st.form_submit_button(get_text('calculate', st.session_state.language))
                
                if submit:
                    # Call the calculation function
                    result = calculate_aquece_resfria(tbs1, ur1/100.0, tbs2, patm)
                    st.session_state.process_results = result
                    st.session_state.chart_data = {
                        'type': 'process',
                        'process': 'aquece_resfria',
                        'process_type': 'heating_cooling',  # Identificador para o tipo de processo
                        'tbs1': tbs1,
                        'tbm1': result['point1']['tbm'],
                        'tbs2': tbs2,
                        'tbm2': result['point2']['tbm'],
                        'process_results': result
                    }
        
        elif process_type == "Umidificação Adiabática (dado UR ponto 2)" or process_type == "Adiabatic Humidification (RH point 2)" or process_type == "Humidificación Adiabática (HR punto 2)":
            with st.form("u_adiabatica_ur_form"):
                st.subheader(get_text('state_point_1', st.session_state.language))
                tbs1 = st.number_input(get_text('dry_bulb_temp', st.session_state.language), value=60.0, step=0.1, key="tbs1_ua_ur")
                ur1 = st.number_input(get_text('relative_humidity', st.session_state.language), value=10.0, min_value=0.0, max_value=100.0, step=0.1, key="ur1_ua_ur")
                
                st.subheader(get_text('state_point_2', st.session_state.language))
                ur2 = st.number_input(get_text('relative_humidity', st.session_state.language), value=80.0, min_value=0.0, max_value=100.0, step=0.1, key="ur2_ua")
                
                submit = st.form_submit_button(get_text('calculate', st.session_state.language))
                
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
        
        elif process_type == "Umidificação Adiabática (dado RM ponto 2)" or process_type == "Adiabatic Humidification (MR point 2)" or process_type == "Humidificación Adiabática (RM punto 2)":
            with st.form("u_adiabatica_rm_form"):
                st.subheader(get_text('state_point_1', st.session_state.language))
                tbs1 = st.number_input(get_text('dry_bulb_temp', st.session_state.language), value=60.0, step=0.1, key="tbs1_ua_rm")
                rm1 = st.number_input(get_text('mixture_ratio', st.session_state.language), value=12.5, min_value=0.0, step=0.1, key="rm1_ua")
                
                st.subheader(get_text('state_point_2', st.session_state.language))
                rm2 = st.number_input(get_text('mixture_ratio', st.session_state.language), value=24.0, min_value=0.0, step=0.1, key="rm2_ua")
                
                submit = st.form_submit_button(get_text('calculate', st.session_state.language))
                
                if submit:
                    # Call the calculation function
                    result = calculate_u_adiabatica_rm(tbs1, rm1, rm2, patm)
                    
                    # Verificar se houve erro no cálculo
                    if 'error' in result:
                        st.error(result['error'])
                        st.session_state.process_results = None
                        st.session_state.chart_data = None
                    else:
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
        if st.session_state.process_results and 'point1' in st.session_state.process_results and 'point2' in st.session_state.process_results:
            results = st.session_state.process_results
            
            # Point 1
            st.subheader(f"{get_text('state_point_1', st.session_state.language)}:")
            df1 = pd.DataFrame({
                get_text('property', st.session_state.language): [
                    get_text('dbt_long', st.session_state.language),
                    get_text('wbt_long', st.session_state.language),
                    get_text('dpt_long', st.session_state.language),
                    get_text('rh_long', st.session_state.language),
                    get_text('mr_long', st.session_state.language),
                    get_text('svp_long', st.session_state.language),
                    get_text('vp_long', st.session_state.language),
                    get_text('sv_long', st.session_state.language),
                    get_text('enthalpy_long', st.session_state.language)
                ],
                get_text('value', st.session_state.language): [
                    f"{results['point1']['tbs']:.2f}",
                    f"{results['point1']['tbm']:.2f}",
                    f"{results['point1']['tpo']:.2f}",
                    f"{results['point1']['ur']:.2f}",
                    f"{results['point1']['rm']:.2f}",
                    f"{results['point1']['pvs']:.2f}",
                    f"{results['point1']['pv']:.2f}",
                    f"{results['point1']['ve']:.3f}",
                    f"{results['point1']['e']:.2f}"
                ]
            })
            
            st.table(df1)
            
            # Point 2
            st.subheader(f"{get_text('state_point_2', st.session_state.language)}:")
            df2 = pd.DataFrame({
                get_text('property', st.session_state.language): [
                    get_text('dbt_long', st.session_state.language),
                    get_text('wbt_long', st.session_state.language),
                    get_text('dpt_long', st.session_state.language),
                    get_text('rh_long', st.session_state.language),
                    get_text('mr_long', st.session_state.language),
                    get_text('svp_long', st.session_state.language),
                    get_text('vp_long', st.session_state.language),
                    get_text('sv_long', st.session_state.language),
                    get_text('enthalpy_long', st.session_state.language)
                ],
                get_text('value', st.session_state.language): [
                    f"{results['point2']['tbs']:.2f}",
                    f"{results['point2']['tbm']:.2f}",
                    f"{results['point2']['tpo']:.2f}",
                    f"{results['point2']['ur']:.2f}",
                    f"{results['point2']['rm']:.2f}",
                    f"{results['point2']['pvs']:.2f}",
                    f"{results['point2']['pv']:.2f}",
                    f"{results['point2']['ve']:.3f}",
                    f"{results['point2']['e']:.2f}"
                ]
            })
            
            st.table(df2)
    
    # Plot psychrometric chart
    if st.session_state.chart_data and st.session_state.chart_data['type'] == 'process':
        st.subheader(get_text('psychrometric_chart', st.session_state.language))
        
        # Gráfico Matplotlib estático
        fig = plot_psychrometric_chart(st.session_state.chart_data, patm, altitude, st.session_state.language)
        st.pyplot(fig)
        
        # Mostrar referências
        show_references(st.session_state.language)

elif page == get_text('air_flow_mixing', st.session_state.language):
    st.subheader(get_text('mixing_calc', st.session_state.language))
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.form("mistura_fluxos_form"):
            st.subheader(get_text('airflow_1', st.session_state.language))
            tbs1 = st.number_input(get_text('dry_bulb_temp', st.session_state.language), value=30.0, step=0.1, key="tbs1_mix")
            ur1 = st.number_input(get_text('relative_humidity', st.session_state.language), value=40.0, min_value=0.0, max_value=100.0, step=0.1, key="ur1_mix")
            q1 = st.number_input(get_text('airflow_rate', st.session_state.language), value=100.0, min_value=0.0, step=10.0, key="q1_mix")
            
            st.subheader(get_text('airflow_2', st.session_state.language))
            tbs2 = st.number_input(get_text('dry_bulb_temp', st.session_state.language), value=20.0, step=0.1, key="tbs2_mix")
            ur2 = st.number_input(get_text('relative_humidity', st.session_state.language), value=60.0, min_value=0.0, max_value=100.0, step=0.1, key="ur2_mix")
            q2 = st.number_input(get_text('airflow_rate', st.session_state.language), value=50.0, min_value=0.0, step=10.0, key="q2_mix")
            
            submit = st.form_submit_button(get_text('calculate', st.session_state.language))
            
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
            st.subheader(get_text('mixing_results', st.session_state.language))
            
            df_combined = pd.DataFrame({
                get_text('property', st.session_state.language): [
                    get_text('dbt_short', st.session_state.language),
                    get_text('wbt_short', st.session_state.language),
                    get_text('dpt_short', st.session_state.language),
                    get_text('rh_short', st.session_state.language),
                    get_text('mr_short', st.session_state.language),
                    get_text('svp_short', st.session_state.language),
                    get_text('vp_short', st.session_state.language),
                    get_text('sv_short', st.session_state.language),
                    get_text('enthalpy_short', st.session_state.language),
                    get_text('flow_short', st.session_state.language)
                ],
                get_text('flow_1', st.session_state.language): [
                    f"{results['point1']['tbs']:.2f}",
                    f"{results['point1']['tbm']:.2f}",
                    f"{results['point1']['tpo']:.2f}",
                    f"{results['point1']['ur']:.2f}",
                    f"{results['point1']['rm']:.2f}",
                    f"{results['point1']['pvs']:.2f}",
                    f"{results['point1']['pv']:.2f}",
                    f"{results['point1']['ve']:.3f}",
                    f"{results['point1']['e']:.2f}",
                    f"{results['q1']:.2f}"
                ],
                get_text('flow_2', st.session_state.language): [
                    f"{results['point2']['tbs']:.2f}",
                    f"{results['point2']['tbm']:.2f}",
                    f"{results['point2']['tpo']:.2f}",
                    f"{results['point2']['ur']:.2f}",
                    f"{results['point2']['rm']:.2f}",
                    f"{results['point2']['pvs']:.2f}",
                    f"{results['point2']['pv']:.2f}",
                    f"{results['point2']['ve']:.3f}",
                    f"{results['point2']['e']:.2f}",
                    f"{results['q2']:.2f}"
                ],
                get_text('flow_mix', st.session_state.language): [
                    f"{results['point3']['tbs']:.2f}",
                    f"{results['point3']['tbm']:.2f}",
                    f"{results['point3']['tpo']:.2f}",
                    f"{results['point3']['ur']:.2f}",
                    f"{results['point3']['rm']:.2f}",
                    f"{results['point3']['pvs']:.2f}",
                    f"{results['point3']['pv']:.2f}",
                    f"{results['point3']['ve']:.3f}",
                    f"{results['point3']['e']:.2f}",
                    f"{results['q3']:.2f}"
                ]
            })
            
            st.table(df_combined)
    
    # Plot psychrometric chart
    if st.session_state.chart_data and st.session_state.chart_data['type'] == 'mixing':
        st.subheader(get_text('psychrometric_chart', st.session_state.language))
        
        # Gráfico Matplotlib estático
        fig = plot_psychrometric_chart(st.session_state.chart_data, patm, altitude, st.session_state.language)
        st.pyplot(fig)
        
        # Mostrar referências
        show_references(st.session_state.language)