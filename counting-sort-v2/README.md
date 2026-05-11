# Counting Sort v2

Portabilidade do algoritmo **Counting Sort** para sistema embarcado STM32, com envio de dados pelo PC, ordenação na placa e validação do resultado por comunicação serial.

## Sumário

- [Sobre a Versão](#sobre-a-versão)
- [Contexto Acadêmico](#contexto-acadêmico)
- [Estrutura de Arquivos](#estrutura-de-arquivos)
- [Hardware Utilizado](#hardware-utilizado)
- [Detalhes Técnicos](#detalhes-técnicos)
- [Fluxo de Funcionamento](#fluxo-de-funcionamento)
- [Algoritmo Implementado](#algoritmo-implementado)
- [Como Executar](#como-executar)
- [Comunicação Serial](#comunicação-serial)
- [Validação](#validação)
- [Observações Importantes](#observações-importantes)
- [Autores](#autores)

## Sobre a Versão

A versão 2 do projeto adapta o Counting Sort para execução em uma placa **STM32 NUCLEO-F030R8**. Diferente da versão em PC, os dados não são lidos de arquivo: eles são gerados e enviados por um script Python para a placa através da interface serial.

A placa recebe os valores em blocos, contabiliza as ocorrências em um vetor de contagem e transmite a sequência ordenada de volta ao computador. Ao final, o Python compara a resposta da placa com a ordenação nativa da linguagem.

## Contexto Acadêmico

Esta etapa corresponde à fase embarcada do projeto da disciplina de **Sistemas Embarcados**.

#### **Objetivos da v2**

- Portar o Counting Sort para um microcontrolador STM32.
- Trabalhar com restrições de memória e tipos inteiros menores.
- Utilizar comunicação serial para troca de dados entre PC e placa.
- Processar 8000 elementos em blocos de tamanho fixo.
- Validar automaticamente o resultado produzido pelo sistema embarcado.

## Estrutura de Arquivos

```text
counting-sort-v2/
│
├── README.md                         # Este arquivo
├── counting-sort-v2.ioc              # Configuração do projeto no STM32CubeIDE
├── STM32F030R8TX_FLASH.ld            # Script de linker para memória Flash
├── mx.scratch                        # Arquivo auxiliar do STM32CubeIDE
│
├── Core/
│   ├── Inc/                          # Headers principais do firmware
│   │   ├── main.h
│   │   ├── stm32f0xx_hal_conf.h
│   │   └── stm32f0xx_it.h
│   ├── Src/                          # Código-fonte principal do firmware
│   │   ├── main.c                    # Recepção, Counting Sort e transmissão
│   │   ├── stm32f0xx_hal_msp.c
│   │   ├── stm32f0xx_it.c
│   │   ├── syscalls.c
│   │   ├── sysmem.c
│   │   └── system_stm32f0xx.c
│   └── Startup/                      # Código de inicialização do STM32
│
├── Drivers/                          # Bibliotecas HAL e CMSIS
│   ├── CMSIS/
│   └── STM32F0xx_HAL_Driver/
│
└── Python_Scripts/
    ├── writer_reader.py              # Script principal de envio, leitura e validação
    └── comunicacao_ser.py            # Script alternativo com porta COM fixa
```

## Hardware Utilizado

A versão embarcada foi desenvolvida para a placa **NUCLEO-F030R8**.

### Especificações Principais

- **Microcontrolador**: STM32F030R8T6
- **Família**: STM32F0
- **Núcleo**: ARM Cortex-M0
- **Frequência configurada**: 48 MHz
- **Memória Flash**: 64 KB
- **SRAM**: 8 KB
- **Comunicação com o PC**: USART2/UART via porta serial da placa NUCLEO

## Detalhes Técnicos

### Firmware STM32

- **Ambiente de desenvolvimento**: STM32CubeIDE
- **Arquivo de configuração**: `counting-sort-v2.ioc`
- **Firmware base**: STM32Cube FW_F0 V1.11.6
- **Toolchain alvo**: STM32CubeIDE/GCC
- **Arquivo principal**: `Core/Src/main.c`
- **USART utilizada no fluxo com Python**: USART2
- **Total de elementos**: 8000
- **Tamanho de cada bloco**: 100 elementos
- **Tipo dos valores recebidos/enviados**: `int16_t`
- **Faixa de valores aceita pelo algoritmo embarcado**: -1000 a 1000
- **Estrutura de ordenação**: vetor `count` com `RANGE = VALOR_MAXIMO - VALOR_MINIMO + 1`

### Scripts Python

- **Script recomendado**: `Python_Scripts/writer_reader.py`
- **Script alternativo**: `Python_Scripts/comunicacao_ser.py`
- **Biblioteca de comunicação serial**: `pyserial`
- **Formato de empacotamento**: little-endian com inteiros de 16 bits (`struct.pack("<100h", ...)`)
- **Validação**: comparação entre a saída da placa e `sorted(entrada)`

## Fluxo de Funcionamento

1. O script Python gera uma lista com 8000 inteiros aleatórios entre -1000 e 1000.
2. A lista é dividida em blocos de 100 elementos.
3. Cada bloco é empacotado como 100 valores `int16_t` e enviado pela serial.
4. O firmware recebe todos os blocos pela USART2.
5. A placa contabiliza as ocorrências de cada valor no vetor `count`.
6. O firmware reconstrói a lista em ordem crescente.
7. A placa transmite a saída ordenada de volta ao PC em blocos de 100 elementos.
8. O Python desempacota os blocos recebidos e valida a ordenação.

## Algoritmo Implementado

O Counting Sort embarcado usa uma faixa fixa de valores para reduzir o uso de memória e evitar alocação dinâmica.

1. **Inicialização do vetor de contagem**
   - Todas as posições do vetor `count` são zeradas no início de cada ciclo.

2. **Recepção dos dados**
   - O firmware espera `TOTAL_ELEMENTOS / CHUNK_SIZE` blocos pela USART2.
   - Cada bloco recebido possui 100 inteiros de 16 bits.

3. **Mapeamento de valores negativos**
   - Como os valores podem ser negativos, o índice do vetor de contagem é calculado por `buffer[j] - VALOR_MINIMO`.
   - Assim, o valor -1000 é mapeado para o índice 0.

4. **Reconstrução ordenada**
   - O firmware percorre `count` do menor para o maior índice.
   - Cada valor é reconstruído como `i + VALOR_MINIMO`.

5. **Transmissão de saída**
   - A saída ordenada é enviada de volta em blocos de 100 elementos.
   - Cada bloco transmitido possui `CHUNK_SIZE * sizeof(int16_t)` bytes.

## Como Executar

### 1. Abrir e compilar o firmware

1. Abra o **STM32CubeIDE**.
2. Importe ou abra o projeto `counting-sort-v2`.
3. Verifique o arquivo `counting-sort-v2.ioc` e as configurações da USART2.
4. Compile o projeto.
5. Grave o firmware na placa **NUCLEO-F030R8**.

### 2. Preparar o ambiente Python

Instale a dependência de comunicação serial, se necessário:

```bash
pip install pyserial
```

### 3. Executar o teste com a placa conectada

Com a placa conectada ao computador, execute:

```bash
cd counting-sort-v2/Python_Scripts
python writer_reader.py
```

O script lista as portas seriais disponíveis, permite selecionar a porta correta, envia os dados para a placa, recebe a lista ordenada e informa se a validação foi bem-sucedida.

## Comunicação Serial

A troca de dados entre PC e placa ocorre por blocos fixos:

- **Elementos por bloco**: 100
- **Bytes por elemento**: 2 bytes (`int16_t`)
- **Bytes por bloco**: 200 bytes
- **Total de blocos enviados**: 80
- **Total de blocos recebidos**: 80
- **Total de dados transmitidos em cada sentido**: 16000 bytes

> Atenção: o baud rate do script Python e o baud rate configurado no firmware devem ser iguais. O `writer_reader.py` define `BAUD_RATE = 115200`, enquanto o firmware deve ser conferido em `huart2.Init.BaudRate` antes da execução.

## Validação

A validação é feita no próprio script Python:

1. O Python mantém a lista original enviada para a placa.
2. Após receber a resposta do STM32, o script calcula `sorted(entrada)`.
3. A saída recebida é comparada elemento a elemento com a lista ordenada pelo Python.
4. Em caso de igualdade, o terminal exibe uma mensagem de sucesso.

## Observações Importantes

- Os valores enviados devem permanecer dentro da faixa **-1000 a 1000** definida no firmware.
- O total de elementos deve ser múltiplo do tamanho do bloco para manter o protocolo serial simples.
- Caso ocorra timeout na leitura serial, reinicie a placa e execute o script novamente.
- O script `writer_reader.py` é mais flexível porque lista as portas disponíveis; o `comunicacao_ser.py` usa uma porta fixa (`COM4`) e pode exigir ajuste manual.
- A implementação embarcada foi projetada para validação acadêmica do algoritmo e do fluxo PC-placa-PC.

## Autores

- Larissa Sales Trece
- Renan Lucas de Moura