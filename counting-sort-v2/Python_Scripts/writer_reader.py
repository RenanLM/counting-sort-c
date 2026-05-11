import serial
import serial.tools.list_ports
import struct
import random
import time
import sys

TOTAL_ELEMENTOS = 8000
CHUNK_SIZE = 100
BAUD_RATE = 115200

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

def main():
    entrada = [random.randint(-1000, 1000) for _ in range(TOTAL_ELEMENTOS)]
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
            print("FASE 2: Recebendo dados ordenados")
            print("=" * 50)
            
            saida_ordenada = []
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
                saida_ordenada.extend(chunk_recebido)
                
                # Exibe o progresso de recebimento
                if (i + 1) % 10 == 0 or i == total_chunks - 1:
                    print(f"  Recebidos {i + 1}/{total_chunks} blocos", end='\r')

            print("\n\n" + "=" * 50)
            print("OK PROCESSAMENTO COMPLETO")
            print("=" * 50)

    except serial.SerialException as e:
        print(f"\nERRO na comunicação serial: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nInterrompido pelo usuário!")
        sys.exit(0)

    # 3. Validar ordenação
    entrada_ordenada_python = sorted(entrada)
    if list(saida_ordenada) == entrada_ordenada_python:
        print(f"\n[SUCESSO] O STM32F030 conseguiu ordenar os {TOTAL_ELEMENTOS} elementos corretamente!")
    else:
        print("\n[FALHA] A lista não foi ordenada corretamente.")

if __name__ == "__main__":
    main()