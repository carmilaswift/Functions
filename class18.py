"""
mini-translator: tradutor simples Inglês <-> Português
Sem dependências externas — só Python puro.
"""

import re

# Dicionário Inglês -> Português (frases primeiro, palavras depois)
DICIONARIO_EN_PT = {
    "good morning": "bom dia",
    "good afternoon": "boa tarde",
    "good evening": "boa noite",
    "good night": "boa noite",
    "how are you": "como você está",
    "thank you very much": "muito obrigado",
    "thank you": "obrigado",
    "see you later": "até mais tarde",
    "nice to meet you": "prazer em conhecê-lo",
    "excuse me": "com licença",
    "i am sorry": "eu sinto muito",
    "my name is": "meu nome é",
    "i love you": "eu te amo",
    "happy birthday": "feliz aniversário",
    "good luck": "boa sorte",
    "hello": "olá",
    "hi": "oi",
    "bye": "tchau",
    "goodbye": "adeus",
    "yes": "sim",
    "no": "não",
    "please": "por favor",
    "sorry": "desculpa",
    "friend": "amigo",
    "family": "família",
    "house": "casa",
    "water": "água",
    "food": "comida",
    "coffee": "café",
    "book": "livro",
    "school": "escola",
    "work": "trabalho",
    "money": "dinheiro",
    "time": "tempo",
    "day": "dia",
    "night": "noite",
    "today": "hoje",
    "tomorrow": "amanhã",
    "love": "amor",
    "happy": "feliz",
    "sad": "triste",
    "big": "grande",
    "small": "pequeno",
    "hot": "quente",
    "cold": "frio",
    "good": "bom",
    "bad": "ruim",
    "dog": "cachorro",
    "cat": "gato",
    "car": "carro",
    "city": "cidade",
    "world": "mundo",
    "i": "eu",
    "you": "você",
    "we": "nós",
    "and": "e",
    "or": "ou",
    "with": "com",
    "for": "para",
}

# Gera o dicionário reverso Português -> Inglês automaticamente
DICIONARIO_PT_EN = {v: k for k, v in DICIONARIO_EN_PT.items()}


def traduzir(texto, direcao="en-pt"):
    """Traduz um texto. direcao: 'en-pt' ou 'pt-en'."""
    tabela = DICIONARIO_EN_PT if direcao == "en-pt" else DICIONARIO_PT_EN
    max_len = max(len(k.split()) for k in tabela)

    tokens = re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ]+|[^\sA-Za-zÀ-ÖØ-öø-ÿ]+", texto)
    is_palavra = [bool(re.match(r"^[A-Za-zÀ-ÖØ-öø-ÿ]+$", t)) for t in tokens]

    resultado = []
    i, n = 0, len(tokens)
    inicio_frase = True

    while i < n:
        if not is_palavra[i]:
            resultado.append(tokens[i])
            if tokens[i].strip() in (".", "!", "?"):
                inicio_frase = True
            i += 1
            continue

        encontrou = False
        for span in range(max_len, 1, -1):
            j, palavras, count = i, [], 0
            while j < n and count < span:
                if is_palavra[j]:
                    palavras.append(tokens[j])
                    count += 1
                    j += 1
                else:
                    break
            if count == span:
                frase = " ".join(w.lower() for w in palavras)
                if frase in tabela:
                    trad = tabela[frase]
                    resultado.append(trad.capitalize() if inicio_frase else trad)
                    i = j
                    encontrou = True
                    inicio_frase = False
                    break
        if encontrou:
            continue

        palavra = tokens[i]
        trad = tabela.get(palavra.lower(), palavra)
        resultado.append(trad.capitalize() if inicio_frase else trad)
        inicio_frase = False
        i += 1

    texto_final = ""
    for palavra in resultado:
        if texto_final and not re.match(r"^[^\sA-Za-zÀ-ÖØ-öø-ÿ]+$", palavra):
            texto_final += " "
        texto_final += palavra
    return texto_final


if __name__ == "__main__":
    print(traduzir("Good morning, my friend!", "en-pt"))
    print(traduzir("Bom dia, meu amigo!", "pt-en"))
    print(traduzir("I love you and I am happy today.", "en-pt"))