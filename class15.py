"""
Calculadora de Calorias (kcal)
------------------------------
Calcula a Taxa Metabólica Basal (TMB) usando a fórmula de Mifflin-St Jeor
e o Gasto Energético Total Diário (GET) com base no nível de atividade física.
"""


def calcular_tmb(sexo, peso_kg, altura_cm, idade_anos):
    """Calcula a Taxa Metabólica Basal (TMB) em kcal/dia."""
    if sexo == "m":
        tmb = (10 * peso_kg) + (6.25 * altura_cm) - (5 * idade_anos) + 5
    else:
        tmb = (10 * peso_kg) + (6.25 * altura_cm) - (5 * idade_anos) - 161
    return tmb


def calcular_get(tmb, nivel_atividade):
    """Calcula o Gasto Energético Total (GET) multiplicando a TMB
    pelo fator de atividade física."""
    fatores = {
        1: 1.2,    # Sedentário (pouco ou nenhum exercício)
        2: 1.375,  # Levemente ativo (exercício leve 1-3 dias/semana)
        3: 1.55,   # Moderadamente ativo (exercício moderado 3-5 dias/semana)
        4: 1.725,  # Muito ativo (exercício pesado 6-7 dias/semana)
        5: 1.9,    # Extremamente ativo (exercício intenso + trabalho físico)
    }
    return tmb * fatores[nivel_atividade]


def obter_float(mensagem):
    while True:
        try:
            return float(input(mensagem).replace(",", "."))
        except ValueError:
            print("Valor inválido. Digite um número (ex: 70.5).")


def obter_int(mensagem, opcoes):
    while True:
        try:
            valor = int(input(mensagem))
            if valor in opcoes:
                return valor
        except ValueError:
            pass
        print(f"Opção inválida. Escolha entre {min(opcoes)} e {max(opcoes)}.")


def main():
    print("=== Calculadora de Calorias (kcal) ===\n")

    sexo = ""
    while sexo not in ("m", "f"):
        sexo = input("Sexo (M/F): ").strip().lower()

    idade = obter_float("Idade (anos): ")
    peso = obter_float("Peso (kg): ")
    altura = obter_float("Altura (cm): ")

    print("\nNível de atividade física:")
    print("1 - Sedentário (pouco ou nenhum exercício)")
    print("2 - Levemente ativo (exercício leve 1-3 dias/semana)")
    print("3 - Moderadamente ativo (exercício moderado 3-5 dias/semana)")
    print("4 - Muito ativo (exercício pesado 6-7 dias/semana)")
    print("5 - Extremamente ativo (exercício intenso + trabalho físico)")
    nivel = obter_int("Escolha uma opção (1-5): ", {1, 2, 3, 4, 5})

    tmb = calcular_tmb(sexo, peso, altura, idade)
    get = calcular_get(tmb, nivel)

    print("\n--- Resultado ---")
    print(f"Taxa Metabólica Basal (TMB): {tmb:.0f} kcal/dia")
    print(f"Gasto Energético Total (GET): {get:.0f} kcal/dia")
    print(f"\nPara emagrecer, consuma cerca de {get - 500:.0f} kcal/dia")
    print(f"Para ganhar peso, consuma cerca de {get + 500:.0f} kcal/dia")
    print(f"Para manter o peso, consuma cerca de {get:.0f} kcal/dia")


if __name__ == "__main__":
    main()