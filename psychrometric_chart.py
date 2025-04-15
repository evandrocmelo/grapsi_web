import numpy as np
import matplotlib.pyplot as plt
from psychrometric_functions import pressao_vapor_saturado, razao_mistura1, temperatura_ponto_orvalho, temperatura_b_molhado, entalpia, pressao_vapor
from translations import get_text

def plot_psychrometric_chart(data, patm=101.325, altitude=0, lang='pt', comparison_data=None):
    """
    Gera um gráfico psicrométrico com base nos dados fornecidos
    
    Args:
        data: Dicionário contendo o tipo de dados e valores para plotar
        patm: Pressão atmosférica (kPa)
        altitude: Altitude do local (m)
        lang: Idioma para os textos do gráfico ('pt' ou 'en')
        comparison_data: Lista de dicionários com processos adicionais para comparação
    
    Returns:
        fig: Figura matplotlib com o gráfico psicrométrico
    """
    # Criar a figura
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Determinar limites do eixo x (temperatura) com base nos dados
    tbs_min = 10  # Valor padrão mínimo
    tbs_max = 50  # Valor padrão máximo
    
    # Verificar pontos de dados para possível ajuste de escala
    max_tbs_input = 0
    
    if data['type'] == 'point':
        max_tbs_input = max(max_tbs_input, data['tbs'])
    elif data['type'] == 'process':
        max_tbs_input = max(max_tbs_input, data['tbs1'], data['tbs2'])
    elif data['type'] == 'mixing':
        max_tbs_input = max(max_tbs_input, data['tbs1'], data['tbs2'], data['tbs3'])
    
    # Se houver temperaturas maiores que 50°C, ajustar a escala
    if max_tbs_input > 50:
        tbs_min = 15
        tbs_max = max_tbs_input + 5
    
    rm_max = 30  # g/kg - valor fixo para razão de mistura
    
    # Configurar eixos
    ax.set_xlim(tbs_min, tbs_max)
    ax.set_ylim(0, 5)  # Pressão de vapor em kPa, máximo aprox. 5 kPa
    ax.set_xlabel(get_text('chart_x_axis', lang))
    ax.set_ylabel(get_text('chart_y_axis', lang))
    
    # Criar segundo eixo Y à direita para razão de mistura
    ax2 = ax.twinx()
    ax2.set_ylim(0, rm_max)  # Razão de mistura em g/kg (0-30)
    ax2.set_ylabel(get_text('chart_y2_axis', lang))
    
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Gerar curva de saturação (UR = 100%) e dados para ambos os eixos
    tbs_range = np.linspace(tbs_min, tbs_max, 100)
    pv_saturacao = []  # Para eixo esquerdo (pressão de vapor)
    rm_saturacao = []  # Para eixo direito (razão de mistura)
    
    for t in tbs_range:
        pvs = pressao_vapor_saturado(t)
        pv_saturacao.append(pvs)
        rm = razao_mistura1(pvs, patm) * 1000  # Converter para g/kg
        rm_saturacao.append(rm)
    
    # Plotar no eixo principal (pressão de vapor)
    ax.plot(tbs_range, pv_saturacao, 'b-', linewidth=2, label=get_text('rh_100_label', lang))
    # Plotar no eixo secundário (razão de mistura)
    ax2.plot(tbs_range, rm_saturacao, 'b-', linewidth=2, alpha=0.1)
    
    # Gerar curvas de umidade relativa constante
    ur_values = [10, 20, 30, 40, 50, 60, 70, 80, 90]
    
    for ur in ur_values:
        ur_decimal = ur / 100.0
        pv_ur = []  # Para eixo esquerdo (pressão de vapor)
        rm_ur = []  # Para eixo direito (razão de mistura)
        valid_indices = []  # Índices onde a razão de mistura está dentro do limite
        
        for i, t in enumerate(tbs_range):
            pvs = pressao_vapor_saturado(t)
            pv = pvs * ur_decimal
            pv_ur.append(pv)
            rm = razao_mistura1(pv, patm) * 1000  # Converter para g/kg
            rm_ur.append(rm)
            
            # Verificar se a razão de mistura está dentro do limite (RM_MAX)
            if rm <= rm_max:
                valid_indices.append(i)
        
        # Plotar no eixo principal (pressão de vapor)
        ax.plot(tbs_range, pv_ur, 'b-', linewidth=1, alpha=0.5)
        
        # Adicionar rótulo de UR apenas se houver pontos válidos
        if valid_indices:
            # Usar um ponto intermediário válido para o rótulo
            idx = valid_indices[len(valid_indices) // 2]
            
            # Obter texto traduzido para o rótulo UR
            rh_text = get_text('rh_label', lang, value=ur)
            
            if ur == 10:
                ax.text(tbs_range[idx], pv_ur[idx], rh_text, 
                        color='blue', fontsize=8, ha='left', va='bottom')
            else:
                ax.text(tbs_range[idx], pv_ur[idx], rh_text, 
                        color='blue', fontsize=8, ha='center', va='center')
    
    # Removidas as linhas de temperatura de bulbo molhado constante conforme solicitado
    
    # Gerar linhas de entalpia constante
    # Ajustar os valores de entalpia com base na temperatura máxima
    if tbs_max > 50:
        # Para temperaturas maiores, usar uma faixa mais ampla
        entalpia_values = np.arange(20, 300, 20)
    else:
        # Faixa padrão para temperaturas normais
        entalpia_values = np.arange(20, 150, 10)
    
    # Para cada valor de entalpia constante
    for ent in entalpia_values:
        # Abordagem diferente: vamos calcular as linhas de entalpia
        # baseadas em uma faixa de razão de mistura e encontrar as temperaturas
        
        # Definir os pontos de razão de mistura com valores fixos de 0 até RM_MAX
        # Criar linearmente os pontos entre 0 e RM_MAX
        rm_points = np.linspace(0.001, rm_max/1000.0, 50)  # Valores fixos em g/kg convertidos para decimal
        tbs_ent = []
        rm_ent = []
        pv_ent = []
        
        for rm in rm_points:
            # Calcular temperatura para esta entalpia e razão de mistura
            # h = 1.006*tbs + w*(2501+1.775*tbs)
            # Reorganizando para isolar tbs:
            # tbs = (h - 2501*w) / (1.006 + 1.775*w)
            tbs = (ent - 2501 * rm) / (1.006 + 1.775 * rm)
            
            # Verificar se a temperatura está dentro da faixa válida para o gráfico
            if tbs_min <= tbs <= tbs_max:
                # Calcular pressão de vapor correspondente
                pv = pressao_vapor(rm, patm)
                
                tbs_ent.append(tbs)
                rm_ent.append(rm * 1000)  # Converter para g/kg para plotagem
                pv_ent.append(pv)
        
        # Verificar se há pontos suficientes para desenhar a linha
        if len(tbs_ent) > 1:  # Precisa de pelo menos 2 pontos para formar uma linha
            # Plotar no eixo principal (pressão de vapor)
            ax.plot(tbs_ent, pv_ent, 'r-', linewidth=1, alpha=0.5)
            # Plotar no eixo secundário (sem mostrar, apenas para referência)
            ax2.plot(tbs_ent, rm_ent, 'r-', linewidth=1, alpha=0.1)
            
            # Adicionar rótulo de entalpia em posição adequada
            if len(tbs_ent) > 2:
                # Usar um ponto a 70% do comprimento da linha
                idx = int(len(tbs_ent) * 0.7)
                if idx < len(tbs_ent):
                    enthalpy_text = get_text('enthalpy_label', lang, value=ent)
                    ax.text(tbs_ent[idx], pv_ent[idx], enthalpy_text, 
                            color='red', fontsize=8, ha='right', va='center')
    
    # Plotar dados específicos com base no tipo
    if data['type'] == 'point':
        # Plotar um único ponto de estado
        tbs = data['tbs']
        tbm = data['tbm']
        
        # Usar pv e rm diretamente se forem fornecidos, caso contrário calcular
        if 'pv' in data and 'rm' in data:
            pv = data['pv']
            rm = data['rm']
            rm_gkg = rm * 1000  # Converter para g/kg se não estiver em g/kg
        else:
            # Calcular a razão de mistura (método antigo como fallback)
            pvs = pressao_vapor_saturado(tbs)
            pvs_tbm = pressao_vapor_saturado(tbm)
            rm_tbm = razao_mistura1(pvs_tbm, patm)
            
            # Para o cálculo da RM, precisamos fazer uma aproximação usando TBM
            e = entalpia(tbm, rm_tbm)
            
            # Tentar diferentes valores de RM até encontrar o que corresponde ao TBS e TBM
            rm = 0
            for rm_test in np.linspace(0, 0.03, 100):  # 0 a 30 g/kg
                e_test = entalpia(tbs, rm_test)
                if abs(e_test - e) < 0.1:
                    rm = rm_test
                    break
            
            rm_gkg = rm * 1000  # Converter para g/kg
            
            # Calcular a pressão de vapor para o eixo principal
            pv = pressao_vapor(rm, patm)
        
        # Plotar no eixo principal (pressão de vapor) - apenas o círculo preto sem rótulo
        ax.plot(tbs, pv, 'ko', markersize=10, markeredgewidth=2, label=get_text('state_point_label', lang))
        # Plotar no eixo secundário (razão de mistura) - invisível para referência
        ax2.plot(tbs, rm_gkg, 'ko', markersize=10, markeredgewidth=2, alpha=0.1)
    
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
            # Calcular razões de mistura (método antigo como fallback)
            pvs1 = pressao_vapor_saturado(tbs1)
            pvs_tbm1 = pressao_vapor_saturado(tbm1)
            rm_tbm1 = razao_mistura1(pvs_tbm1, patm)
            e1 = entalpia(tbm1, rm_tbm1)
            
            pvs2 = pressao_vapor_saturado(tbs2)
            pvs_tbm2 = pressao_vapor_saturado(tbm2)
            rm_tbm2 = razao_mistura1(pvs_tbm2, patm)
            e2 = entalpia(tbm2, rm_tbm2)
            
            # Encontrar RM que corresponde a TBS e TBM
            rm1 = 0
            for rm_test in np.linspace(0, 0.03, 100):
                e_test = entalpia(tbs1, rm_test)
                if abs(e_test - e1) < 0.1:
                    rm1 = rm_test
                    break
            
            rm2 = 0
            for rm_test in np.linspace(0, 0.03, 100):
                e_test = entalpia(tbs2, rm_test)
                if abs(e_test - e2) < 0.1:
                    rm2 = rm_test
                    break
            
            rm1_gkg = rm1 * 1000  # Converter para g/kg
            rm2_gkg = rm2 * 1000  # Converter para g/kg
            
            # Calcular pressões de vapor para o eixo principal
            pv1 = pressao_vapor(rm1, patm)
            pv2 = pressao_vapor(rm2, patm)
        
        # Plotar pontos e linha com maior destaque no eixo principal (pressão de vapor)
        # Sem rótulos, apenas os círculos coloridos
        ax.plot(tbs1, pv1, 'ro', markersize=10, markeredgewidth=2, label=get_text('point_1_label', lang))
        ax.plot(tbs2, pv2, 'bo', markersize=10, markeredgewidth=2, label=get_text('point_2_label', lang))
        
        # Verificar o tipo de processo
        if 'process_type' in data and data['process_type'] == 'heating_cooling' and rm2 < rm1:
            # Processo especial de aquecimento/resfriamento com condensação
            # Encontrar a interseção com a curva de saturação (TPO)
            tpo = temperatura_ponto_orvalho(pv1)  # Ponto de orvalho = temperatura onde UR=100% para o mesmo pv
            pvs_tpo = pressao_vapor_saturado(tpo)  # Deve ser igual a pv1
            
            # Calcular a pressão de vapor saturado para o traçado da curva de saturação
            # entre o ponto de orvalho (tpo) e a temperatura de bulbo seco 2 (tbs2)
            tbs_saturacao = np.linspace(tpo, tbs2, 50)
            pv_saturacao = []
            
            for t in tbs_saturacao:
                pv_saturacao.append(pressao_vapor_saturado(t))
            
            # Desenhar o caminho real do processo:
            # 1. Linha horizontal do ponto 1 até o ponto onde UR=100% (tpo, pv1)
            ax.plot([tbs1, tpo], [pv1, pv1], 'k-', linewidth=3)
            
            # 2. Curva seguindo a linha de UR=100% do ponto de orvalho até o ponto 2
            ax.plot(tbs_saturacao, pv_saturacao, 'k-', linewidth=3)
        elif 'process' in data and data['process'] == 'u_adiabatica':
            # Processo de umidificação adiabática - linha de entalpia constante
            # A entalpia é constante, então vamos desenhar uma linha de entalpia entre os pontos
            
            # Definir pontos entre rm1 e rm2 para desenhar a linha de entalpia
            if rm1 < rm2:
                rm_points = np.linspace(rm1, rm2, 50)  # Do menor para o maior
            else:
                rm_points = np.linspace(rm2, rm1, 50)  # Do menor para o maior
                
            # Obter a entalpia do ponto 1 (que é igual à do ponto 2)
            # Verificar se temos os resultados disponíveis diretamente
            if 'process_results' in data and data['process_results']:
                e1 = data['process_results']['point1']['e']
            else:
                # Estimativa da entalpia se não temos os resultados completos
                e1 = entalpia(tbs1, rm1)
            
            tbs_ent = []
            pv_ent = []
            
            for rm in rm_points:
                # Calcular temperatura para esta entalpia e razão de mistura
                # usando a mesma fórmula usada para desenhar linhas de entalpia
                tbs = (e1 - 2501 * rm) / (1.006 + 1.775 * rm)
                
                # Verificar se a temperatura está dentro da faixa válida
                if tbs_min <= tbs <= tbs_max:
                    # Calcular pressão de vapor correspondente
                    pv = pressao_vapor(rm, patm)
                    
                    tbs_ent.append(tbs)
                    pv_ent.append(pv)
            
            # Desenhar a linha de entalpia constante
            if len(tbs_ent) > 1:
                ax.plot(tbs_ent, pv_ent, 'k-', linewidth=3)
        else:
            # Processo normal - linha reta entre os pontos
            ax.plot([tbs1, tbs2], [pv1, pv2], 'k-', linewidth=3)  # Linha mais grossa
        
        # Plotar também no eixo secundário (invisível)
        ax2.plot(tbs1, rm1_gkg, 'ro', markersize=5, alpha=0.1)
        ax2.plot(tbs2, rm2_gkg, 'bo', markersize=5, alpha=0.1)
    
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
            rm1_gkg = results['point1']['rm']  # Já está em g/kg
            rm2_gkg = results['point2']['rm']
            rm3_gkg = results['point3']['rm']
            rm1 = rm1_gkg / 1000.0  # Converter para decimal
            rm2 = rm2_gkg / 1000.0
            rm3 = rm3_gkg / 1000.0
            pv1 = results['point1']['pv']
            pv2 = results['point2']['pv']
            pv3 = results['point3']['pv']
        else:
            # Calcular razões de mistura (aproximação usando TBM)
            pvs1 = pressao_vapor_saturado(tbs1)
            pvs_tbm1 = pressao_vapor_saturado(tbm1)
            rm_tbm1 = razao_mistura1(pvs_tbm1, patm)
            e1 = entalpia(tbm1, rm_tbm1)
            
            pvs2 = pressao_vapor_saturado(tbs2)
            pvs_tbm2 = pressao_vapor_saturado(tbm2)
            rm_tbm2 = razao_mistura1(pvs_tbm2, patm)
            e2 = entalpia(tbm2, rm_tbm2)
            
            pvs3 = pressao_vapor_saturado(tbs3)
            pvs_tbm3 = pressao_vapor_saturado(tbm3)
            rm_tbm3 = razao_mistura1(pvs_tbm3, patm)
            e3 = entalpia(tbm3, rm_tbm3)
            
            # Encontrar RM que corresponde a TBS e TBM
            rm1 = 0
            for rm_test in np.linspace(0, 0.03, 100):
                e_test = entalpia(tbs1, rm_test)
                if abs(e_test - e1) < 0.1:
                    rm1 = rm_test
                    break
            
            rm2 = 0
            for rm_test in np.linspace(0, 0.03, 100):
                e_test = entalpia(tbs2, rm_test)
                if abs(e_test - e2) < 0.1:
                    rm2 = rm_test
                    break
                    
            rm3 = 0
            for rm_test in np.linspace(0, 0.03, 100):
                e_test = entalpia(tbs3, rm_test)
                if abs(e_test - e3) < 0.1:
                    rm3 = rm_test
                    break
            
            rm1_gkg = rm1 * 1000  # Converter para g/kg
            rm2_gkg = rm2 * 1000  # Converter para g/kg
            rm3_gkg = rm3 * 1000  # Converter para g/kg
            
            # Calcular pressões de vapor para o eixo principal
            pv1 = pressao_vapor(rm1, patm)
            pv2 = pressao_vapor(rm2, patm)
            pv3 = pressao_vapor(rm3, patm)
        
        # Plotar pontos e linhas com maior destaque no eixo principal (pressão de vapor)
        # Sem rótulos, apenas os círculos coloridos
        ax.plot(tbs1, pv1, 'ro', markersize=10, markeredgewidth=2, label=get_text('flow_1_label', lang))
        ax.plot(tbs2, pv2, 'go', markersize=10, markeredgewidth=2, label=get_text('flow_2_label', lang))
        ax.plot(tbs3, pv3, 'bo', markersize=10, markeredgewidth=2, label=get_text('mixture_label', lang))
        
        # Linha de mistura com maior destaque
        ax.plot([tbs1, tbs3], [pv1, pv3], 'k--', linewidth=2)
        ax.plot([tbs2, tbs3], [pv2, pv3], 'k--', linewidth=2)
        
        # Plotar também no eixo secundário (invisível)
        ax2.plot(tbs1, rm1_gkg, 'ro', markersize=5, alpha=0.1)
        ax2.plot(tbs2, rm2_gkg, 'go', markersize=5, alpha=0.1)
        ax2.plot(tbs3, rm3_gkg, 'bo', markersize=5, alpha=0.1)
    
    # Plotar processos adicionais para comparação, se existirem
    if comparison_data and len(comparison_data) > 0:
        # Cores distintas para cada processo adicional
        colors = ['purple', 'orange', 'darkgreen', 'brown', 'magenta', 'teal', 'olive', 'gold', 'cyan']
        
        for i, comp_data in enumerate(comparison_data):
            color_idx = i % len(colors)  # Ciclar pelas cores se houver mais processos que cores
            color = colors[color_idx]
            
            if comp_data['type'] == 'process':
                # Extrair dados do processo
                tbs1 = comp_data['tbs1']
                tbm1 = comp_data['tbm1']
                tbs2 = comp_data['tbs2']
                tbm2 = comp_data['tbm2']
                
                # Calcular razões de mistura e pressões de vapor
                pvs1 = pressao_vapor_saturado(tbs1)
                pvs_tbm1 = pressao_vapor_saturado(tbm1)
                rm_tbm1 = razao_mistura1(pvs_tbm1, patm)
                e1 = entalpia(tbm1, rm_tbm1)
                
                pvs2 = pressao_vapor_saturado(tbs2)
                pvs_tbm2 = pressao_vapor_saturado(tbm2)
                rm_tbm2 = razao_mistura1(pvs_tbm2, patm)
                e2 = entalpia(tbm2, rm_tbm2)
                
                # Encontrar RM que corresponde a TBS e TBM
                rm1 = 0
                for rm_test in np.linspace(0, 0.03, 100):
                    e_test = entalpia(tbs1, rm_test)
                    if abs(e_test - e1) < 0.1:
                        rm1 = rm_test
                        break
                
                rm2 = 0
                for rm_test in np.linspace(0, 0.03, 100):
                    e_test = entalpia(tbs2, rm_test)
                    if abs(e_test - e2) < 0.1:
                        rm2 = rm_test
                        break
                
                rm1_gkg = rm1 * 1000  # Converter para g/kg
                rm2_gkg = rm2 * 1000  # Converter para g/kg
                
                # Calcular pressões de vapor para o eixo principal
                pv1 = pressao_vapor(rm1, patm)
                pv2 = pressao_vapor(rm2, patm)
                
                # Processo name ou process type para legenda
                default_process_name = get_text('process_default_name', lang, number=i+1)
                process_name = comp_data.get('process_name', default_process_name)
                
                # Plotar pontos e linha
                point_label = get_text('point_1_short', lang) 
                ax.plot(tbs1, pv1, 'o', color=color, markersize=8, label=f"{process_name} - {point_label}")
                ax.plot(tbs2, pv2, 'o', color=color, markersize=8)
                ax.plot([tbs1, tbs2], [pv1, pv2], '-', color=color, linewidth=2)
                
                # Também plotar no eixo secundário (invisível)
                ax2.plot(tbs1, rm1_gkg, 'o', color=color, markersize=5, alpha=0.1)
                ax2.plot(tbs2, rm2_gkg, 'o', color=color, markersize=5, alpha=0.1)
            
            elif comp_data['type'] == 'mixing':
                # Plotar uma mistura de dois fluxos de ar (três pontos e linhas)
                tbs1 = comp_data['tbs1']
                tbm1 = comp_data['tbm1']
                tbs2 = comp_data['tbs2']
                tbm2 = comp_data['tbm2']
                tbs3 = comp_data['tbs3']
                tbm3 = comp_data['tbm3']
                
                # Calcular razões de mistura e pressões de vapor (mesmo cálculo do código normal)
                # (lógica simplificada para brevidade)
                pvs1 = pressao_vapor_saturado(tbs1)
                pvs_tbm1 = pressao_vapor_saturado(tbm1)
                rm_tbm1 = razao_mistura1(pvs_tbm1, patm)
                e1 = entalpia(tbm1, rm_tbm1)
                
                pvs2 = pressao_vapor_saturado(tbs2)
                pvs_tbm2 = pressao_vapor_saturado(tbm2)
                rm_tbm2 = razao_mistura1(pvs_tbm2, patm)
                e2 = entalpia(tbm2, rm_tbm2)
                
                pvs3 = pressao_vapor_saturado(tbs3)
                pvs_tbm3 = pressao_vapor_saturado(tbm3)
                rm_tbm3 = razao_mistura1(pvs_tbm3, patm)
                e3 = entalpia(tbm3, rm_tbm3)
                
                # Encontrar RM que corresponde a TBS e TBM (para cada ponto)
                rm1 = 0
                for rm_test in np.linspace(0, 0.03, 100):
                    e_test = entalpia(tbs1, rm_test)
                    if abs(e_test - e1) < 0.1:
                        rm1 = rm_test
                        break
                
                rm2 = 0
                for rm_test in np.linspace(0, 0.03, 100):
                    e_test = entalpia(tbs2, rm_test)
                    if abs(e_test - e2) < 0.1:
                        rm2 = rm_test
                        break
                
                rm3 = 0
                for rm_test in np.linspace(0, 0.03, 100):
                    e_test = entalpia(tbs3, rm_test)
                    if abs(e_test - e3) < 0.1:
                        rm3 = rm_test
                        break
                
                rm1_gkg = rm1 * 1000  # Converter para g/kg
                rm2_gkg = rm2 * 1000  # Converter para g/kg
                rm3_gkg = rm3 * 1000  # Converter para g/kg
                
                # Calcular pressões de vapor para o eixo principal
                pv1 = pressao_vapor(rm1, patm)
                pv2 = pressao_vapor(rm2, patm)
                pv3 = pressao_vapor(rm3, patm)
                
                # Nome do processo para a legenda
                default_mixture_name = get_text('mixture_default_name', lang, number=i+1)
                process_name = comp_data.get('process_name', default_mixture_name)
                
                # Plotar pontos e linhas
                flow_label = get_text('flow_1_short', lang)
                ax.plot(tbs1, pv1, 'o', color=color, markersize=8, label=f"{process_name} - {flow_label}")
                ax.plot(tbs2, pv2, 'o', color=color, markersize=8)
                ax.plot(tbs3, pv3, 'o', color=color, markersize=8)
                
                # Linhas de mistura
                ax.plot([tbs1, tbs3], [pv1, pv3], '--', color=color, linewidth=1.5)
                ax.plot([tbs2, tbs3], [pv2, pv3], '--', color=color, linewidth=1.5)
                
                # Também plotar no eixo secundário (invisível)
                ax2.plot(tbs1, rm1_gkg, 'o', color=color, markersize=5, alpha=0.1)
                ax2.plot(tbs2, rm2_gkg, 'o', color=color, markersize=5, alpha=0.1)
                ax2.plot(tbs3, rm3_gkg, 'o', color=color, markersize=5, alpha=0.1)
    
    ax.set_title(get_text('chart_title', lang, altitude=altitude))
    ax.legend(loc='upper left')
    
    plt.tight_layout()
    return fig
