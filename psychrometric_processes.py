from psychrometric_functions import *

def calculate_aquece_resfria(tbs1, ur1, tbs2, patm):
    """
    Calcula o processo de aquecimento ou resfriamento
    
    Args:
        tbs1: Temperatura de bulbo seco inicial (°C)
        ur1: Umidade relativa inicial (decimal)
        tbs2: Temperatura de bulbo seco final (°C)
        patm: Pressão atmosférica (kPa)
    
    Returns:
        dict: Dicionário com as propriedades dos pontos 1 e 2
    """
    # Point State 1
    pvs = pressao_vapor_saturado(tbs1)
    pv = ur1 * pvs
    rm = razao_mistura1(pv, patm)
    tpo = temperatura_ponto_orvalho(pv)
    e = entalpia(tbs1, rm)
    tbm = temperatura_b_molhado(tbs1, e, patm)
    ve = volume_especifico(tbs1, rm, patm)
    
    point1 = {
        'tbs': tbs1,
        'tbm': tbm,
        'tpo': tpo,
        'ur': ur1 * 100,  # Convertido para percentual
        'rm': rm * 1000,  # Convertido para g/kg
        'pvs': pvs,
        'pv': pv,
        've': ve,
        'e': e
    }
    
    # Ponto de Estado 2
    pvs2 = pressao_vapor_saturado(tbs2)
    if tbs2 > tpo:
        rm2 = rm
        pv2 = pv
        ur2 = pv2 / pvs2
        tpo2 = tpo
        e2 = entalpia(tbs2, rm2)
        tbm2 = temperatura_b_molhado(tbs2, e2, patm)
    else:
        ur2 = 1.0
        pv2 = ur2 * pvs2
        rm2 = razao_mistura1(pv2, patm)
        tpo2 = tbs2
        e2 = entalpia(tbs2, rm2)
        tbm2 = tbs2
    
    ve2 = volume_especifico(tbs2, rm2, patm)
    
    point2 = {
        'tbs': tbs2,
        'tbm': tbm2,
        'tpo': tpo2,
        'ur': ur2 * 100,  # Convertido para percentual
        'rm': rm2 * 1000,  # Convertido para g/kg
        'pvs': pvs2,
        'pv': pv2,
        've': ve2,
        'e': e2
    }
    
    return {'point1': point1, 'point2': point2}

def calculate_u_adiabatica_tbs(tbs1, ur1, tbs2, patm):
    """
    Calcula o processo de umidificação adiabática até uma temperatura de bulbo seco alvo
    
    Args:
        tbs1: Temperatura de bulbo seco inicial (°C)
        ur1: Umidade relativa inicial (decimal)
        tbs2: Temperatura de bulbo seco final (°C)
        patm: Pressão atmosférica (kPa)
    
    Returns:
        dict: Dicionário com as propriedades dos pontos 1 e 2
    """
    # Ponto de Estado 1
    pvs = pressao_vapor_saturado(tbs1)
    pv = ur1 * pvs
    rm = razao_mistura1(pv, patm)
    e = entalpia(tbs1, rm)
    ve = volume_especifico(tbs1, rm, patm)
    
    if ur1 == 1:
        tpo = tbs1
        tbm = tbs1
    else:
        tpo = temperatura_ponto_orvalho(pv)
        tbm = temperatura_b_molhado(tbs1, e, patm)
    
    point1 = {
        'tbs': tbs1,
        'tbm': tbm,
        'tpo': tpo,
        'ur': ur1 * 100,
        'rm': rm * 1000,
        'pvs': pvs,
        'pv': pv,
        've': ve,
        'e': e
    }
    
    # Ponto de Estado 2
    tbm2 = tbm
    e2 = e
    rm2 = rm
    
    # Ajuste da razão de mistura até atingir a temperatura de bulbo seco desejada
    iterations = 0
    max_iterations = 1000
    
    while iterations < max_iterations:
        iterations += 1
        
        if tbs1 > tbs2:  # indica que ur1 < ur2
            rm2 = rm2 + 0.0001
        else:
            rm2 = rm2 - 0.0001
        
        pv2 = pressao_vapor(rm2, patm)
        tbs0 = temperatura_b_seco(e2, rm2)
        pvs2 = pressao_vapor_saturado(tbs2)
        ur2 = pv2 / pvs2
        
        if tbs1 > tbs2:   # tbs > tbs2
            if abs(tbs0 - tbs2) < 0.01:
                break
        elif tbs0 > tbs2:
            break
    
    tpo2 = temperatura_ponto_orvalho(pv2)
    ve2 = volume_especifico(tbs2, rm2, patm)
    
    point2 = {
        'tbs': tbs2,
        'tbm': tbm2,
        'tpo': tpo2,
        'ur': ur2 * 100,
        'rm': rm2 * 1000,
        'pvs': pvs2,
        'pv': pv2,
        've': ve2,
        'e': e2
    }
    
    return {'point1': point1, 'point2': point2}

def calculate_u_adiabatica_ur(tbs1, ur1, ur2, patm):
    """
    Calcula o processo de umidificação adiabática até uma umidade relativa alvo
    
    Args:
        tbs1: Temperatura de bulbo seco inicial (°C)
        ur1: Umidade relativa inicial (decimal)
        ur2: Umidade relativa final (decimal)
        patm: Pressão atmosférica (kPa)
    
    Returns:
        dict: Dicionário com as propriedades dos pontos 1 e 2
    """
    # Ponto de Estado 1
    pvs = pressao_vapor_saturado(tbs1)
    pv = ur1 * pvs
    rm = razao_mistura1(pv, patm)
    e = entalpia(tbs1, rm)
    ve = volume_especifico(tbs1, rm, patm)
    tpo = temperatura_ponto_orvalho(pv)
    tbm = temperatura_b_molhado(tbs1, e, patm)
    
    point1 = {
        'tbs': tbs1,
        'tbm': tbm,
        'tpo': tpo,
        'ur': ur1 * 100,
        'rm': rm * 1000,
        'pvs': pvs,
        'pv': pv,
        've': ve,
        'e': e
    }
    
    # Ponto de estado 2
    e2 = e
    tbm2 = tbm
    rm2 = rm
    
    # Ajuste da razão de mistura até atingir a umidade relativa desejada
    iterations = 0
    max_iterations = 1000
    
    while iterations < max_iterations:
        iterations += 1
        
        rm2 = rm2 + 0.0001
        pv2 = pressao_vapor(rm2, patm)
        tbs2 = temperatura_b_seco(e2, rm2)
        pvs2 = pressao_vapor_saturado(tbs2)
        ur0 = pv2 / pvs2
        
        if ur0 >= ur2 or abs(ur0 - ur2) < 0.001:
            break
    
    if ur2 >= 0.99:
        tbs2 = tbm
        tpo2 = tbm
        pvs2 = pressao_vapor_saturado(tbs2)
        pv2 = pvs2
        rm2 = razao_mistura1(pv2, patm)
    else:
        tpo2 = temperatura_ponto_orvalho(pv2)
    
    ve2 = volume_especifico(tbs2, rm2, patm)
    
    point2 = {
        'tbs': tbs2,
        'tbm': tbm2,
        'tpo': tpo2,
        'ur': ur2 * 100,
        'rm': rm2 * 1000,
        'pvs': pvs2,
        'pv': pv2,
        've': ve2,
        'e': e2
    }
    
    return {'point1': point1, 'point2': point2}

def calculate_u_adiabatica_rm(tbs1, rm1_gkg, rm2_gkg, patm):
    """
    Calcula o processo de umidificação adiabática até uma razão de mistura alvo
    
    Args:
        tbs1: Temperatura de bulbo seco inicial (°C)
        rm1_gkg: Razão de mistura inicial (g/kg)
        rm2_gkg: Razão de mistura final (g/kg)
        patm: Pressão atmosférica (kPa)
    
    Returns:
        dict: Dicionário com as propriedades dos pontos 1 e 2
    """
    # Converter g/kg para decimal
    rm1 = rm1_gkg / 1000.0
    rm2 = rm2_gkg / 1000.0
    
    # Ponto de Estado 1
    pvs = pressao_vapor_saturado(tbs1)
    pv = pressao_vapor(rm1, patm)
    ur = pv / pvs
    
    if ur > 1.0:
        return {'error': 'O valor da razão de mistura do ponto 1 é muito alto'}
    
    e = entalpia(tbs1, rm1)
    ve = volume_especifico(tbs1, rm1, patm)
    tpo = temperatura_ponto_orvalho(pv)
    tbm = temperatura_b_molhado(tbs1, e, patm)
    
    point1 = {
        'tbs': tbs1,
        'tbm': tbm,
        'tpo': tpo,
        'ur': ur * 100,
        'rm': rm1 * 1000,
        'pvs': pvs,
        'pv': pv,
        've': ve,
        'e': e
    }
    
    # Ponto de Estado 2
    e2 = e
    tbm2 = tbm
    tbs2 = temperatura_b_seco(e2, rm2)
    pvs2 = pressao_vapor_saturado(tbs2)
    pv2 = pressao_vapor(rm2, patm)
    ur2 = pv2 / pvs2
    
    if ur2 > 1.0:
        return {'error': 'O valor da razão de mistura fornecida no ponto 2 é muito alta'}
    
    tpo2 = temperatura_ponto_orvalho(pv2)
    ve2 = volume_especifico(tbs2, rm2, patm)
    
    if ur2 >= 1.0:
        ur2 = 0.99999
        tbs2 = tbm2
        tpo2 = tbm2
        pvs2 = pressao_vapor_saturado(tbs2)
        pv2 = pvs2
        rm2 = razao_mistura1(pv2, patm)
        ve2 = volume_especifico(tbs2, rm2, patm)
    
    point2 = {
        'tbs': tbs2,
        'tbm': tbm2,
        'tpo': tpo2,
        'ur': ur2 * 100,
        'rm': rm2 * 1000,
        'pvs': pvs2,
        'pv': pv2,
        've': ve2,
        'e': e2
    }
    
    return {'point1': point1, 'point2': point2}

def calculate_mistura_fluxos(tbs1, ur1, q1, tbs2, ur2, q2, patm):
    """
    Calcula a mistura de dois fluxos de ar
    
    Args:
        tbs1: Temperatura de bulbo seco do fluxo 1 (°C)
        ur1: Umidade relativa do fluxo 1 (decimal)
        q1: Vazão de ar do fluxo 1 (m³/h)
        tbs2: Temperatura de bulbo seco do fluxo 2 (°C)
        ur2: Umidade relativa do fluxo 2 (decimal)
        q2: Vazão de ar do fluxo 2 (m³/h)
        patm: Pressão atmosférica (kPa)
    
    Returns:
        dict: Dicionário com as propriedades dos três pontos (fluxo 1, fluxo 2 e mistura)
    """
    # Fluxo de ar 1
    pvs1 = pressao_vapor_saturado(tbs1)
    pv1 = ur1 * pvs1
    rm1 = razao_mistura1(pv1, patm)
    e1 = entalpia(tbs1, rm1)
    ve1 = volume_especifico(tbs1, rm1, patm)
    tpo1 = temperatura_ponto_orvalho(pv1)
    tbm1 = temperatura_b_molhado(tbs1, e1, patm)
    
    m1 = q1 / ve1  # massa de ar seco (kg/h)
    
    point1 = {
        'tbs': tbs1,
        'tbm': tbm1,
        'tpo': tpo1,
        'ur': ur1 * 100,
        'rm': rm1 * 1000,
        'pvs': pvs1,
        'pv': pv1,
        've': ve1,
        'e': e1,
        'q': q1,
        'm': m1
    }
    
    # Fluxo de ar 2
    pvs2 = pressao_vapor_saturado(tbs2)
    pv2 = ur2 * pvs2
    rm2 = razao_mistura1(pv2, patm)
    e2 = entalpia(tbs2, rm2)
    ve2 = volume_especifico(tbs2, rm2, patm)
    tpo2 = temperatura_ponto_orvalho(pv2)
    tbm2 = temperatura_b_molhado(tbs2, e2, patm)
    
    m2 = q2 / ve2  # massa de ar seco (kg/h)
    
    point2 = {
        'tbs': tbs2,
        'tbm': tbm2,
        'tpo': tpo2,
        'ur': ur2 * 100,
        'rm': rm2 * 1000,
        'pvs': pvs2,
        'pv': pv2,
        've': ve2,
        'e': e2,
        'q': q2,
        'm': m2
    }
    
    # Ar resultante da mistura
    m3 = m1 + m2
    rm3 = (m1 * rm1 + m2 * rm2) / m3
    e3 = (m1 * e1 + m2 * e2) / m3
    
    # Calcular tbs3 a partir de e3 e rm3
    tbs3 = temperatura_b_seco(e3, rm3)
    
    # Demais propriedades do ponto 3
    pvs3 = pressao_vapor_saturado(tbs3)
    pv3 = pressao_vapor(rm3, patm)
    ur3 = pv3 / pvs3
    ve3 = volume_especifico(tbs3, rm3, patm)
    tpo3 = temperatura_ponto_orvalho(pv3)
    tbm3 = temperatura_b_molhado(tbs3, e3, patm)
    
    q3 = m3 * ve3
    
    point3 = {
        'tbs': tbs3,
        'tbm': tbm3,
        'tpo': tpo3,
        'ur': ur3 * 100,
        'rm': rm3 * 1000,
        'pvs': pvs3,
        'pv': pv3,
        've': ve3,
        'e': e3,
        'q': q3,
        'm': m3
    }
    
    return {
        'point1': point1, 
        'point2': point2, 
        'point3': point3,
        'q1': q1,
        'q2': q2,
        'q3': q3
    }
