"""
Universo do Amor
-----------------
Uma pequena animação romântica em Python: um céu estrelado (o universo)
onde, aos poucos, um coração se desenha ponto a ponto, seguido por
uma mensagem de amor.

Requisitos: matplotlib, pillow, numpy
    pip install matplotlib pillow numpy --break-system-packages
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# ---------- Configuração da cena ----------
fig, ax = plt.subplots(figsize=(9, 9), facecolor="black")
ax.set_facecolor("black")
ax.set_xlim(-20, 20)
ax.set_ylim(-22, 20)
ax.axis("off")

# ---------- O Universo: campo de estrelas ----------
rng = np.random.default_rng(42)
n_stars = 260
star_x = rng.uniform(-20, 20, n_stars)
star_y = rng.uniform(-20, 20, n_stars)
star_base_size = rng.uniform(1, 12, n_stars)
star_phase = rng.uniform(0, 2 * np.pi, n_stars)

stars = ax.scatter(star_x, star_y, s=star_base_size, c="white", alpha=0.7)

# Título fixo no topo, lembrando que tudo isso é o universo
ax.text(
    0, 19, "✦ o universo ✦",
    color="lightskyblue", fontsize=13, ha="center",
    family="monospace", alpha=0.85,
)

# ---------- O Coração (curva paramétrica clássica) ----------
t = np.linspace(0, 2 * np.pi, 220)
heart_x = 16 * np.sin(t) ** 3
heart_y = 13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t)
heart_x /= 1.6
heart_y /= 1.6

heart_scatter = ax.scatter([], [], s=45, c="deeppink", edgecolors="white", linewidths=0.3)

# ---------- Mensagem final ----------
message = "voce e o meu universo inteiro"
text = ax.text(
    0, -19, "", color="white", fontsize=15, ha="center",
    family="monospace", weight="bold",
)

TOTAL_HEART_FRAMES = len(heart_x)
TOTAL_TEXT_FRAMES = len(message)
TOTAL_FRAMES = TOTAL_HEART_FRAMES + TOTAL_TEXT_FRAMES + 40  # pausa final


def init():
    heart_scatter.set_offsets(np.empty((0, 2)))
    text.set_text("")
    return heart_scatter, text, stars


def animate(frame):
    # 1) estrelas do universo sempre cintilando
    twinkle = 1 + 0.4 * np.sin(frame / 8 + star_phase)
    stars.set_sizes(np.abs(star_base_size * twinkle))

    # 2) coração se desenhando ponto a ponto
    n = min(frame, TOTAL_HEART_FRAMES)
    offsets = np.column_stack((heart_x[:n], heart_y[:n]))
    heart_scatter.set_offsets(offsets)

    # 3) mensagem aparecendo letra por letra, depois do coração completo
    if frame > TOTAL_HEART_FRAMES:
        chars = min(frame - TOTAL_HEART_FRAMES, TOTAL_TEXT_FRAMES)
        text.set_text(message[:chars])

    return heart_scatter, text, stars


ani = animation.FuncAnimation(
    fig, animate, init_func=init,
    frames=TOTAL_FRAMES, interval=45, blit=False, repeat=True,
)

# ---------- Exportação ----------
ani.save("universo_amor.gif", writer="pillow", fps=22)
print("GIF gerado: universo_amor.gif")