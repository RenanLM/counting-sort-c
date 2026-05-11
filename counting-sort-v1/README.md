# Counting Sort V1

Implementação em C do algoritmo **Counting Sort** para execução em PC, leitura de dados por arquivo texto e validação da ordenação com Python.

## Sumário

- [Sobre a Versão](#sobre-a-versão)
- [Contexto Acadêmico](#contexto-acadêmico)
- [Estrutura de Arquivos](#estrutura-de-arquivos)
- [Detalhes Técnicos](#detalhes-técnicos)
- [Algoritmo Implementado](#algoritmo-implementado)
- [Como Executar](#como-executar)
- [Entrada e Saída](#entrada-e-saída)
- [Validação](#validação)
- [Autores](#autores)

## Sobre a Versão

A versão 1 foi criada para validar o funcionamento do Counting Sort em um ambiente de PC antes da portabilidade para sistema embarcado. O programa lê até 8000 inteiros de um arquivo, ordena os valores em ordem crescente, mede o tempo de execução e grava a saída ordenada em outro arquivo.

## Contexto Acadêmico

Esta etapa faz parte do projeto da disciplina de **Sistemas Embarcados** e corresponde à fase de implementação e validação inicial do algoritmo.

#### **Objetivos da v1**

- Projetar o Counting Sort de forma correta.
- Definir entrada, saída e limites do algoritmo.
- Implementar a ordenação em C.
- Gerar dados de teste automaticamente.
- Comparar o resultado em C com a ordenação nativa do Python.

## Estrutura de Arquivos

```text
counting-sort-v1/
│
├── README.md                 # Este arquivo
├── countingSort.c            # Programa principal em C
├── dados.py                  # Gera dados_teste.txt com inteiros aleatórios
├── validar_ordenacao.py      # Compara lista_ordenada.txt com sort do Python
└── teste.py                  # Validador alternativo usando NumPy
```

## Detalhes Técnicos

- **Linguagem principal**: C
- **Scripts auxiliares**: Python 3
- **Plataforma alvo**: Windows
- **Compilador recomendado**: GCC/MinGW
- **Quantidade máxima de elementos**: 8000
- **Valor mínimo aceito**: -10000
- **Valor máximo aceito**: 10000
- **Medição de desempenho**: `QueryPerformanceCounter` da Windows API

## Algoritmo Implementado

1. O arquivo `dados_teste.txt` é aberto para leitura.
2. A primeira linha de comentário é ignorada.
3. Os inteiros são carregados em um vetor de tamanho fixo.
4. O programa identifica o menor e o maior valor da lista.
5. Caso existam valores negativos, os dados são deslocados temporariamente para índices positivos.
6. O vetor de contagem registra a quantidade de ocorrências de cada valor.
7. A lista ordenada é reconstruída em ordem crescente.
8. O deslocamento dos negativos é revertido, quando necessário.
9. A saída é salva em `lista_ordenada.txt`.

## Como Executar

1. Gere os dados de entrada:

```bash
   python dados.py
```
2. Compile o programa em C no Windows:

```bash
   gcc countingSort.c -o countingSort.exe
```

3. Execute a aplicação:

```bash
   countingSort.exe
```

4. Valide o resultado com Python:

```bash
   python validar_ordenacao.py
```

## Entrada e Saída

- **Entrada**: `dados_teste.txt`, contendo uma linha inicial de comentário e, em seguida, um inteiro por linha.
- **Saída do C**: `lista_ordenada.txt`, contendo os inteiros ordenados em ordem crescente.
- **Saída do Python**: `lista_ordenada_python.txt`, usada como referência para validação.

## Validação

O script `validar_ordenacao.py` lê os dados originais, ordena uma cópia com o `sort` do Python e compara o resultado com a saída gerada pelo programa em C.

Se todos os elementos estiverem na mesma ordem, a validação informa que a saída do Counting Sort em C está correta.

## Autores

- Larissa Sales Trece
- Renan Lucas de Moura