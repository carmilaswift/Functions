"""
Conversor de Moedas - Real (BRL) para Dólar (USD), Euro (EUR) ou Peso (ARS)
----------------------------------------------------------------------------
Este script converte um valor em Reais para a moeda escolhida pelo usuário,
usando taxas de câmbio fixas definidas no dicionário TAXAS.

IMPORTANTE: As taxas abaixo são apenas exemplos e podem estar desatualizadas.
Para valores reais/atualizados, substitua os números em TAXAS pela cotação
do dia (ex: consultando o Banco Central, Google ou uma API de câmbio).
"""

# Taxas de conversão: quantas unidades da moeda estrangeira equivalem a 1 Real (BRL)
TAXAS = {
    "USD": 0.18,   # Dólar americano
    "EUR": 0.17,   # Euro
    "ARS": 185.00, # Peso argentino
}

NOMES = {
    "USD": "Dólar (USD)",
    "EUR": "Euro (EUR)",
    "ARS": "Peso Argentino (ARS)",
}


def converter(valor_reais: float, moeda: str) -> float:
    """Converte um valor em Reais para a moeda informada."""
    moeda = moeda.upper()
    if moeda not in TAXAS:
        raise ValueError(f"Moeda '{moeda}' não suportada. Escolha entre: {', '.join(TAXAS)}")
    return valor_reais * TAXAS[moeda]


def escolher_moeda() -> str:
    print("\nEscolha a moeda de destino:")
    print("1 - Dólar (USD)")
    print("2 - Euro (EUR)")
    print("3 - Peso Argentino (ARS)")

    opcoes = {"1": "USD", "2": "EUR", "3": "ARS"}

    while True:
        escolha = input("Digite o número da opção desejada: ").strip()
        if escolha in opcoes:
            return opcoes[escolha]
        print("Opção inválida. Tente novamente.")


def ler_valor() -> float:
    while True:
        try:
            valor = float(input("Digite o valor em Reais (R$): ").replace(",", "."))
            if valor < 0:
                print("O valor não pode ser negativo.")
                continue
            return valor
        except ValueError:
            print("Valor inválido. Digite apenas números (ex: 150.50).")


def main():
    print("=" * 45)
    print("      CONVERSOR DE MOEDAS - REAL (BRL)")
    print("=" * 45)

    continuar = True
    while continuar:
        valor = ler_valor()
        moeda = escolher_moeda()
        resultado = converter(valor, moeda)

        print(f"\nR$ {valor:,.2f} equivalem a {resultado:,.2f} {NOMES[moeda]}")
        print(f"(Taxa utilizada: 1 BRL = {TAXAS[moeda]} {moeda})\n")

        de_novo = input("Deseja fazer outra conversão? (s/n): ").strip().lower()
        continuar = de_novo == "s"

    print("\nObrigado por usar o conversor!")


if __name__ == "__main__":
    main()