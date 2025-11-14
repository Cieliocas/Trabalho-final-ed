import time
import re
from collections import deque, Counter, OrderedDict, defaultdict
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
    init = time.time()

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
        tipoEstrutura = defaultdict(list)
        for w in words:
            tipoEstrutura[w].append(1)

    elif estrutura == 'tuple':
        tipoEstrutura = tuple()
        for w in words:
            list_temp = list(tipoEstrutura)
            list_temp.append(w)
            tipoEstrutura = tuple(list_temp)
    end = time.time()
    return f"{end - init:.3f}"

word = ler_arquivo('leipzig100k.txt')
estruturas = ['tuple', 'list', 'set', 'dict', 'deque', 'defaultdict']
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
