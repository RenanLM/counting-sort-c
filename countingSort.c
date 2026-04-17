#include <stdio.h>
#include <stdlib.h>
#include <windows.h>

// Incluindo o arquivo com os dados de teste
#include "dados_teste.h" 

// Definindo o tamanho máximo da entrada
#define MAX_ELEMENTS 8000

// Definindo o valor máximo esperado dentro da lista. 
#define MAX_VALUE 10000 

// Definindo o valor mínimo esperado dentro da lista. 
#define MIN_VALUE -10000

void counting_sort(int lista[], int size) {

    if (size <= 0 || size > MAX_ELEMENTS) { // Verificação de segurança para evitar estouro de buffer
        printf("Erro: Tamanho da lista deve ser entre 1 e %d.\n", MAX_ELEMENTS);
        return; 
    }

    int saida[MAX_ELEMENTS];
    int count[MAX_VALUE + 1];

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

    // Proteção de segurança: se o número for maior que o buffer de contagem, para a execução
    /* if (max > MAX_VALUE) {
        printf("Erro: Elemento excede o valor máximo permitido para o array count.\n");
        return;
    } */

    for (int i = 0; i <= max; i++) {
        count[i] = 0;
    }

    for (int i = 0; i < size; i++) {
        count[lista[i]]++;
    }

    for (int i = 1; i <= max; i++) {
        count[i] += count[i - 1];
    }

    for (int i = size - 1; i >= 0; i--) {
        saida[count[lista[i]] - 1] = lista[i];
        count[lista[i]]--;
    }

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


int main() {
    int n = MAX_ELEMENTS;

    // Medir o tempo de execução do counting sort
    LARGE_INTEGER frequency;
    LARGE_INTEGER start;
    LARGE_INTEGER end;

    QueryPerformanceFrequency(&frequency);
    QueryPerformanceCounter(&start);
    
    // Ordenando
    counting_sort(lista, n);
    
    QueryPerformanceCounter(&end);

    double time_taken_ms = (double)(end.QuadPart - start.QuadPart) * 1000.0 / (double)frequency.QuadPart;
    printf("Tempo de execucao do counting sort para %d elementos: %.3f ms\n", n, time_taken_ms);

    int ordenado = 1;
    for(int i = 1; i < n; i++) { 
        if(lista[i] < lista[i-1]) {
            ordenado = 0;
            break;
        }
    }

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