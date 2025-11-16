import time
import re
from collections import deque, defaultdict
import matplotlib.pyplot as plt
import numpy as np # Adicionado para uso na escala logarítmica

# --- Configurações ---
PALAVRAS_EXCLUIR = [
    'Lisbon', 'NASA', 'Kyunghee', 'Konkuk', 'Sogang', 
    'momentarily', 'rubella', 'vaccinations', 'government', 'Authorities'
]
NUM_EXECUCOES = 5  # Número de repetições para o cálculo da média (conforme OBS)
ESTRUTURAS_TESTADAS = ['list', 'set', 'dict', 'deque', 'defaultdict']

# --- Funções Auxiliares ---
def ler_arquivo(file):
    """Lê o arquivo de texto e retorna uma lista de palavras."""
    try:
        with open(file, 'r', encoding='utf-8') as arq:
            arquivo = arq.read()
            padrao = r"[ \t\n,.;!?()\"]+" 
        palavras = [p for p in re.split(padrao, arquivo) if p]
        return palavras
    except FileNotFoundError:
        print(f"ERRO: Arquivo '{file}' não encontrado. Certifique-se de que está na mesma pasta.")
        return []

def inicializar_colecao(words, estrutura):
    """Inicializa e preenche a coleção com todas as palavras (140k)."""
    if estrutura == 'list':
        return list(words)
    elif estrutura == 'set':
        return set(words)
    elif estrutura == 'dict':
        # Dicionário usa a palavra como chave e o índice como valor
        return {w: i for i, w in enumerate(words)}
    elif estrutura == 'deque':
        return deque(words)
    elif estrutura == 'defaultdict':
        colecao = defaultdict(list)
        for w in words:
            colecao[w].append(1)
        return colecao
    return None 

def medir_tempo_exclusao(colecao_base, estrutura):
    """Mede o tempo total para excluir as 10 palavras na estrutura. 
    A colecao_base é copiada para manter a original intacta."""
    
    # Cópia profunda da coleção para garantir que a exclusão não afete o próximo teste
    if estrutura == 'list':
        colecao = colecao_base[:]
    elif estrutura == 'set':
        colecao = colecao_base.copy()
    elif estrutura in ['dict', 'defaultdict']:
        colecao = colecao_base.copy()
    elif estrutura == 'deque':
        colecao = colecao_base.copy()
    else:
        return 0.0

    total_tempo = 0.0
    num_exclusoes = 0

    for w in PALAVRAS_EXCLUIR:
        try:
            init = time.time()
            if estrutura in ['list', 'deque']:
                colecao.remove(w) # O(n) na list; O(n) na deque para itens do meio
            elif estrutura == 'set':
                colecao.discard(w) # O(1)
            elif estrutura in ['dict', 'defaultdict']:
                del colecao[w] # O(1)
            
            end = time.time()
            total_tempo += (end - init)
            num_exclusoes += 1
        except (ValueError, KeyError, IndexError):
            # A palavra não estava na coleção
            pass

    return total_tempo / num_exclusoes if num_exclusoes > 0 else 0.0


# --- Execução Principal (Questão 4) ---
print("--- [ Questão 4 ] Avaliação Temporal: Exclusão ---")

# 1. Carregar as palavras