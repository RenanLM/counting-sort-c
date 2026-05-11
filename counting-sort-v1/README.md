# Counting Sort C

Projeto acadêmico em C para estudo do **Counting Sort** com dados inteiros (incluindo negativos) e validação com Python.

## Visão geral
- Ordena até `8000` inteiros vindos de arquivo texto (`dados_teste.txt`)
- Gera arquivo de saída ordenado (`lista_ordenada.txt`).
- Inclui scripts auxiliares para geração de dados aleatórios e validação.

## Estrutura de arquivos (hierarquia e função)
- `countingSort.c`: aplicação principal em C (leitura, ordenação, validação e escrita da saída).
- `dados.py`: gera o arquivo `dados_teste.txt` com números aleatórios.
- `validar_ordenacao.py`: valida a saída do C comparando com o `sort` do Python.
- `teste.py`: validador alternativo usando NumPy.

## Requisitos
- **Windows** (plataforma alvo da aplicação C atual).
- GCC/MinGW (ou compilador C compatível com `windows.h`).
- Python 3 para scripts auxiliares.

## Como usar
1. Gerar dados:
   ```bash
   python dados.py
   ```
2. Compilar (Windows):
   ```bash
   gcc countingSort.c -o countingSort.exe
   ```
3. Executar:
   ```bash
   countingSort.exe
   ```
4. Validar resultado:
   ```bash
   python validar_ordenacao.py
   ```

## Entrada e saída do algoritmo
- **Entrada:** lista de inteiros (`int`), lida de arquivo texto (`dados_teste.txt`).
- **Saída:** lista de inteiros (`int`) ordenada em ordem crescente, salva em `lista_ordenada.txt`.

## Contexto acadêmico
Este projeto foi realizado como forma de aprendizagem para a disciplina de Sistemas Embarcados, com foco em implementação, limitações de uso, documentação técnica e validação de resultados.