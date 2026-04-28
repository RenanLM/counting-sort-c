import numpy as np

# 1. Ler arquivo de entrada
def ler_lista(caminho):
    entrada = []
    with open(caminho, 'r') as f:
        for linha in f:
            linha = linha.strip()
            if linha and (linha.lstrip('-').isdigit()):
                entrada.append(int(linha))
    return entrada


# 2. Ler saída do algoritmo
def ler_saida(caminho):
    saida = []
    with open(caminho, 'r') as f:
        for linha in f:
            linha = linha.strip()
            if linha:
                saida.append(int(linha))
    return saida


# 3. Validar ordenação
def validar(entrada, saida):
    saida_esperada = np.sort(entrada)

    if np.array_equal(saida_esperada, saida):
        print("Ordenação correta!")
    else:
        print("Ordenação incorreta!")

        # mostra primeiros erros
        for i, (a, b) in enumerate(zip(saida_esperada, saida)):
            if a != b:
                print(f"Erro na posição {i}: esperado {a}, recebeu {b}")
                break

entrada = ler_lista("dados_teste.txt")
saida = ler_saida("lista_ordenada.txt")

validar(entrada, saida)