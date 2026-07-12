# calculator estatistcs data
import statistics
from collections import Counter

def calcular_estatisticas(dados):
    """
    Calcula média, mediana, moda e coeficiente de variação.
    """
    if not dados:
        return "Erro: A lista de dados está vazia."
    
    try:
        # Conversão para float
        numeros = [float(x) for x in dados]
    except ValueError:
        return "Erro: Todos os valores devem ser números."
    
    n = len(numeros)
    
    # Média
    media = statistics.mean(numeros)
    
    # Mediana
    mediana = statistics.median(numeros)
    
    # Moda
    contagem = Counter(numeros)
    max_freq = max(contagem.values())
    modas = [k for k, v in contagem.items() if v == max_freq]
    moda = modas if len(modas) > 1 else modas[0]
    
    # Desvio padrão e Coeficiente de Variação
    if n > 1:
        desvio_padrao = statistics.stdev(numeros)
        coef_variacao = (desvio_padrao / media) * 100 if media != 0 else float('nan')
    else:
        desvio_padrao = 0
        coef_variacao = 0
    
    # Resultados
    print("\n" + "="*50)
    print("          RESULTADOS ESTATÍSTICOS")
    print("="*50)
    print(f"Quantidade de dados     : {n}")
    print(f"Média (Média Aritmética): {media:.4f}")
    print(f"Mediana                 : {mediana:.4f}")
    print(f"Moda                    : {moda}")
    print(f"Desvio Padrão           : {desvio_padrao:.4f}")
    print(f"Coeficiente de Variação : {coef_variacao:.2f}%")
    print("="*50)


# ==================== INTERFACE DE USO ====================
if __name__ == "__main__":
    print("Calculadora Estatística - Média, Moda, Mediana e Coeficiente de Variação")
    print("Digite os valores separados por vírgula ou espaço.\n")
    
    entrada = input("Valores: ")
    # Aceita tanto vírgula quanto espaço
    valores = [x.strip() for x in entrada.replace(',', ' ').split()]
    
    resultado = calcular_estatisticas(valores)
    if isinstance(resultado, str):
        print(resultado)