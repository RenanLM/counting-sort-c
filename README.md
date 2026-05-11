# Counting Sort

Implementação do algoritmo **Counting Sort** em C para ordenação de inteiros, com uma versão de execução em PC e uma versão portada para sistema embarcado STM32. O projeto utiliza scripts Python auxiliares para geração de dados, comunicação serial e validação dos resultados.

## Sumário

- [Sobre o Projeto](#sobre-o-projeto)
- [Contexto Acadêmico](#contexto-acadêmico)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Hardware Utilizado](#hardware-utilizado)
- [Detalhes Técnicos](#detalhes-técnicos)
- [Algoritmo Implementado](#algoritmo-implementado)
- [Como Executar](#como-executar)
- [Licença](#licença)
- [Autores](#autores)

## Sobre o Projeto

O Counting Sort é um algoritmo de ordenação baseado na contagem de ocorrências dos valores de entrada. Em vez de comparar elementos entre si, o algoritmo contabiliza quantas vezes cada valor aparece e reconstrói a lista em ordem crescente.

Neste repositório, o algoritmo foi implementado para ordenar listas de inteiros, incluindo valores negativos, com foco em validação funcional no PC e adaptação para execução em uma placa STM32.

## Contexto Acadêmico

Este projeto foi desenvolvido durante a cadeira de **Sistemas Embarcados** e está dividido em **2 partes**:

#### **Versão 1 (v1)** - Implementação em PC

- Implementar o Counting Sort em C.
- Ler dados de entrada a partir de arquivo texto.
- Medir o tempo de execução do algoritmo.
- Salvar a lista ordenada em arquivo.
- Validar a saída com scripts Python.
- **Objetivo**: garantir a corretude do algoritmo em ambiente de PC antes da portabilidade.

#### **Versão 2 (v2)** - Sistema Embarcado

- Portar o Counting Sort para a placa STM32.
- Receber dados por comunicação serial em blocos.
- Ordenar os elementos usando vetor de contagem em memória embarcada.
- Transmitir os dados ordenados de volta para o PC.
- Validar o resultado recebido com Python.
- **Objetivo**: executar o algoritmo em um sistema embarcado com restrições de memória e comunicação.

## Estrutura do Projeto

```text
project-counting-sort/
│
├── README.md                         # Este arquivo
├── LICENSE                           # Licença GNU GPLv3
│
├── counting-sort-v1/                 # Versão 1 - Implementação em PC
│   ├── README.md                     # Documentação específica da v1
│   ├── countingSort.c                # Aplicação principal em C
│   ├── dados.py                      # Geração de dados aleatórios
│   ├── validar_ordenacao.py          # Validação com sort do Python
│   └── teste.py                      # Validação alternativa com NumPy
│
└── counting-sort-v2/                 # Versão 2 - Sistema Embarcado STM32
    ├── counting-sort-v2.ioc          # Configuração do STM32CubeIDE
    ├── Core/                         # Código-fonte principal gerado/editado
    ├── Drivers/                      # Drivers HAL/CMSIS do STM32
    ├── Python_Scripts/               # Scripts de comunicação serial
    └── STM32F030R8TX_FLASH.ld        # Script de linker da placa
```

## Hardware Utilizado

A placa selecionada para a versão embarcada foi a **NUCLEO-F030R8** da STMicroelectronics.

### Especificações Principais

- **Microcontrolador**: STM32F030R8T6
- **Processador**: ARM Cortex-M0
- **Frequência configurada**: 48 MHz
- **Memória Flash**: 64 KB
- **SRAM**: 8 KB
- **Arquitetura**: 32-bit RISC
- **Comunicação**: UART/Serial via USART2

## Detalhes Técnicos

### Versão PC

- **Linguagem principal**: C
- **Plataforma alvo**: Windows
- **Medição de tempo**: `QueryPerformanceCounter`
- **Quantidade de elementos**: 8000
- **Faixa de valores**: -10000 a 10000
- **Entrada**: `dados_teste.txt`
- **Saída**: `lista_ordenada.txt`

### Versão Embarcada

- **Ambiente**: STM32CubeIDE
- **Firmware base**: STM32Cube FW_F0
- **Quantidade de elementos**: 8000
- **Tamanho dos blocos seriais**: 100 elementos
- **Tipo dos dados transmitidos**: `int16_t`
- **Faixa de valores**: -1000 a 1000
- **Validação**: comparação com `sorted()` do Python no PC

## Algoritmo Implementado

1. **Leitura dos dados**
   - Na v1, os inteiros são lidos de um arquivo texto.
   - Na v2, os inteiros são recebidos pela UART em blocos de 100 elementos.

2. **Contagem das ocorrências**
   - É criado um vetor de contagem com uma posição para cada valor possível da faixa configurada.
   - Para suportar números negativos, a posição no vetor é calculada usando deslocamento pelo menor valor permitido.

3. **Reconstrução ordenada**
   - O vetor de contagem é percorrido em ordem crescente.
   - Cada valor é escrito na saída tantas vezes quanto sua contagem acumulada.

4. **Saída e validação**
   - Na v1, a lista ordenada é salva em arquivo e comparada com o `sort` do Python.
   - Na v2, a placa envia a lista ordenada ao PC, onde o Python valida o resultado recebido.

## Como Executar

### Versão 1 - PC

```bash
cd counting-sort-v1
python dados.py
gcc countingSort.c -o countingSort.exe
./countingSort.exe
python validar_ordenacao.py
```

### Versão 2 - STM32

1. Abra `counting-sort-v2/counting-sort-v2.ioc` no STM32CubeIDE.
2. Compile e grave o firmware na placa **NUCLEO-F030R8**.
3. Conecte a placa ao PC via serial.
4. Execute o script Python de envio, recebimento e validação:

```bash
cd counting-sort-v2/Python_Scripts
python writer_reader.py
```

## Licença

Este projeto está sob a licença **GNU General Public License v3.0**. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Autores

- Larissa Sales Trece
- Renan Lucas de Moura