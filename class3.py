# Generation code
import secrets
import string

def gerar_senha(tamanho=12):
    # Combina letras maiúsculas, minúsculas, números e símbolos
    caracteres = string.ascii_letters + string.digits + string.punctuation
    
    # Gera a senha de forma criptograficamente segura
    senha = ''.join(secrets.choice(caracteres) for _ in range(tamanho))
    return senha

# Exemplo de uso com tamanho personalizado
tamanho_desejado = 16
print(f"Sua senha segura é: {gerar_senha(tamanho_desejado)}")
