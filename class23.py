import random

print("=" * 35)
print("🎮 JOGO DE ADIVINHAÇÃO")
print("=" * 35)

# Sorteia um número entre 1 e 100
numero_secreto = random.randint(1, 100)

tentativas = 0

while True:
    try:
        palpite = int(input("Digite um número entre 1 e 100: "))
        tentativas += 1

        if palpite < numero_secreto:
            print("📉 O número secreto é MAIOR!\n")

        elif palpite > numero_secreto:
            print("📈 O número secreto é MENOR!\n")

        else:
            print(f"\n🎉 Parabéns! Você acertou!")
            print(f"O número secreto era {numero_secreto}.")
            print(f"Você precisou de {tentativas} tentativa(s).")
            break

    except ValueError:
        print("❌ Digite apenas números inteiros!")