def classificar_idade(idade):
    if idade < 12:
        return "criança"
    elif idade < 18:
        return "adolescente"
    else:
        return "adulto"

# chamando a função com valores diferentes
print(classificar_idade(8))    # criança
print(classificar_idade(25))   # adulto

def saudacao(nome, periodo="dia"):
    return f"Bom {periodo}, {nome}!"

pessoas = ["Ana", "João", "Lucas"]

for pessoa in pessoas:
    print(saudacao(pessoa))            # usa o padrão "dia"
    print(saudacao(pessoa, "noite"))   # sobrescreve o padrão