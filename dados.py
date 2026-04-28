import random

QUANTIDADE = 8000
VALOR_MAXIMO = 10000
VALOR_MINIMO = -10000

with open("dados_teste.txt", "w", encoding="utf-8") as f:
    f.write(f"// Arquivo gerado automaticamente com {QUANTIDADE} inteiros\n")
    
    for i in range(QUANTIDADE):
        # Gera um número entre 0 e 10000
        num = random.randint(VALOR_MINIMO, VALOR_MAXIMO)
        f.write(f"{num}\n")

print("Arquivo 'dados_teste.txt' gerado com sucesso!")