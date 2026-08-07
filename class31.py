"""
Gera duas (ou mais) variáveis quantitativas correlacionadas,
calcula o coeficiente de correlação e plota um gráfico de dispersão.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# 1) Configurações
# ------------------------------------------------------------
np.random.seed(42)        # reprodutibilidade
n = 200                    # número de observações
correlacao_desejada = 0.75 # entre -1 e 1

# ------------------------------------------------------------
# 2) Gerar duas variáveis correlacionadas
#    Usamos uma distribuição normal multivariada, definindo
#    a matriz de covariância a partir da correlação desejada.
# ------------------------------------------------------------
media = [0, 0]
matriz_cov = [
    [1, correlacao_desejada],
    [correlacao_desejada, 1]
]

dados = np.random.multivariate_normal(media, matriz_cov, size=n)

# ------------------------------------------------------------
# 3) Transformar para escalas mais "realistas"
#    Exemplo: variável X = altura da mesa (cm), variável Y = nível de desconforto (0-10)
# ------------------------------------------------------------
x = dados[:, 0] * 5 + 75   # média 75 cm, desvio ~5
y = dados[:, 1] * 1.5 + 5  # média 5, desvio ~1.5
y = np.clip(y, 0, 10)      # limitar escala de desconforto entre 0 e 10

df = pd.DataFrame({
    "altura_mesa_cm": x,
    "nivel_desconforto": y
})

# ------------------------------------------------------------
# 4) Verificar a correlação obtida
# ------------------------------------------------------------
correlacao_real = df["altura_mesa_cm"].corr(df["nivel_desconforto"])
print(f"Correlação de Pearson obtida: {correlacao_real:.3f}")
print(df.describe())

# ------------------------------------------------------------
# 5) Salvar em CSV (opcional)
# ------------------------------------------------------------
df.to_csv("variaveis_correlacionadas.csv", index=False)

# ------------------------------------------------------------
# 6) Gráfico de dispersão
# ------------------------------------------------------------
plt.figure(figsize=(7, 5))
plt.scatter(df["altura_mesa_cm"], df["nivel_desconforto"], alpha=0.6, color="darkorange")
plt.title(f"Correlação entre altura da mesa e desconforto (r = {correlacao_real:.2f})")
plt.xlabel("Altura da mesa (cm)")
plt.ylabel("Nível de desconforto (0-10)")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("dispersao_correlacao.png", dpi=150)
plt.show()