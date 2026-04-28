from pathlib import Path

ARQUIVO_ENTRADA = Path("dados_teste.txt")
ARQUIVO_C = Path("lista_ordenada.txt")
ARQUIVO_PY = Path("lista_ordenada_python.txt")


def carregar_dados(caminho: Path) -> list[int]:
    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

    numeros: list[int] = []
    with caminho.open("r", encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if not linha or linha.startswith("//"):
                continue
            numeros.append(int(linha))
    return numeros


def ordenar_com_sort(valores: list[int]) -> list[int]:
    ordenados = valores.copy()
    ordenados.sort()
    return ordenados


def salvar_lista(caminho: Path, numeros: list[int]) -> None:
    with caminho.open("w", encoding="utf-8") as f:
        for numero in numeros:
            f.write(f"{numero}\n")


def comparar_listas(lista_c: list[int], lista_py: list[int]) -> bool:
    if len(lista_c) != len(lista_py):
        print(f"Falha: tamanhos diferentes (C={len(lista_c)} | Python={len(lista_py)}).")
        return False

    for idx, (valor_c, valor_py) in enumerate(zip(lista_c, lista_py)):
        if valor_c != valor_py:
            print(
                "Falha: diferença encontrada no índice "
                f"{idx} (C={valor_c} | Python={valor_py})."
            )
            return False

    return True


def main() -> None:
    dados_entrada = carregar_dados(ARQUIVO_ENTRADA)
    ordenado_python = ordenar_com_sort(dados_entrada)
    salvar_lista(ARQUIVO_PY, ordenado_python)
    print(f"Arquivo '{ARQUIVO_PY}' gerado com sucesso.")

    if not ARQUIVO_C.exists():
        print(
            "Arquivo 'lista_ordenada.txt' ainda não existe. "
            "Execute o programa C antes para validar a comparação."
        )
        return

    ordenado_c = carregar_dados(ARQUIVO_C)

    if comparar_listas(ordenado_c, ordenado_python):
        print("Validação concluída: a saída do counting sort em C está correta.")
    else:
        print("Validação falhou: a saída do counting sort em C difere da ordenação em Python.")


if __name__ == "__main__":
    main()
