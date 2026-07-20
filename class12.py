def calcular_imc(peso, altura):
    """Calcula o IMC dado o peso (kg) e a altura (m)."""
    imc = peso / (altura ** 2)
    return round(imc, 2)

def classificar_imc(imc):
    """Retorna a classificação do IMC."""
    if imc < 18.5:
        return "Abaixo do peso"
    elif imc < 25:
        return "Peso normal"
    elif imc < 30:
        return "Sobrepeso"
    elif imc < 35:
        return "Obesidade grau I"
    elif imc < 40:
        return "Obesidade grau II"
    else:
        return "Obesidade grau III"

def main():
    print("=== Calculadora de IMC ===")
    peso = float(input("Digite seu peso (kg): "))
    altura = float(input("Digite sua altura (m): "))

    imc = calcular_imc(peso, altura)
    classificacao = classificar_imc(imc)

    print(f"\nSeu IMC é: {imc}")
    print(f"Classificação: {classificacao}")

if __name__ == "__main__":
    main()