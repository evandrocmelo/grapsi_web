import numpy as np
import plotly.graph_objects as go
from psychrometric_functions import pressao_vapor_saturado, razao_mistura1, entalpia, pressao_vapor
from psychrometric_functions import temperatura_ponto_orvalho, temperatura_b_molhado, volume_especifico
from psychrometric_functions import calculate_from_tbs_ur
from translations import get_text

def plot_interactive_psychrometric_chart(data, patm=101.325, altitude=0, lang='pt', comparison_data=None):
    """
    Gera um gráfico psicrométrico interativo com base nos dados fornecidos
    
    Args:
        data: Dicionário contendo o tipo de dados e valores para plotar
        patm: Pressão atmosférica (kPa)
        altitude: Altitude do local (m)
        lang: Idioma para os textos do gráfico ('pt' ou 'en')
        comparison_data: Lista de dicionários com processos adicionais para comparação
    
    Returns:
        fig: Figura Plotly com o gráfico psicrométrico interativo
    """
    # Definir os limites de temperatura com base nos dados
    tbs_min = 10
    tbs_max = 50
    
    # Se houver temperaturas maiores que 50°C, ajustar o máximo
    if 'tbs' in data and data['tbs'] > 45:
        tbs_max = data['tbs'] + 5
    if 'tbs1' in data and data['tbs1'] > 45:
        tbs_max = max(tbs_max, data['tbs1'] + 5)
    if 'tbs2' in data and data['tbs2'] > 45:
        tbs_max = max(tbs_max, data['tbs2'] + 5)
    
    # Ajustar o mínimo com base nos pontos de dados
    if 'tbs' in data and data['tbs'] < 15:
        tbs_min = max(0, data['tbs'] - 5)
    if 'tbs1' in data and data['tbs1'] < 15:
        tbs_min = min(tbs_min, max(0, data['tbs1'] - 5))
    if 'tbs2' in data and data['tbs2'] < 15:
        tbs_min = min(tbs_min, max(0, data['tbs2'] - 5))
    
    # Limite máximo para razão de mistura (g/kg)
    rm_max = 30
    
    # Criar figura Plotly
    fig = go.Figure()
    
    # Gerar curva de saturação (UR = 100%)
    tbs_range = np.linspace(tbs_min, tbs_max, 100)
    pv_saturacao = []  # Para eixo y1 (pressão de vapor)
    rm_saturacao = []  # Para eixo y2 (razão de mistura)
    
    for t in tbs_range:
        pvs = pressao_vapor_saturado(t)
        pv_saturacao.append(pvs)
        rm = razao_mistura1(pvs, patm) * 1000  # Converter para g/kg
        rm_saturacao.append(rm)
    
    # Adicionar curva de saturação ao gráfico
    fig.add_trace(go.Scatter(
        x=tbs_range,
        y=pv_saturacao,
        mode='lines',
        name=get_text('rh_100_label', lang),
        line=dict(color='blue', width=2)
    ))
    
    # Gerar linhas de umidade relativa constante
    ur_values = [10, 20, 30, 40, 50, 60, 70, 80, 90]
    
    for ur in ur_values:
        pv_ur = []
        tbs_ur = []
        rm_ur = []
        
        for t in tbs_range:
            pvs = pressao_vapor_saturado(t)
            pv = (ur / 100) * pvs
            rm = razao_mistura1(pv, patm) * 1000  # g/kg
            
            # Filtrar pontos onde RM fica muito grande (evitar linhas saindo do gráfico)
            if rm <= rm_max:
                pv_ur.append(pv)
                tbs_ur.append(t)
                rm_ur.append(rm)
        
        # Adicionar linha de UR constante ao gráfico
        if len(tbs_ur) > 0:
            fig.add_trace(go.Scatter(
                x=tbs_ur,
                y=pv_ur,
                mode='lines',
                name=get_text('rh_label', lang, value=ur),
                line=dict(color='blue', width=1, dash='dot'),
                showlegend=bool(ur == 50)  # Mostrar apenas uma linha na legenda
            ))
            
            # Adicionar rótulo de UR no meio da linha
            if len(tbs_ur) > 2:
                idx = len(tbs_ur) // 2  # Ponto médio
                rh_text = get_text('rh_label', lang, value=ur)
                fig.add_annotation(
                    x=tbs_ur[idx], 
                    y=pv_ur[idx],
                    text=rh_text,
                    showarrow=False,
                    font=dict(color="blue", size=10)
                )
    
    # Gerar linhas de entalpia constante
    if tbs_max > 50:
        entalpia_values = np.arange(20, 300, 20)
    else:
        entalpia_values = np.arange(20, 150, 10)
    
    for ent in entalpia_values:
        rm_points = np.linspace(0.001, rm_max/1000.0, 50)  # Valores em decimal
        tbs_ent = []
        pv_ent = []
        
        for rm in rm_points:
            # Calcular TBS para entalpia e RM dados
            tbs = (ent - 2501 * rm) / (1.006 + 1.775 * rm)
            
            # Verificar se a temperatura está dentro do range
            if tbs_min <= tbs <= tbs_max:
                pv = pressao_vapor(rm, patm)
                tbs_ent.append(tbs)
                pv_ent.append(pv)
        
        # Adicionar linha de entalpia constante
        if len(tbs_ent) > 1:
            fig.add_trace(go.Scatter(
                x=tbs_ent,
                y=pv_ent,
                mode='lines',
                name=f"h = {ent} kJ/kg",
                line=dict(color='red', width=1, dash='dot'),
                showlegend=bool(ent == 60)  # Mostrar apenas uma linha na legenda
            ))
            
            # Adicionar rótulo de entalpia
            if len(tbs_ent) > 5:
                idx = int(len(tbs_ent) * 0.7)
                enthalpy_text = get_text('enthalpy_label', lang, value=ent)
                fig.add_annotation(
                    x=tbs_ent[idx], 
                    y=pv_ent[idx],
                    text=enthalpy_text,
                    showarrow=False,
                    font=dict(color="red", size=10)
                )
    
    # Plotar dados específicos com base no tipo
    if data['type'] == 'point':
        # Plotar um único ponto de estado
        tbs = data['tbs']
        tbm = data['tbm']
        
        # Usar pv e rm diretamente se forem fornecidos, caso contrário calcular
        if 'pv' in data and 'rm' in data:
            pv = data['pv']
            rm = data['rm']
            rm_gkg = rm * 1000 if rm < 1 else rm  # Converter para g/kg se não estiver
        else:
            # Calcular a partir dos resultados do processo
            if 'process_results' in data and data['process_results']:
                results = data['process_results']
                pv = results['point1']['pv']
                rm_gkg = results['point1']['rm']
            else:
                # Fallback: calcular a partir de TBS e TBM
                pvs = pressao_vapor_saturado(tbs)
                pvs_tbm = pressao_vapor_saturado(tbm)
                rm_tbm = razao_mistura1(pvs_tbm, patm)
                e = entalpia(tbm, rm_tbm)
                
                # Inicializar rm com valor padrão
                rm = 0
                
                for rm_test in np.linspace(0, 0.03, 100):
                    e_test = entalpia(tbs, rm_test)
                    if abs(e_test - e) < 0.1:
                        rm = rm_test
                        break
                
                rm_gkg = rm * 1000  # g/kg
                pv = pressao_vapor(rm, patm)
        
        # Adicionar ponto ao gráfico
        fig.add_trace(go.Scatter(
            x=[tbs],
            y=[pv],
            mode='markers',
            name=get_text('state_point_label', lang),
            marker=dict(color='black', size=12, symbol='circle')
        ))
    
    elif data['type'] == 'process':
        # Plotar um processo (dois pontos e uma linha entre eles)
        tbs1 = data['tbs1']
        tbm1 = data['tbm1']
        tbs2 = data['tbs2']
        tbm2 = data['tbm2']
        
        if 'process_results' in data and data['process_results']:
            # Usar os valores calculados diretamente
            results = data['process_results']
            rm1_gkg = results['point1']['rm']  # Já está em g/kg
            rm2_gkg = results['point2']['rm']
            rm1 = rm1_gkg / 1000.0  # Converter para decimal
            rm2 = rm2_gkg / 1000.0
            pv1 = results['point1']['pv']
            pv2 = results['point2']['pv']
        else:
            # Calcular razões de mistura e pressões
            pvs1 = pressao_vapor_saturado(tbs1)
            pvs_tbm1 = pressao_vapor_saturado(tbm1)
            rm_tbm1 = razao_mistura1(pvs_tbm1, patm)
            e1 = entalpia(tbm1, rm_tbm1)
            
            rm1 = 0
            for rm_test in np.linspace(0, 0.03, 100):
                e_test = entalpia(tbs1, rm_test)
                if abs(e_test - e1) < 0.1:
                    rm1 = rm_test
                    break
            
            pvs2 = pressao_vapor_saturado(tbs2)
            pvs_tbm2 = pressao_vapor_saturado(tbm2)
            rm_tbm2 = razao_mistura1(pvs_tbm2, patm)
            e2 = entalpia(tbm2, rm_tbm2)
            
            rm2 = 0
            for rm_test in np.linspace(0, 0.03, 100):
                e_test = entalpia(tbs2, rm_test)
                if abs(e_test - e2) < 0.1:
                    rm2 = rm_test
                    break
            
            rm1_gkg = rm1 * 1000  # g/kg
            rm2_gkg = rm2 * 1000  # g/kg
            pv1 = pressao_vapor(rm1, patm)
            pv2 = pressao_vapor(rm2, patm)
        
        # Adicionar pontos 1 e 2 ao gráfico
        fig.add_trace(go.Scatter(
            x=[tbs1],
            y=[pv1],
            mode='markers',
            name=get_text('point_1_label', lang),
            marker=dict(color='red', size=12, symbol='circle')
        ))
        
        fig.add_trace(go.Scatter(
            x=[tbs2],
            y=[pv2],
            mode='markers',
            name=get_text('point_2_label', lang),
            marker=dict(color='blue', size=12, symbol='circle')
        ))
        
        # Verificar se é processo de aquecimento/resfriamento com RM2 < RM1
        if 'process_type' in data and data['process_type'] == 'heating_cooling' and rm2 < rm1:
            # Encontrar a interseção com a curva de saturação (ponto de orvalho)
            tpo = temperatura_ponto_orvalho(pv1)
            
            # Calcular a curva de saturação entre TPO e TBS2
            tbs_saturacao = np.linspace(tpo, tbs2, 50)
            pv_saturacao = []
            
            for t in tbs_saturacao:
                pv_saturacao.append(pressao_vapor_saturado(t))
            
            # Adicionar linha horizontal do ponto 1 até TPO
            fig.add_trace(go.Scatter(
                x=[tbs1, tpo],
                y=[pv1, pv1],
                mode='lines',
                line=dict(color='black', width=3),
                showlegend=False
            ))
            
            # Adicionar curva de saturação do TPO até o ponto 2
            fig.add_trace(go.Scatter(
                x=tbs_saturacao,
                y=pv_saturacao,
                mode='lines',
                line=dict(color='black', width=3),
                showlegend=False
            ))
        else:
            # Processo normal - linha reta entre os pontos
            fig.add_trace(go.Scatter(
                x=[tbs1, tbs2],
                y=[pv1, pv2],
                mode='lines',
                line=dict(color='black', width=3),
                showlegend=False
            ))
    
    elif data['type'] == 'mixing':
        # Plotar uma mistura de dois fluxos de ar (três pontos e linhas)
        tbs1 = data['tbs1']
        tbm1 = data['tbm1']
        tbs2 = data['tbs2']
        tbm2 = data['tbm2']
        tbs3 = data['tbs3']
        tbm3 = data['tbm3']
        
        if 'process_results' in data and data['process_results']:
            # Usar os valores calculados diretamente
            results = data['process_results']
            rm1_gkg = results['point1']['rm']  # g/kg
            rm2_gkg = results['point2']['rm']
            rm3_gkg = results['point3']['rm']
            rm1 = rm1_gkg / 1000.0  # Converter para decimal
            rm2 = rm2_gkg / 1000.0
            rm3 = rm3_gkg / 1000.0
            pv1 = results['point1']['pv']
            pv2 = results['point2']['pv']
            pv3 = results['point3']['pv']
        else:
            # Cálculos de fallback (simplificados)
            rm1 = rm2 = rm3 = 0
            pv1 = pressao_vapor(rm1, patm)
            pv2 = pressao_vapor(rm2, patm)
            pv3 = pressao_vapor(rm3, patm)
        
        # Adicionar pontos ao gráfico
        fig.add_trace(go.Scatter(
            x=[tbs1],
            y=[pv1],
            mode='markers',
            name=get_text('flow_1_label', lang),
            marker=dict(color='red', size=12, symbol='circle')
        ))
        
        fig.add_trace(go.Scatter(
            x=[tbs2],
            y=[pv2],
            mode='markers',
            name=get_text('flow_2_label', lang),
            marker=dict(color='green', size=12, symbol='circle')
        ))
        
        fig.add_trace(go.Scatter(
            x=[tbs3],
            y=[pv3],
            mode='markers',
            name=get_text('mixture_label', lang),
            marker=dict(color='blue', size=12, symbol='circle')
        ))
        
        # Adicionar linhas de mistura
        fig.add_trace(go.Scatter(
            x=[tbs1, tbs3],
            y=[pv1, pv3],
            mode='lines',
            line=dict(color='black', width=2, dash='dash'),
            showlegend=False
        ))
        
        fig.add_trace(go.Scatter(
            x=[tbs2, tbs3],
            y=[pv2, pv3],
            mode='lines',
            line=dict(color='black', width=2, dash='dash'),
            showlegend=False
        ))
    
    # Configurar layout do gráfico
    fig.update_layout(
        title=get_text('chart_title', lang, altitude=altitude),
        xaxis_title=get_text('chart_x_axis', lang),
        yaxis_title=get_text('chart_y_axis', lang),
        template="plotly_white",
        hovermode='closest',
        width=800,
        height=600,
        showlegend=False,  # Remover a legenda
        margin=dict(l=80, r=80, t=80, b=80),
        # Adicionar funcionalidade de clique
        clickmode='event+select',
        # Forçar modo claro
        paper_bgcolor='white',
        plot_bgcolor='white'
    )
    
    # Configurar eixos
    fig.update_xaxes(
        range=[tbs_min, tbs_max], 
        gridcolor="lightgray",
        showline=True,
        linewidth=2,
        linecolor='black',
        ticks="outside",
        tickfont=dict(color='black'),
        tickwidth=2,
        tickcolor='black',
        title_font=dict(color='black')
    )
    fig.update_yaxes(
        range=[0, 5], 
        gridcolor="lightgray",
        showline=True,
        linewidth=2,
        linecolor='black',
        ticks="outside",
        tickfont=dict(color='black'),
        tickwidth=2,
        tickcolor='black',
        title_font=dict(color='black')
    )  # PV em kPa
    
    # Adicionar funcionalidade de clique
    # Note: A detecção de clique é processada no lado do cliente usando Streamlit
    
    return fig

def calculate_properties_from_click(x=25.0, y=1.5, patm=101.325):
    """
    Calcula as propriedades psicrométricas do ponto clicado no gráfico
    
    Args:
        x: Temperatura de bulbo seco (°C), default=25.0
        y: Pressão de vapor (kPa), default=1.5
        patm: Pressão atmosférica (kPa)
    
    Returns:
        dict: Dicionário com as propriedades calculadas
    """
    # Temperatura de bulbo seco = coordenada x
    tbs = x
    
    # Pressão parcial de vapor = coordenada y
    pv = y
    
    # Pressão de vapor saturado
    pvs = pressao_vapor_saturado(tbs)
    
    # Umidade relativa (decimal)
    ur = pv / pvs
    
    # Razão de mistura (g/kg)
    rm = razao_mistura1(pv, patm) * 1000
    
    # Temperatura do ponto de orvalho
    tpo = temperatura_ponto_orvalho(pv)
    
    # Entalpia
    e = entalpia(tbs, rm/1000.0)
    
    # Temperatura de bulbo molhado
    tbm = temperatura_b_molhado(tbs, e, patm)
    
    # Volume específico
    ve = volume_especifico(tbs, rm/1000.0, patm)
    
    # Retornar propriedades
    return {
        'tbs': tbs,
        'tbm': tbm,
        'tpo': tpo,
        'ur': ur * 100,  # Converter para porcentagem
        'rm': rm,
        'pvs': pvs,
        'pv': pv,
        've': ve,
        'e': e
    }