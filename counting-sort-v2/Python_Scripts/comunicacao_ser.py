import serial
import serial.tools.list_ports
import struct
import random
import time
import sys
import os

# Constantes de configuração
TOTAL_ELEMENTOS = 8000
CHUNK_SIZE = 100
BAUD_RATE = 115200
PASTA_RESULTADOS = "resultados_ordenacao"

def list_serial_ports():
    """Lista todas as portas seriais disponíveis."""
    ports = serial.tools.list_ports.comports()
    if not ports:
        print("Nenhuma porta serial encontrada!")
        return None

    print("\n=== Portas Seriais Disponíveis ===")
    for i, port in enumerate(ports):
        print(f"{i}: {port.device} - {port.description}")

    return ports

def select_port(ports):
    """Permite ao usuário selecionar uma porta serial."""
    if len(ports) == 1:
        print(f"\nUsando porta padrão: {ports[0].device}")
        return ports[0].device

    while True:
        try:
            choice = int(input("\nEscolha o número da porta: "))
            if 0 <= choice < len(ports):
                return ports[choice].device
            else:
                print("Número inválido!")
        except ValueError:
            print("Digite um número válido!")

def salvar_lista_txt(lista, nome_arquivo):
    """Salva uma lista de inteiros em um arquivo .txt, um por linha."""
    caminho_completo = os.path.join(PASTA_RESULTADOS, nome_arquivo)
    try:
        with open(caminho_completo, 'w', encoding='utf-8') as f:
            for item in lista:
                f.write(f"{item}\n")
        return caminho_completo
    except Exception as e:
        print(f"Erro ao salvar o arquivo {nome_arquivo}: {e}")
        return None

def main():
    # Cria a pasta para salvar os arquivos .txt se ela não existir
    os.makedirs(PASTA_RESULTADOS, exist_ok=True)
    print(f"[*] Pasta de trabalho preparada: ./{PASTA_RESULTADOS}/")

    # Gera os dados de entrada
    entrada = [random.randint(-1000, 1000) for _ in range(TOTAL_ELEMENTOS)]
    
    # Salva os dados brutos gerados
    arq_entrada = salvar_lista_txt(entrada, "1_entrada_desordenada.txt")
    
    # Ordena com Python e salva
    entrada_ordenada_python = sorted(entrada)
    arq_python = salvar_lista_txt(entrada_ordenada_python, "2_ordenado_python.txt")

    formato_chunk = f"<{CHUNK_SIZE}h"
    total_chunks = TOTAL_ELEMENTOS // CHUNK_SIZE

    ports = list_serial_ports()
    if not ports:
        sys.exit(1)

    port = select_port(ports)

    try:
        print(f"\n=== Conectando em {port} (115200 baud) ===")
        with serial.Serial(port, BAUD_RATE, timeout=10) as ser:
            time.sleep(2)  # Aguarda estabilização da conexão
            print("OK Conexão estabelecida\n")
            
            print("=" * 50)
            print(f"FASE 1: Enviando {TOTAL_ELEMENTOS} números em blocos de {CHUNK_SIZE}")
            print("=" * 50)
            
            # 1. Envio de blocos
            for i in range(total_chunks):
                start_idx = i * CHUNK_SIZE
                chunk = entrada[start_idx : start_idx + CHUNK_SIZE]
                bytes_chunk = struct.pack(formato_chunk, *chunk)
                
                ser.write(bytes_chunk)
                ser.flush()
                
                # Exibe o progresso na mesma linha do terminal
                if (i + 1) % 10 == 0 or i == total_chunks - 1:
                    print(f"  Enviados {i + 1}/{total_chunks} blocos", end='\r')
                
                time.sleep(0.01)
            
            print("\n\nOK Envio concluído. Aguardando processamento...")

            print("\n" + "=" * 50)
            print("FASE 2: Recebendo dados ordenados da STM32")
            print("=" * 50)
            
            saida_ordenada_stm = []
            bytes_esperados = CHUNK_SIZE * 2
            
            # 2. Recebimento de blocos
            for i in range(total_chunks):
                bytes_saida = ser.read(bytes_esperados)
                
                # Validação de recebimento do pacote
                if len(bytes_saida) != bytes_esperados:
                    print(f"\n\n[ERRO] Timeout! Esperava {bytes_esperados} bytes, mas recebeu {len(bytes_saida)}.")
                    print("A placa possivelmente travou. Aperte o botão RESET na placa e tente novamente.")
                    sys.exit(1)
                    
                chunk_recebido = struct.unpack(formato_chunk, bytes_saida)
                saida_ordenada_stm.extend(chunk_recebido)
                
                # Exibe o progresso de recebimento
                if (i + 1) % 10 == 0 or i == total_chunks - 1:
                    print(f"  Recebidos {i + 1}/{total_chunks} blocos", end='\r')

            print("\n\n" + "=" * 50)
            print("OK PROCESSAMENTO COMPLETO")
            print("=" * 50)

            # Salva o resultado retornado pela placa
            arq_stm = salvar_lista_txt(saida_ordenada_stm, "3_ordenado_stm32.txt")

    except serial.SerialException as e:
        print(f"\nERRO na comunicação serial: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nInterrompido pelo usuário!")
        sys.exit(0)

    # 3. Validar ordenação (Comparação entre listas que reflete o conteúdo dos TXT)
    print("\n" + "=" * 50)
    print("VALIDAÇÃO DOS DADOS")
    print("=" * 50)
    
    if list(saida_ordenada_stm) == entrada_ordenada_python:
        print(f"[SUCESSO] O STM32F030 conseguiu ordenar os {TOTAL_ELEMENTOS} elementos corretamente!")
        print("\nOs arquivos gerados para conferência manual são idênticos e estão localizados em:")
        print(f" -> {arq_python}")
        print(f" -> {arq_stm}")
    else:
        print("[FALHA] A lista não foi ordenada corretamente.")
        print("\nVerifique os arquivos gerados para entender a divergência:")
        print(f" -> Esperado (Python): {arq_python}")
        print(f" -> Obtido (STM32):  {arq_stm}")

if __name__ == "__main__":
    main()