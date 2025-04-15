"""
Arquivo de traduções para o aplicativo GRAPSI
"""

# Dicionário com todas as strings traduzidas
translations = {
    'pt': {
        # Títulos gerais
        'app_title': 'GRAPSI - Gráfico Psicrométrico Digital',
        'app_description': 'GRAPSI é um aplicativo que calcula as propriedades psicrométricas do ar úmido e as exibe em um gráfico na tela do computador. Ele pode simular processos como aquecimento, resfriamento, umidificação adiabática e mistura de fluxos de ar. O programa opera em uma ampla faixa de temperaturas, de -100 a 372 ºC, e altitudes de até 4.000 metros.',
        'sidebar_title': 'GRAPSI',
        'input_options': 'Opções de Entrada',
        'data_input': 'Dados de Entrada',
        
        # Seleção de página/tipo de cálculo
        'select_calculation': 'Selecione o tipo de cálculo:',
        'state_point': 'Ponto de Estado',
        'psychrometric_processes': 'Processos Psicrométricos',
        'air_flow_mixing': 'Mistura de Fluxos de Ar',
        
        # Configurações
        'site_altitude': 'Altitude do Local (m)',
        'atm_pressure': 'Pressão atmosférica: {pressure:.2f} kPa',
        
        # Página de Ponto de Estado
        'state_point_calc': 'Cálculo do Ponto de Estado',
        'select_method': 'Selecione o método de cálculo:',
        'dbt_rh': 'TBS e UR',
        'dbt_wbt': 'TBS e TBM',
        'dbt_dpt': 'TBS e TPO',
        'dry_bulb_temp': 'Temperatura de bulbo seco (°C)',
        'relative_humidity': 'Umidade relativa (%)',
        'wet_bulb_temp': 'Temperatura de bulbo molhado (°C)',
        'dew_point_temp': 'Temperatura do ponto de orvalho (°C)',
        
        # Botões
        'calculate': 'Calcular',
        
        # Resultados
        'results': 'Resultados:',
        'property': 'Propriedade',
        'value': 'Valor',
        'dbt_long': 'Temperatura de Bulbo Seco (°C)',
        'wbt_long': 'Temperatura de Bulbo Molhado (°C)',
        'dpt_long': 'Temperatura de Ponto de Orvalho (°C)',
        'rh_long': 'Umidade Relativa (%)',
        'mr_long': 'Razão de Mistura (g/kg)',
        'svp_long': 'Pressão de Vapor Saturado (kPa)',
        'vp_long': 'Pressão Parcial de Vapor (kPa)',
        'sv_long': 'Volume Específico (m³/kg)',
        'enthalpy_long': 'Entalpia (kJ/kg)',
        
        # Gráfico
        'psychrometric_chart': 'Gráfico Psicrométrico',
        'chart_title': 'Gráfico Psicrométrico (Altitude = {altitude:.0f} m)',
        'chart_x_axis': 'Temperatura de Bulbo Seco (°C)',
        'chart_y_axis': 'Pressão de Vapor (kPa)',
        'chart_y2_axis': 'Razão de Mistura (g/kg)',
        'rh_100_label': 'UR = 100%',
        'rh_label': 'UR = {value}%',
        'enthalpy_label': 'h={value} kJ/kg',
        'state_point_label': 'Ponto de Estado',
        'point_1_label': 'Ponto 1',
        'point_2_label': 'Ponto 2', 
        'flow_1_label': 'Fluxo 1',
        'flow_2_label': 'Fluxo 2',
        'mixture_label': 'Mistura',
        'point_1_short': 'P1',
        'flow_1_short': 'F1',
        'process_default_name': 'Processo {number}',
        'mixture_default_name': 'Mistura {number}',
        
        # Processos psicrométricos
        'process_calc': 'Cálculo de Processos Psicrométricos',
        'select_process': 'Selecione o tipo de processo:',
        'heating_cooling': 'Aquecimento/Resfriamento',
        'adiabatic_humid_dbt': 'Umidificação Adiabática (TBS)',
        'adiabatic_humid_rh': 'Umidificação Adiabática (UR)',
        'adiabatic_humid_mr': 'Umidificação Adiabática (RM)',
        'state_point_1': 'Ponto de Estado 1',
        'state_point_2': 'Ponto de Estado 2',
        'mixture_ratio': 'Razão de mistura (g/kg)',
        
        # Mistura de Fluxos de Ar
        'mixing_calc': 'Cálculo de Mistura de Fluxos de Ar',
        'airflow_1': 'Fluxo de Ar 1',
        'airflow_2': 'Fluxo de Ar 2',
        'airflow_rate': 'Vazão de ar (m³/h)',
        'mixing_results': 'Resultados da Mistura de Fluxos de Ar:',
        'flow_1': 'Fluxo 1',
        'flow_2': 'Fluxo 2', 
        'flow_mix': 'Fluxo M',
        
        # Tabela de resultados abreviada
        'dbt_short': 'TBS (°C)',
        'wbt_short': 'TBM (°C)',
        'dpt_short': 'TPO (°C)',
        'rh_short': 'UR (%)',
        'mr_short': 'RM (g/kg)',
        'svp_short': 'PVS (kPa)',
        'vp_short': 'PV (kPa)',
        'sv_short': 'VE (m³/kg)',
        'enthalpy_short': 'h (kJ/kg)',
        'flow_short': 'Q (m³/h)',
        
        # Referências
        'references': 'Referências',
        'references_content': '- Melo et al. GRAPSI -Programa Computacional para o Cálculo das Propriedades Psicrométricas do Ar. Engenharia na Agricultura, Viçosa, MG, v.12, n.2, 154-162, Abr./Jun., 2004.\n- Melo, E.C. O Programa Computacional GRAPSI. Edição do autor. 2011.',
        'language': 'Idioma',
        'select_language': 'Selecione o idioma:',
        'portuguese': 'Português',
        'english': 'Inglês',
        'spanish': 'Espanhol',
        'select_calculation_method': 'Selecione o método de cálculo:',
        'author_info': 'Evandro de Castro Melo',
        'author_website': '[web page](https://evandro.eng.br)'
    },
    'en': {
        # General titles
        'app_title': 'GRAPSI - Digital Psychrometric Chart',
        'app_description': 'GRAPSI is an application that calculates the psychrometric properties of moist air and displays them on a chart on the computer screen. It can simulate processes such as heating, cooling, adiabatic humidification, and mixing of air flows. The program operates over a wide temperature range, from -100 to 372 ºC, and altitudes up to 4,000 meters.',
        'sidebar_title': 'GRAPSI',
        'input_options': 'Input Options',
        'data_input': 'Input Data',
        
        # Page/calculation type selection
        'select_calculation': 'Select calculation type:',
        'state_point': 'State Point',
        'psychrometric_processes': 'Psychrometric Processes',
        'air_flow_mixing': 'Air Flow Mixing',
        
        # Settings
        'site_altitude': 'Site Altitude (m)',
        'atm_pressure': 'Atmospheric pressure: {pressure:.2f} kPa',
        
        # State Point page
        'state_point_calc': 'State Point Calculation',
        'select_method': 'Select calculation method:',
        'dbt_rh': 'DBT and RH',
        'dbt_wbt': 'DBT and WBT',
        'dbt_dpt': 'DBT and DPT',
        'dry_bulb_temp': 'Dry bulb temperature (°C)',
        'relative_humidity': 'Relative humidity (%)',
        'wet_bulb_temp': 'Wet bulb temperature (°C)',
        'dew_point_temp': 'Dew point temperature (°C)',
        
        # Buttons
        'calculate': 'Calculate',
        
        # Results
        'results': 'Results:',
        'property': 'Property',
        'value': 'Value',
        'dbt_long': 'Dry Bulb Temperature (°C)',
        'wbt_long': 'Wet Bulb Temperature (°C)',
        'dpt_long': 'Dew Point Temperature (°C)',
        'rh_long': 'Relative Humidity (%)',
        'mr_long': 'Humidity Ratio (g/kg)',
        'svp_long': 'Saturated Vapor Pressure (kPa)',
        'vp_long': 'Partial Vapor Pressure (kPa)',
        'sv_long': 'Specific Volume (m³/kg)',
        'enthalpy_long': 'Enthalpy (kJ/kg)',
        
        # Chart
        'psychrometric_chart': 'Psychrometric Chart',
        'chart_title': 'Psychrometric Chart (Altitude = {altitude:.0f} m)',
        'chart_x_axis': 'Dry Bulb Temperature (°C)',
        'chart_y_axis': 'Vapor Pressure (kPa)',
        'chart_y2_axis': 'Humidity Ratio (g/kg)',
        'rh_100_label': 'RH = 100%',
        'rh_label': 'RH = {value}%',
        'enthalpy_label': 'h={value} kJ/kg',
        'state_point_label': 'State Point',
        'point_1_label': 'Point 1',
        'point_2_label': 'Point 2', 
        'flow_1_label': 'Flow 1',
        'flow_2_label': 'Flow 2',
        'mixture_label': 'Mixture',
        'point_1_short': 'P1',
        'flow_1_short': 'F1',
        'process_default_name': 'Process {number}',
        'mixture_default_name': 'Mixture {number}',
        
        # Psychrometric processes
        'process_calc': 'Psychrometric Process Calculation',
        'select_process': 'Select process type:',
        'heating_cooling': 'Heating/Cooling',
        'adiabatic_humid_dbt': 'Adiabatic Humidification (DBT)',
        'adiabatic_humid_rh': 'Adiabatic Humidification (RH)',
        'adiabatic_humid_mr': 'Adiabatic Humidification (HR)',
        'state_point_1': 'State Point 1',
        'state_point_2': 'State Point 2',
        'mixture_ratio': 'Humidity ratio (g/kg)',
        
        # Air Flow Mixing
        'mixing_calc': 'Air Flow Mixing Calculation',
        'airflow_1': 'Air Flow 1',
        'airflow_2': 'Air Flow 2',
        'airflow_rate': 'Air flow rate (m³/h)',
        'mixing_results': 'Air Flow Mixing Results:',
        'flow_1': 'Flow 1',
        'flow_2': 'Flow 2',
        'flow_mix': 'Flow M',
        
        # Abbreviated results table
        'dbt_short': 'DBT (°C)',
        'wbt_short': 'WBT (°C)',
        'dpt_short': 'DPT (°C)',
        'rh_short': 'RH (%)',
        'mr_short': 'HR (g/kg)',
        'svp_short': 'SVP (kPa)',
        'vp_short': 'VP (kPa)',
        'sv_short': 'SV (m³/kg)',
        'enthalpy_short': 'h (kJ/kg)',
        'flow_short': 'Q (m³/h)',
        
        # References
        'references': 'References',
        'references_content': '- Melo et al. GRAPSI - Computer Program for Calculating Psychrometric Properties of Air. Agricultural Engineering, Viçosa, MG, v.12, n.2, 154-162, Apr./Jun., 2004.\n- Melo, E.C. The GRAPSI Computer Program. Author\'s Edition. 2011.',
        'language': 'Language',
        'select_language': 'Select language:',
        'portuguese': 'Portuguese',
        'english': 'English',
        'spanish': 'Spanish',
        'select_calculation_method': 'Select calculation method:',
        'author_info': 'Evandro de Castro Melo',
        'author_website': '[web page](https://evandro.eng.br)'
    },
    'es': {
        # Títulos generales
        'app_title': 'GRAPSI - Gráfico Psicrométrico Digital',
        'app_description': 'GRAPSI es una aplicación que calcula las propiedades psicrométricas del aire húmedo y las muestra en un gráfico en la pantalla del ordenador. Puede simular procesos como calentamiento, enfriamiento, humidificación adiabática y mezcla de flujos de aire. El programa opera en un amplio rango de temperaturas, desde -100 hasta 372 ºC, y altitudes de hasta 4.000 metros.',
        'sidebar_title': 'GRAPSI',
        'input_options': 'Opciones de Entrada',
        'data_input': 'Datos de Entrada',
        
        # Selección de página/tipo de cálculo
        'select_calculation': 'Seleccione el tipo de cálculo:',
        'state_point': 'Punto de Estado',
        'psychrometric_processes': 'Procesos Psicrométricos',
        'air_flow_mixing': 'Mezcla de Flujos de Aire',
        
        # Configuraciones
        'site_altitude': 'Altitud del Sitio (m)',
        'atm_pressure': 'Presión atmosférica: {pressure:.2f} kPa',
        
        # Página de Punto de Estado
        'state_point_calc': 'Cálculo del Punto de Estado',
        'select_method': 'Seleccione el método de cálculo:',
        'dbt_rh': 'TBS y HR',
        'dbt_wbt': 'TBS y TBH',
        'dbt_dpt': 'TBS y TPR',
        'dry_bulb_temp': 'Temperatura de bulbo seco (°C)',
        'relative_humidity': 'Humedad relativa (%)',
        'wet_bulb_temp': 'Temperatura de bulbo húmedo (°C)',
        'dew_point_temp': 'Temperatura del punto de rocío (°C)',
        
        # Botones
        'calculate': 'Calcular',
        
        # Resultados
        'results': 'Resultados:',
        'property': 'Propiedad',
        'value': 'Valor',
        'dbt_long': 'Temperatura de Bulbo Seco (°C)',
        'wbt_long': 'Temperatura de Bulbo Húmedo (°C)',
        'dpt_long': 'Temperatura de Punto de Rocío (°C)',
        'rh_long': 'Humedad Relativa (%)',
        'mr_long': 'Relación de Mezcla (g/kg)',
        'svp_long': 'Presión de Vapor Saturado (kPa)',
        'vp_long': 'Presión Parcial de Vapor (kPa)',
        'sv_long': 'Volumen Específico (m³/kg)',
        'enthalpy_long': 'Entalpía (kJ/kg)',
        
        # Gráfico
        'psychrometric_chart': 'Gráfico Psicrométrico',
        'chart_title': 'Gráfico Psicrométrico (Altitud = {altitude:.0f} m)',
        'chart_x_axis': 'Temperatura de Bulbo Seco (°C)',
        'chart_y_axis': 'Presión de Vapor (kPa)',
        'chart_y2_axis': 'Relación de Mezcla (g/kg)',
        'rh_100_label': 'HR = 100%',
        'rh_label': 'HR = {value}%',
        'enthalpy_label': 'h={value} kJ/kg',
        'state_point_label': 'Punto de Estado',
        'point_1_label': 'Punto 1',
        'point_2_label': 'Punto 2', 
        'flow_1_label': 'Flujo 1',
        'flow_2_label': 'Flujo 2',
        'mixture_label': 'Mezcla',
        'point_1_short': 'P1',
        'flow_1_short': 'F1',
        'process_default_name': 'Proceso {number}',
        'mixture_default_name': 'Mezcla {number}',
        
        # Procesos psicrométricos
        'process_calc': 'Cálculo de Procesos Psicrométricos',
        'select_process': 'Seleccione el tipo de proceso:',
        'heating_cooling': 'Calentamiento/Enfriamiento',
        'adiabatic_humid_dbt': 'Humidificación Adiabática (TBS)',
        'adiabatic_humid_rh': 'Humidificación Adiabática (HR)',
        'adiabatic_humid_mr': 'Humidificación Adiabática (RM)',
        'state_point_1': 'Punto de Estado 1',
        'state_point_2': 'Punto de Estado 2',
        'mixture_ratio': 'Relación de mezcla (g/kg)',
        
        # Mezcla de Flujos de Aire
        'mixing_calc': 'Cálculo de Mezcla de Flujos de Aire',
        'airflow_1': 'Flujo de Aire 1',
        'airflow_2': 'Flujo de Aire 2',
        'airflow_rate': 'Caudal de aire (m³/h)',
        'mixing_results': 'Resultados de la Mezcla de Flujos de Aire:',
        'flow_1': 'Flujo 1',
        'flow_2': 'Flujo 2', 
        'flow_mix': 'Flujo M',
        
        # Tabla de resultados abreviada
        'dbt_short': 'TBS (°C)',
        'wbt_short': 'TBH (°C)',
        'dpt_short': 'TPR (°C)',
        'rh_short': 'HR (%)',
        'mr_short': 'RM (g/kg)',
        'svp_short': 'PVS (kPa)',
        'vp_short': 'PV (kPa)',
        'sv_short': 'VE (m³/kg)',
        'enthalpy_short': 'h (kJ/kg)',
        'flow_short': 'Q (m³/h)',
        
        # Referencias
        'references': 'Referencias',
        'references_content': '- Melo et al. GRAPSI - Programa Computacional para el Cálculo de las Propiedades Psicrométricas del Aire. Ingeniería Agrícola, Viçosa, MG, v.12, n.2, 154-162, Abr./Jun., 2004.\n- Melo, E.C. El Programa Computacional GRAPSI. Edición del autor. 2011.',
        'language': 'Idioma',
        'select_language': 'Seleccione el idioma:',
        'portuguese': 'Portugués',
        'english': 'Inglés',
        'spanish': 'Español',
        'select_calculation_method': 'Seleccione el método de cálculo:',
        'author_info': 'Evandro de Castro Melo',
        'author_website': '[página web](https://evandro.eng.br)'
    }
}

def get_text(key, lang='pt', **kwargs):
    """
    Retorna o texto traduzido para a chave e idioma fornecidos.
    Argumentos adicionais podem ser passados para formatação da string.
    
    Args:
        key (str): A chave da string no dicionário de traduções
        lang (str): O código do idioma ('pt', 'en' ou 'es')
        **kwargs: Argumentos para formatação da string
        
    Returns:
        str: O texto traduzido
    """
    if lang not in translations:
        lang = 'pt'  # Fallback para português se o idioma não for suportado
        
    if key not in translations[lang]:
        # Se a chave não existir, retorna a própria chave
        return key
    
    text = translations[lang][key]
    
    # Se houver argumentos para formatação, formatar a string
    if kwargs:
        try:
            text = text.format(**kwargs)
        except KeyError:
            # Se a formatação falhar, retorna o texto sem formatar
            pass
    
    return text