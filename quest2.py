import time
import re
from collections import deque, namedtuple, defaultdict
import matplotlib.pyplot as plt

#Ler aquivo
def ler_arquivo(file):
    with open(file, 'r', encoding='utf-8') as arq:
        arquivo = arq.read()
        padrao = r"[ \t\n,.;!?()\"]+"  

    palavras = [p for p in re.split(padrao, arquivo) if p]
    return palavras

#Calcula o tempo da inserção de cada collections:
def tempo_insercao(words, estrutura):
    init = time.perf_counter()

    if estrutura == 'list':
        tipoEstrutura = list()
        for w in words:
            tipoEstrutura.append(w)

    elif estrutura == 'set':
        tipoEstrutura = set()
        for w in words:
            tipoEstrutura.add(w)

    elif estrutura == 'dict':
        tipoEstrutura = dict()
        for i, w in enumerate(words):
            tipoEstrutura[w] = i

    elif estrutura == 'deque':
        tipoEstrutura = deque()
        for w in words:
            tipoEstrutura.append(w)

    elif estrutura == 'defaultdict':
        tipoEstrutura = defaultdict(int)
        for w in words:
            tipoEstrutura[w] += 1

    elif estrutura == 'namedtuple':
        tipoEstrutura = list()
        tipo = namedtuple('Estrutura', ['Valor'])
        for w in words:
            obj = tipo(w)
            tipoEstrutura.append(obj)

    end = time.perf_counter()
    return f"{end - init:.3f}"

word = ler_arquivo('leipzig100k.txt')
estruturas = ['list', 'set', 'dict', 'deque', 'defaultdict', 'namedtuple']
tempos = dict()

for estrutura in estruturas:
    tempo = tempo_insercao(word, estrutura)
    tempos[estrutura] = float(tempo)

print(tempos)

estruturas = list(tempos.keys())
valores = list(tempos.values())

plt.figure(figsize=(10, 6))
plt.bar(estruturas, valores)
plt.xlabel('Estrutura de Dados')
plt.ylabel('Tempo (segundos)')
plt.title('Tempo de Inserção de 140.000 palavras')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
