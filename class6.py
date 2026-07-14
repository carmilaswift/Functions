# Generate code CPF
"""
Mini Gerador de Cifras
-----------------------
Gera progressões de acordes aleatórias em qualquer tom (maior ou menor)
e exibe no formato de cifra, pronto pra tocar no violão/guitarra.
"""

import random

NOTAS = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

# Graus da escala maior e menor (em semitons a partir da tônica)
ESCALA_MAIOR = [0, 2, 4, 5, 7, 9, 11]
ESCALA_MENOR = [0, 2, 3, 5, 7, 8, 10]

# Qualidade de cada grau (maior, menor, diminuto)
QUALIDADE_MAIOR = ["", "m", "m", "", "", "m", "dim"]
QUALIDADE_MENOR = ["m", "dim", "", "m", "m", "", ""]

# Progressões clássicas (em graus, 1 = tônica)
PROGRESSOES = [
    [1, 5, 6, 4],
    [1, 6, 4, 5],
    [2, 5, 1, 1],
    [1, 4, 5, 5],
    [6, 4, 1, 5],
    [1, 4, 6, 5],
]


def montar_acordes(tom, modo="maior"):
    indice_tom = NOTAS.index(tom)
    escala = ESCALA_MAIOR if modo == "maior" else ESCALA_MENOR
    qualidades = QUALIDADE_MAIOR if modo == "maior" else QUALIDADE_MENOR

    acordes = []
    for i, semitons in enumerate(escala):
        nota = NOTAS[(indice_tom + semitons) % 12]
        acordes.append(nota + qualidades[i])
    return acordes


def gerar_progressao(tom, modo="maior", compassos=4):
    acordes = montar_acordes(tom, modo)
    graus = random.choice(PROGRESSOES)

    # se pediu mais compassos que a progressão base, repete/completa
    while len(graus) < compassos:
        graus += random.choice(PROGRESSOES)
    graus = graus[:compassos]

    return [acordes[g - 1] for g in graus]


def formatar_cifra(progressao, repeticoes=2, batida="D D U U D U"):
    linha = "  |  ".join(progressao)
    print("=" * 40)
    print(f"Batida sugerida: {batida}")
    print("=" * 40)
    for i in range(repeticoes):
        print(f"| {linha} |")
    print("=" * 40)


def main():
    print("MINI GERADOR DE CIFRAS\n")

    tom = input(f"Tom (ex: C, D, F#) [Enter = aleatório]: ").strip().upper()
    if tom not in NOTAS:
        tom = random.choice(NOTAS)

    modo = input("Modo (maior/menor) [Enter = maior]: ").strip().lower()
    if modo not in ("maior", "menor"):
        modo = "maior"

    try:
        compassos = int(input("Quantos acordes na progressão? [Enter = 4]: ") or 4)
    except ValueError:
        compassos = 4

    progressao = gerar_progressao(tom, modo, compassos)

    print(f"\nTom escolhido: {tom} {modo}")
    formatar_cifra(progressao)


if __name__ == "__main__":
    main()