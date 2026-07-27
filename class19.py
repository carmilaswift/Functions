"""
Conversor de Peso
------------------
Converte entre libras (lb), quilogramas (kg), gramas (g),
onças (oz) e toneladas (t).
"""

# Fatores de conversão: tudo é convertido primeiro para gramas (unidade base)
FATORES_PARA_GRAMAS = {
    "g": 1,
    "kg": 1000,
    "lb": 453.59237,      # 1 libra = 453.59237 gramas
    "oz": 28.349523125,   # 1 onça = 28.349523125 gramas
    "t": 1_000_000,       # 1 tonelada = 1.000.000 gramas
}

UNIDADES_NOMES = {
    "g": "gramas",
    "kg": "quilogramas",
    "lb": "libras",
    "oz": "onças",
    "t": "toneladas",
}


def converter_peso(valor: float, de_unidade: str, para_unidade: str) -> float:
    """
    Converte um valor de uma unidade de peso para outra.

    :param valor: valor numérico a converter
    :param de_unidade: unidade de origem ('g', 'kg', 'lb', 'oz', 't')
    :param para_unidade: unidade de destino ('g', 'kg', 'lb', 'oz', 't')
    :return: valor convertido
    """
    de_unidade = de_unidade.lower().strip()
    para_unidade = para_unidade.lower().strip()

    if de_unidade not in FATORES_PARA_GRAMAS:
        raise ValueError(f"Unidade de origem inválida: '{de_unidade}'")
    if para_unidade not in FATORES_PARA_GRAMAS:
        raise ValueError(f"Unidade de destino inválida: '{para_unidade}'")

    # Converte o valor para gramas (unidade intermediária) e depois para a unidade final
    valor_em_gramas = valor * FATORES_PARA_GRAMAS[de_unidade]
    valor_convertido = valor_em_gramas / FATORES_PARA_GRAMAS[para_unidade]

    return valor_convertido


def exibir_unidades_disponiveis():
    print("\nUnidades disponíveis:")
    for sigla, nome in UNIDADES_NOMES.items():
        print(f"  {sigla:>3} - {nome}")
    print()


def menu_interativo():
    print("=" * 45)
    print("        CONVERSOR DE PESO EM PYTHON")
    print("=" * 45)

    while True:
        exibir_unidades_disponiveis()

        try:
            valor = float(input("Digite o valor a converter: ").replace(",", "."))
        except ValueError:
            print("⚠️  Valor inválido. Tente novamente.\n")
            continue

        de_unidade = input("Unidade de origem (ex: lb, kg, g, oz, t): ").lower().strip()
        para_unidade = input("Unidade de destino (ex: lb, kg, g, oz, t): ").lower().strip()

        try:
            resultado = converter_peso(valor, de_unidade, para_unidade)
            print(
                f"\n✅ {valor} {UNIDADES_NOMES[de_unidade]} = "
                f"{resultado:.4f} {UNIDADES_NOMES[para_unidade]}\n"
            )
        except ValueError as erro:
            print(f"⚠️  Erro: {erro}\n")

        continuar = input("Deseja fazer outra conversão? (s/n): ").lower().strip()
        if continuar != "s":
            print("\nEncerrando o conversor. Até logo! 👋")
            break


if __name__ == "__main__":
    menu_interativo()