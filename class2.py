# calculator with fractions and square root
import math

print("=" * 35)
print("      CALCULADORA SIMPLES")
print("=" * 35)

while True:
    print("\nEscolha uma opção:")
    print("1 - Soma")
    print("2 - Subtração")
    print("3 - Multiplicação")
    print("4 - Divisão")
    print("5 - Fração (numerador/denominador)")
    print("6 - Raiz quadrada")
    print("7 - Sair")

    opcao = input("\nDigite a opção: ")

    if opcao == "1":
        a = float(input("Primeiro número: "))
        b = float(input("Segundo número: "))
        print(f"Resultado: {a + b}")

    elif opcao == "2":
        a = float(input("Primeiro número: "))
        b = float(input("Segundo número: "))
        print(f"Resultado: {a - b}")

    elif opcao == "3":
        a = float(input("Primeiro número: "))
        b = float(input("Segundo número: "))
        print(f"Resultado: {a * b}")

    elif opcao == "4":
        a = float(input("Primeiro número: "))
        b = float(input("Segundo número: "))

        if b != 0:
            print(f"Resultado: {a / b}")
        else:
            print("Erro: divisão por zero!")

    elif opcao == "5":
        numerador = float(input("Numerador: "))
        denominador = float(input("Denominador: "))

        if denominador != 0:
            print(f"Fração = {numerador}/{denominador}")
            print(f"Valor decimal = {numerador / denominador}")
        else:
            print("Erro: denominador não pode ser zero!")

    elif opcao == "6":
        numero = float(input("Digite um número: "))

        if numero >= 0:
            print(f"Raiz quadrada = {math.sqrt(numero):.4f}")
        else:
            print("Não existe raiz quadrada real de número negativo.")

    elif opcao == "7":
        print("Calculadora encerrada.")
        break

    else:
        print("Opção inválida! Tente novamente.")