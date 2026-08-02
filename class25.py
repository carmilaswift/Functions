import time

def desenhar_coracao():
    linhas = [
        " ***   ***  ",
        "***** ***** ",
        "*************",
        " *********** ",
        "  *********  ",
        "   *******   ",
        "    *****    ",
        "     ***     ",
        "      *      "
    ]
    for linha in linhas:
        print(linha.center(40))
        time.sleep(0.2)

def dedicatoria(nome_destinatario, nome_remetente, mensagem):
    print("\n" + "=" * 40)
    desenhar_coracao()
    print("=" * 40)
    print(f"\nPara: {nome_destinatario}\n")
    print(mensagem)
    print(f"\nCom amor,\n{nome_remetente}")
    print("\n" + "=" * 40 + "\n")

if __name__ == "__main__":
    mensagem = (
        "Cada dia ao seu lado é um presente.\n"
        "Você trouxe cor para os meus dias\n"
        "e um sorriso que não cabe no peito.\n"
        "Obrigado(a) por existir e por fazer\n"
        "parte da minha história."
    )

    dedicatoria(
        nome_destinatario="Seu Amor",
        nome_remetente="Quem te ama",
        mensagem=mensagem
    )