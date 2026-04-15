import random

QUANTIDADE = 8000
VALOR_MAXIMO = 10000

with open("dados_teste.h", "w") as f:
    f.write(f"// Arquivo gerado automaticamente com {QUANTIDADE} inteiros\n")
    f.write(f"int lista[{QUANTIDADE}] = {{\n    ")
    
    for i in range(QUANTIDADE):
        # Gera um número entre 0 e 10000
        num = random.randint(0, VALOR_MAXIMO)
        f.write(f"{num}")
        
        if i < QUANTIDADE - 1:
            f.write(", ")
            
        # Quebra de linha a cada 15 números
        if (i + 1) % 15 == 0:
            f.write("\n    ")
            
    f.write("\n};\n")

print("Arquivo 'dados_teste.h' gerado com sucesso!")