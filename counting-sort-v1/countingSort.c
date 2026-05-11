/**
 * @file countingSort.c
 * @brief Implementação do algoritmo Counting Sort para ordenar inteiros lidos de arquivo.
 *
 * @details
 * Aplicação acadêmica desenvolvida para demonstrar o uso do algoritmo Counting Sort
 * em C, simulando seu funcionamento em um Soc,
 * incluindo leitura de dados de arquivo, medição de desempenho e gravação da
 * saída ordenada.
 *
 * Copyright (c) 2026.
 * Permissão de uso, cópia, modificação e distribuição concedida conforme os termos
 * do arquivo LICENSE deste repositório.
 *
 * @section uso Como usar
 * 1. Gere dados de entrada com: `python dados.py`
 * 2. Compile no Windows (alvo principal):
 *    `gcc countingSort.c -o countingSort.exe`
 * 3. Execute: `countingSort.exe`
 * 4. O resultado será salvo em `lista_ordenada.txt`.
 *
 * @section io Entrada e saída
 * Entrada: arquivo texto `dados_teste.txt` com inteiros (um por linha),
 * podendo conter uma primeira linha de comentário.
 * Saída: arquivo texto `lista_ordenada.txt` com inteiros em ordem crescente.
 *
 * @section contexto Contexto de desenvolvimento
 * Trabalho de disciplina voltado ao estudo de algoritmos de ordenação e análise de
 * desempenho.
 *
 * @section autores Autores/estudantes
 * Larissa Sales Trece
 * Renan Lucas de Moura
 *
 * @date 2026-04-30
 * @platform Plataforma alvo: Windows (uso de QueryPerformanceCounter/Windows API).
 */

#include <stdio.h>
#include <stdlib.h>
#include <windows.h>

/** @brief Quantidade máxima de elementos suportados no vetor de entrada. */
#define MAX_ELEMENTS 8000

/** @brief Maior valor permitido na entrada. */
#define MAX_VALUE 10000
/** @brief Menor valor permitido na entrada. */ 
#define MIN_VALUE -10000

/**
 * @brief Ordena um vetor de inteiros em ordem crescente usando Counting Sort.
 *
 * @details
 * A função aceita números negativos através de um deslocamento temporário dos dados
 * quando o menor valor é negativo. Após a ordenação, o deslocamento é revertido.
 *
 * @param[in,out] lista Vetor de inteiros a ser ordenado (modificado in-place).
 * @param[in] size Quantidade de elementos válidos em `lista`.
 *
 * @return Não retorna valor.
 *
 * @note Variáveis globais afetadas: nenhuma.
 */
void counting_sort(int lista[], int size) {

    // Verificação de segurança para evitar estouro de buffer
    if (size <= 0 || size > MAX_ELEMENTS) { 
        printf("Erro: Tamanho da lista deve ser entre 1 e %d.\n", MAX_ELEMENTS);
        return; 
    }

    // Array de saída (resultado ordenado)
    int saida[MAX_ELEMENTS];
    // Array de contagem para armazenar a contagem de cada elemento
    int count[MAX_VALUE - MIN_VALUE + 1];

    // For para encontrar o valor máximo na lista
    int max = lista[0];
    for (int i = 1; i < size; i++) {
        if (lista[i] > max) {
            max = lista[i];
        }
    }

    // For para encontrar o valor mínimo na lista
    int min = lista[0];
    for (int i = 1; i < size; i++) {
        if (lista[i] < min) {
            min = lista[i];
        }
    }

    // If para verificar se o valor mínimo é negativo
    if (min < 0) {
        // Ajustar os valores para que sejam positivos
        for (int i = 0; i < size; i++) {
            lista[i] -= min;
        }
        max -= min; // Ajustar o valor máximo também
    }

    // Inicializar o array de contagem
   for (int i = 0; i <= max; i++) {
        count[i] = 0;
    }

    // Contar cada elemento da lista
    for (int i = 0; i < size; i++) {
        count[lista[i]]++;
    }

    // Modificar o array de contagem para que ele contenha a posição de cada elemento no array de saída
    for (int i = 1; i <= max; i++) {
        count[i] += count[i - 1];
    }

    // Construir o array de saída
    for (int i = size - 1; i >= 0; i--) {
        saida[count[lista[i]] - 1] = lista[i];
        count[lista[i]]--;
    }
    
    // Copiar o array de saída para a lista original, agora ordenada
    for (int i = 0; i < size; i++) {
        lista[i] = saida[i];
    }

    // Se os valores foram ajustados para serem positivos, reverter o ajuste
    if (min < 0) {
        for (int i = 0; i < size; i++) {
            lista[i] += min;
        }
    }
}

/**
 * @brief Função principal da aplicação.
 *
 * @details
 * Lê os dados do arquivo de entrada, executa a ordenação, mede tempo de execução,
 * valida se o vetor está ordenado e grava o resultado em arquivo.
 *
 * @param[in] argc Quantidade de argumentos de linha de comando (não utilizado).
 * @param[in] argv Vetor de argumentos de linha de comando (não utilizado).
 *
 * @return `0` em sucesso, `1` em erro de leitura do arquivo de entrada.
 *
 * @note Variáveis globais afetadas: nenhuma.
 */

int main() {
    // Definir o número de elementos a serem ordenados e criar a lista para armazenar os dados
    int n = MAX_ELEMENTS;
    int lista[MAX_ELEMENTS];

    // Abrir e ler arquivo com dados de teste, desconsiderando a primeira linha do arquivo
    FILE *arquivo = fopen("dados_teste.txt", "r");
    if (arquivo == NULL) {
        printf("Erro: Não foi possivel abrir o arquivo de entrada.\n");
        return 1;
    }
    else {
        int i = 0;
        // Ler a primeira linha (comentário) e descartá-la
        char linha[256];
        fgets(linha, sizeof(linha), arquivo);
        while (i < n && fscanf(arquivo, "%d", &lista[i]) == 1) {
            i++;
        }
        fclose(arquivo);
    }

    // Medir o tempo de execução do counting sort
    LARGE_INTEGER frequency;
    LARGE_INTEGER start;
    LARGE_INTEGER end;
    QueryPerformanceFrequency(&frequency);
    QueryPerformanceCounter(&start);
    
    // Ordenando
    counting_sort(lista, n);

    // Fim da ordenação
    QueryPerformanceCounter(&end);

    // Calcular o tempo em milissegundos
    double time_taken_ms = (double)(end.QuadPart - start.QuadPart) * 1000.0 / (double)frequency.QuadPart;
    printf("Tempo de execucao do counting sort para %d elementos: %.3f ms\n", n, time_taken_ms);

    // Verificar se a lista está ordenada corretamente
    int ordenado = 1;
    for(int i = 1; i < n; i++) { 
        if(lista[i] < lista[i-1]) {
            ordenado = 0;
            break;
        }
    }
    // Imprimir o resultado da verificação e salvar a lista ordenada em um arquivo de saída
    if(ordenado) {
        printf("Lista ordenada com sucesso.\n");

        printf("Salvando dados no arquivo...\n");
 
        FILE *arquivo = fopen("lista_ordenada.txt", "w");
        
        if (arquivo == NULL) {
            printf("Erro: Nao foi possivel criar o arquivo de saida.\n");
        } else {
            
            for (int i = 0; i < n; i++) {
                fprintf(arquivo, "%d\n", lista[i]);
            }
            
            fclose(arquivo);
            printf("Sucesso! Dados salvos em 'lista_ordenada.txt'.\n");
        }
    } else {
        printf("Não foi possível ordenar a lista.\n");
    }

    return 0;
}