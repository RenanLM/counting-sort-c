import serial
import struct
import random
import time

TOTAL_ELEMENTOS = 8000
CHUNK_SIZE = 100
PORTA_COM = "COM4"
BAUD_RATE = 115200

def comunicar_com_placa():
    entrada = [random.randint(-1000, 1000) for _ in range(TOTAL_ELEMENTOS)]
    
    # teste todos iguais:
    # entrada = [0] * TOTAL_ELEMENTOS
    # entrada = [-1000] * TOTAL_ELEMENTOS
    # entrada = [1000] * TOTAL_ELEMENTOS

    # entrada = [-1000, 1000] * 4000
    
    '''
    entrada = list(range(-1000, 1001))
    entrada = (entrada * ((8000 // len(entrada)) + 1))[:8000]
    random.shuffle(entrada)
    '''

    formato_chunk = f"<{CHUNK_SIZE}h"
    
    with serial.Serial(PORTA_COM, BAUD_RATE, timeout=10) as ser:
        time.sleep(1)
        print(f"Enviando {TOTAL_ELEMENTOS} números em blocos de {CHUNK_SIZE}...")
        
        # 1. Envia os blocos em intervalos para evitar sobrecarregar a placa
        for i in range(0, TOTAL_ELEMENTOS, CHUNK_SIZE):
            chunk = entrada[i : i + CHUNK_SIZE]
            bytes_chunk = struct.pack(formato_chunk, *chunk)
            ser.write(bytes_chunk)
            
            time.sleep(0.01) 
            
        print("Dados enviados! Aguardando ordenação...")
        
        saida_ordenada = []
        
        # 2. Recebe os blocos processados
        for i in range(0, TOTAL_ELEMENTOS, CHUNK_SIZE):
            bytes_saida = ser.read(CHUNK_SIZE * 2)

            
            # Proteção: verifica se recebeu o pacote inteiro antes de desempacotar
            if len(bytes_saida) != CHUNK_SIZE * 2:
                print(f"\n[ERRO] Timeout! Esperava 200 bytes, mas recebeu apenas {len(bytes_saida)}.")
                print("Aperte o botão RESET e tente novamente.")
                return

            chunk_recebido = struct.unpack(formato_chunk, bytes_saida)
            print(chunk_recebido)
            saida_ordenada.extend(chunk_recebido)
            

    # 3. Validar ordenação
    entrada_ordenada_python = sorted(entrada)
    if list(saida_ordenada) == entrada_ordenada_python:
        print(f"\n[SUCESSO] O STM32F030 conseguiu ordenar os {TOTAL_ELEMENTOS} elementos!")
    else:
        print("\n[FALHA] A lista não foi ordenada corretamente.")

if __name__ == "__main__":
    comunicar_com_placa()