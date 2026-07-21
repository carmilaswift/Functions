"""
Calculadora de Média Ponderada
-------------------------------
Calcula a média ponderada a partir de valores e pesos informados pelo usuário.

Fórmula:
    média_ponderada = (Σ (valor_i * peso_i)) / (Σ peso_i)
"""


def calcular_media_ponderada(valores, pesos):
    """Recebe duas listas (valores e pesos) e retorna a média ponderada."""
    if len(valores) != len(pesos):
        raise ValueError("A quantidade de valores deve ser igual à de pesos.")
    if len(valores) == 0:
        raise ValueError("É preciso informar ao menos um valor.")
    if sum(pesos) == 0:
        raise ValueError("A soma dos pesos não pode ser zero.")

    soma_ponderada = sum(v * p for v, p in zip(valores, pesos))
    soma_pesos = sum(pesos)
    return soma_ponderada / soma_pesos


def ler_float(mensagem):
    """Lê um número float do usuário, validando a entrada."""
    while True:
        try:
            return float(input(mensagem).replace(",", "."))
        except ValueError:
            print("Entrada inválida. Digite um número (ex: 7.5).")


def main():
    print("=== Calculadora de Média Ponderada ===\n")

    while True:
        try:
            n = int(input("Quantos valores você vai informar? "))
            if n <= 0:
                print("Informe um número inteiro maior que zero.")
                continue
            break
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")

    valores = []
    pesos = []

    for i in range(1, n + 1):
        print(f"\n-- Item {i} --")
        valor = ler_float(f"  Valor {i}: ")
        peso = ler_float(f"  Peso {i}: ")
        valores.append(valor)
        pesos.append(peso)

    try:
        resultado = calcular_media_ponderada(valores, pesos)
        print(f"\n>>> Média ponderada: {resultado:.2f}")
    except ValueError as erro:
        print(f"\nErro: {erro}")


if __name__ == "__main__":
    main()