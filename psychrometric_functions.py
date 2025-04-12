import numpy as np
import math

# Funções para os cálculos das propriedades do ar úmido

def pressao_vapor_saturado(t):
    """
    Cálculo da pressão do vapor de saturação
    
    Args:
        t: Temperatura (°C)
    
    Returns:
        p_vs: Pressão de vapor saturado (kPa)
    """
    t = t + 273.16
    if t > 273.16:
        aux = -7511.52 / t + 89.63121 + 0.023998970 * t
        aux = aux - 1.1654551E-5 * (t ** 2) - 1.2810336E-8 * (t ** 3)
        aux = aux + 2.0998405E-11 * (t ** 4) - 12.150799 * np.log(t)
        p_vs = np.exp(aux)
        return p_vs
    else:
        aux = 24.2779 - 6238.64 / t - 0.344438 * np.log(t)
        p_vs = np.exp(aux)
        return p_vs

def razao_mistura1(p, patm):
    """
    Primeiro método de cálculo para razão de mistura
    
    Args:
        p: Pressão parcial de vapor (kPa)
        patm: Pressão atmosférica (kPa)
    
    Returns:
        rm_1: Razão de mistura (decimal)
    """
    rm_1 = 0.62198 * p / (patm - p)
    return rm_1

def razao_mistura2(ts, th, w):
    """
    Segundo método de cálculo para razão de mistura
    
    Args:
        ts: Temperatura de bulbo seco (°C)
        th: Temperatura de bulbo molhado (°C)
        w: Razão de mistura na saturação à temperatura th
    
    Returns:
        rm_2: Razão de mistura (decimal)
    """
    aux1 = (2501. - 2.411 * th) * w - 1.006 * (ts - th)
    aux2 = 2501. + 1.775 * ts - 4.186 * th
    rm_2 = aux1 / aux2
    return rm_2

def umidade_relativa(p, ps):
    """
    Cálculo da Umidade Relativa
    
    Args:
        p: Pressão parcial de vapor (kPa)
        ps: Pressão de vapor saturado (kPa)
    
    Returns:
        u_rel: Umidade relativa (decimal)
    """
    u_rel = p / ps
    return u_rel

def entalpia(t, w):
    """
    Cálculo de Entalpia
    
    Args:
        t: Temperatura (°C)
        w: Razão de mistura (decimal)
    
    Returns:
        h: Entalpia (kJ/kg de ar seco)
    """
    h = 1.006 * t + w * (2501. + 1.775 * t)
    return h

def pressao_vapor(w, patm):
    """
    Cálculo da pressão parcial de vapor
    
    Args:
        w: Razão de mistura (decimal)
        patm: Pressão atmosférica (kPa)
    
    Returns:
        p_vap: Pressão parcial de vapor (kPa)
    """
    p_vap = patm * w / (0.62198 + w)
    return p_vap

def temperatura_ponto_orvalho(p):
    """
    Cálculo da temperatura do ponto de orvalho
    
    Args:
        p: Pressão parcial de vapor (kPa)
    
    Returns:
        t_po: Temperatura do ponto de orvalho (°C)
    """
    a = np.log10(p * 10)  # log10 requires Numpy
    t_po = (186.4905 - 237.3 * a) / (a - 8.2859)
    return t_po

def temperatura_b_molhado(ts, et, patm):
    """
    Cálculo da temperatura do bulbo molhado
    
    Args:
        ts: Temperatura de bulbo seco (°C)
        et: Entalpia (kJ/kg)
        patm: Pressão atmosférica (kPa)
    
    Returns:
        t_bm: Temperatura de bulbo molhado (°C)
    """
    delta = 0.1
    th = ts - delta
    while True:
        rmbs = (et - 1.006 * th) / (2501. + 1.775 * th)
        ps = pressao_vapor_saturado(th)
        urel = (patm * rmbs) / (ps * (0.62198 + rmbs))
        if urel > 1:
            th = th + delta
            delta = delta / 2
        if urel < 0.999:
            th = th - delta
        if 0.999 <= urel < 1:
            break
    t_bm = th
    return t_bm

def temperatura_b_seco(h, w):
    """
    Cálculo da temperatura do bulbo seco
    
    Args:
        h: Entalpia (kJ/kg)
        w: Razão de mistura (decimal)
    
    Returns:
        t_bs: Temperatura de bulbo seco (°C)
    """
    t_bs = (h - 2501. * w) / (1.006 + 1.775 * w)
    return t_bs

def volume_especifico(t, w, patm):
    """
    Cálculo de volume específico
    
    Args:
        t: Temperatura (°C)
        w: Razão de mistura (decimal)
        patm: Pressão atmosférica (kPa)
    
    Returns:
        v_esp: Volume específico (m³/kg)
    """
    r = 0.28705
    t = t + 273.16
    v_esp = r * t / patm * (1 + 1.6078 * w)
    return v_esp

# Funções para converter os resultados em um formato adequado para a interface web

def calculate_from_tbs_ur(tbs, ur, patm):
    """
    Calcula as propriedades psicrométricas a partir da temperatura de bulbo seco e umidade relativa
    
    Args:
        tbs: Temperatura de bulbo seco (°C)
        ur: Umidade relativa (decimal)
        patm: Pressão atmosférica (kPa)
    
    Returns:
        dict: Dicionário com as propriedades calculadas
    """
    pvs = pressao_vapor_saturado(tbs)
    pv = ur * pvs
    rm = razao_mistura1(pv, patm)
    e = entalpia(tbs, rm)
    ve = volume_especifico(tbs, rm, patm)
    
    if ur >= 0.99:
        tpo = tbs
    else:
        tpo = temperatura_ponto_orvalho(pv)
    
    tbm = temperatura_b_molhado(tbs, e, patm)
    
    return {
        'tbs': tbs,
        'tbm': tbm,
        'tpo': tpo,
        'ur': ur * 100,  # Convertido para percentual
        'rm': rm * 1000,  # Convertido para g/kg
        'pvs': pvs,
        'pv': pv,
        've': ve,
        'e': e
    }

def calculate_from_tbs_tbm(tbs, tbm, patm):
    """
    Calcula as propriedades psicrométricas a partir da temperatura de bulbo seco e temperatura de bulbo molhado
    
    Args:
        tbs: Temperatura de bulbo seco (°C)
        tbm: Temperatura de bulbo molhado (°C)
        patm: Pressão atmosférica (kPa)
    
    Returns:
        dict: Dicionário com as propriedades calculadas
    """
    pvs = pressao_vapor_saturado(tbs)
    
    if tbs == tbm:
        ur = 1.0
        tpo = tbs
        pv = pvs
        rm = razao_mistura1(pvs, patm)
    else:
        pvsu = pressao_vapor_saturado(tbm)
        rmsu = razao_mistura1(pvsu, patm)
        rm = razao_mistura2(tbs, tbm, rmsu)
        pv = pressao_vapor(rm, patm)
        ur = umidade_relativa(pv, pvs)
        tpo = temperatura_ponto_orvalho(pv)
    
    e = entalpia(tbs, rm)
    ve = volume_especifico(tbs, rm, patm)
    
    return {
        'tbs': tbs,
        'tbm': tbm,
        'tpo': tpo,
        'ur': ur * 100,  # Convertido para percentual
        'rm': rm * 1000,  # Convertido para g/kg
        'pvs': pvs,
        'pv': pv,
        've': ve,
        'e': e
    }

def calculate_from_tbs_tpo(tbs, tpo, patm):
    """
    Calcula as propriedades psicrométricas a partir da temperatura de bulbo seco e temperatura de ponto de orvalho
    
    Args:
        tbs: Temperatura de bulbo seco (°C)
        tpo: Temperatura de ponto de orvalho (°C)
        patm: Pressão atmosférica (kPa)
    
    Returns:
        dict: Dicionário com as propriedades calculadas
    """
    pvs = pressao_vapor_saturado(tbs)
    
    if tbs == tpo:
        pv = pvs
        ur = 0.999999
        rm = razao_mistura1(pvs, patm)
        e = entalpia(tbs, rm)
        tbm = tbs
    else:
        pv = pressao_vapor_saturado(tpo)
        rm = razao_mistura1(pv, patm)
        ur = umidade_relativa(pv, pvs)
        e = entalpia(tbs, rm)
        tbm = temperatura_b_molhado(tbs, e, patm)
    
    ve = volume_especifico(tbs, rm, patm)
    
    return {
        'tbs': tbs,
        'tbm': tbm,
        'tpo': tpo,
        'ur': ur * 100,  # Convertido para percentual
        'rm': rm * 1000,  # Convertido para g/kg
        'pvs': pvs,
        'pv': pv,
        've': ve,
        'e': e
    }
