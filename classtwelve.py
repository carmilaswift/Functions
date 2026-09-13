import math
import random
import time


class CelestialBody:

    """Representa uma manifestação individual de matéria no universo."""

    def __init__(
        self, body_id: int, mass: float, x: float, y: float, vx: float, vy: float
    ):
        self.id = body_id
        self.mass = mass
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def apply_gravity(self, other: "CelestialBody", g_const: float, dt: float):
        """Calcula e aplica a atração gravitacional entre duas manifestações materiais."""
        dx = other.x - self.x
        dy = other.y - self.y
        distance = math.sqrt(dx**2 + dy**2)

        # Evita divisão por zero e colisão extrema
        if distance < 1.0:
            return

        force = (g_const * self.mass * other.mass) / (distance**2)
        fx = force * (dx / distance)
        fy = force * (dy / distance)

        # Aceleração a = F / m
        self.vx += (fx / self.mass) * dt
        self.vy += (fy / self.mass) * dt

    def update_position(self, dt: float):
        """Atualiza a posição no plano físico."""
        self.x += self.vx * dt
        self.y += self.vy * dt


class ManifestedUniverse:

    """Gerenciador do ciclo de vida e leis do Universo Manifestado."""

    def __init__(
        self, G: float = 0.5, entropy_decay: float = 0.9999, dimensions: int = 2
    ):
        self.G = G  # Constante Gravitacional
        self.entropy_decay = entropy_decay  # Perda gradual de energia
        self.dimensions = dimensions
        self.is_manifested = False
        self.bodies = []
        self.age = 0.0

    def manifest(self, num_bodies: int = 5):
        """O grande momento da criação: Transição do Não-Manifestado para o Manifestado (Big Bang)."""
        print("=== ESTADO INICIAL: O VAZIO NÃO-MANIFESTADO ===")
        print("Espaço-tempo indiferenciado... aguardando flutuação de energia.\n")
        time.sleep(1)

        print("⚡ O BIG BANG / A MANIFESTAÇÃO COMEÇA! ⚡\n")
        self.bodies = []

        for i in range(num_bodies):
            # Posicionamento a partir do centro original (0,0) com distribuição radial
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2.0, 8.0)
            mass = random.uniform(10.0, 100.0)

            x = random.uniform(-5.0, 5.0)
            y = random.uniform(-5.0, 5.0)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed

            body = CelestialBody(
                body_id=i + 1, mass=mass, x=x, y=y, vx=vx, vy=vy
            )
            self.bodies.append(body)

        self.is_manifested = True
        self.age = 0.0

    def step(self, dt: float = 0.1):
        """Avança o tempo cósmico por uma unidade 'dt'."""
        if not self.is_manifested:
            return

        # 1. Aplica força da gravidade mútua entre todos os corpos
        for i in range(len(self.bodies)):
            for j in range(len(self.bodies)):
                if i != j:
                    self.bodies[i].apply_gravity(self.bodies[j], self.G, dt)

        # 2. Atualiza posições e aplica entropia/atrito cósmico
        for body in self.bodies:
            body.update_position(dt)
            body.vx *= self.entropy_decay
            body.vy *= self.entropy_decay

        self.age += dt

    def render_state(self):
        """Imprime o estado atual do universo no console."""
        print(f"--- Universo Manifestado | Tempo: {self.age:.1f}s ---")
        for b in self.bodies:
            pos_str = f"X: {b.x:6.2f} | Y: {b.y:6.2f}"
            vel_str = f"Vx: {b.vx:5.2f} | Vy: {b.vy:5.2f}"
            print(
                f"Corpo #{b.id} [Massa: {b.mass:5.1f}] -> Pos: ({pos_str}) | Vel: ({vel_str})"
            )
        print("-" * 65 + "\n")


# --- Execução da Simulação ---
if __name__ == "__main__":
    universe = ManifestedUniverse(G=1.5)

    # Big Bang: cria 4 corpos celestes
    universe.manifest(num_bodies=4)

    # Simula 5 passos de tempo para demonstrar a evolução cósmica
    for _ in range(5):
        universe.step(dt=0.5)
        universe.render_state()
        time.sleep(0.5)
