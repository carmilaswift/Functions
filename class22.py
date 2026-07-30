"""
Jogo da Velha (Tic-Tac-Toe)
Dois jogadores se revezam no mesmo terminal.
"""


def criar_tabuleiro():
    return [str(i) for i in range(1, 10)]


def exibir_tabuleiro(tabuleiro):
    print()
    print(f" {tabuleiro[0]} | {tabuleiro[1]} | {tabuleiro[2]} ")
    print("---+---+---")
    print(f" {tabuleiro[3]} | {tabuleiro[4]} | {tabuleiro[5]} ")
    print("---+---+---")
    print(f" {tabuleiro[6]} | {tabuleiro[7]} | {tabuleiro[8]} ")
    print()


def verificar_vencedor(tabuleiro, jogador):
    combinacoes_vencedoras = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # linhas
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # colunas
        (0, 4, 8), (2, 4, 6),             # diagonais
    ]
    return any(
        tabuleiro[a] == tabuleiro[b] == tabuleiro[c] == jogador
        for a, b, c in combinacoes_vencedoras
    )


def tabuleiro_cheio(tabuleiro):
    return all(pos in ("X", "O") for pos in tabuleiro)


def obter_jogada(tabuleiro, jogador):
    while True:
        entrada = input(f"Jogador {jogador}, escolha uma posição (1-9): ").strip()

        if not entrada.isdigit() or not (1 <= int(entrada) <= 9):
            print("Entrada inválida. Digite um número entre 1 e 9.")
            continue

        posicao = int(entrada) - 1

        if tabuleiro[posicao] in ("X", "O"):
            print("Essa posição já está ocupada. Escolha outra.")
            continue

        return posicao


def jogar():
    tabuleiro = criar_tabuleiro()
    jogador_atual = "X"

    print("=== JOGO DA VELHA ===")
    print("Use os números abaixo para escolher sua posição:")
    exibir_tabuleiro(tabuleiro)

    while True:
        posicao = obter_jogada(tabuleiro, jogador_atual)
        tabuleiro[posicao] = jogador_atual

        exibir_tabuleiro(tabuleiro)

        if verificar_vencedor(tabuleiro, jogador_atual):
            print(f"🎉 Jogador {jogador_atual} venceu! Parabéns!")
            break

        if tabuleiro_cheio(tabuleiro):
            print("😐 Empate! O tabuleiro está cheio.")
            break

        jogador_atual = "O" if jogador_atual == "X" else "X"

    jogar_novamente = input("Deseja jogar novamente? (s/n): ").strip().lower()
    if jogar_novamente == "s":
        jogar()
    else:
        print("Obrigado por jogar!")


if __name__ == "__main__":
    jogar()