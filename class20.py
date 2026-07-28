def eh_identificador_valido(nome):
    # Verifica se está vazio
    if not nome:
        return False, "O nome não pode estar vazio"
    
    # Verifica se é uma palavra reservada do Python
    import keyword
    if keyword.iskeyword(nome):
        return False, f"'{nome}' é uma palavra reservada do Python"
    
    # Verifica se o primeiro caractere é letra ou underscore
    if not (nome[0].isalpha() or nome[0] == '_'):
        return False, "Deve começar com letra ou underscore (_)"
    
    # Verifica se os demais caracteres são letras, números ou underscore
    for char in nome[1:]:
        if not (char.isalnum() or char == '_'):
            return False, f"Caractere inválido: '{char}'"
    
    return True, "Nome válido!"


# Testando
nomes_teste = ["idade", "2nome", "nome_completo", "class", "_privado", "nome com espaço", "café"]

for nome in nomes_teste:
    valido, mensagem = eh_identificador_valido(nome)
    status = "✅" if valido else "❌"
    print(f"{status} '{nome}': {mensagem}")