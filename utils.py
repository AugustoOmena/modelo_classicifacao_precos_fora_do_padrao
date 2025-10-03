"""
Utilitários para formatação de números no padrão brasileiro
"""
import pandas as pd

def formatar_moeda(valor):
    """
    Formata valor para moeda brasileira (R$ 1.234,56)
    
    Args:
        valor (float): Valor a ser formatado
    
    Returns:
        str: Valor formatado em moeda brasileira
    """
    if pd.isna(valor):
        return "R$ 0,00"
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def formatar_numero(valor, decimais=0):
    """
    Formata número com separadores brasileiros (1.234.567,89)
    
    Args:
        valor (float): Valor a ser formatado
        decimais (int): Número de casas decimais (padrão: 0)
    
    Returns:
        str: Número formatado no padrão brasileiro
    """
    if pd.isna(valor):
        return "0"
    if decimais == 0:
        return f"{int(valor):,}".replace(",", ".")
    else:
        return f"{valor:,.{decimais}f}".replace(",", "X").replace(".", ",").replace("X", ".")

def formatar_percentual(valor):
    """
    Formata percentual brasileiro (12,34%)
    
    Args:
        valor (float): Valor percentual a ser formatado
    
    Returns:
        str: Percentual formatado no padrão brasileiro
    """
    if pd.isna(valor):
        return "0,00%"
    return f"{valor:,.2f}%".replace(",", "X").replace(".", ",").replace("X", ".")

def formatar_milhares(valor):
    """
    Formata números grandes de forma mais legível (1,2M, 1,5K)
    
    Args:
        valor (float): Valor a ser formatado
    
    Returns:
        str: Valor formatado de forma compacta
    """
    if pd.isna(valor):
        return "0"
    
    if valor >= 1_000_000:
        return f"{valor/1_000_000:,.1f}M".replace(",", "X").replace(".", ",").replace("X", ".")
    elif valor >= 1_000:
        return f"{valor/1_000:,.1f}K".replace(",", "X").replace(".", ",").replace("X", ".")
    else:
        return formatar_numero(valor)