# Make Escopo in Python
def minha_funcao():
    x = 10  # x é local, só existe dentro da função
    print(x)
x = ''
minha_funcao()  # imprime 10
print(x)  # ERRO! x não existe fora da função

y = 100  # y é global

def outra_funcao():
    print(y)  # a função CONSEGUE ler y, mesmo sem criar

outra_funcao()  # imprime 100
print(y)  # imprime 100
