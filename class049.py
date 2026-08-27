from dataclasses import dataclass, field
from typing import List, Dict
import math

@dataclass
class NodeGratidao:
    entidade: str
    nivel_apreciacao: float  # Escala de 0.0 a 10.0
    impactos: List[str] = field(default_factory=list)
    conexoes: Dict[str, float] = field(default_factory=dict)  # Alvo -> Peso do efeito cascata

class RededeGratidao:
    def __init__(self, sistema_foco: str):
        self.sistema_foco = sistema_foco
        self.nos: Dict[str, NodeGratidao] = {}

    def registrar_reconhecimento(self, entidade: str, nivel: float, impactos: List[str]) -> None:
        self.nos[entidade] = NodeGratidao(
            entidade=entidade, 
            nivel_apreciacao=min(max(nivel, 0.0), 10.0), 
            impactos=impactos
        )

    def vincular_efeito_cascata(self, origem: str, destino: str, peso: float) -> None:
        if origem in self.nos and destino in self.nos:
            self.nos[origem].conexoes[destino] = peso

    def calcular_ressonancia_acumulada(self) -> float:
        """Calcula a ressonância emocional considerando a densidade de impacto e conexões."""
        ressonancia_total = 0.0
        for no in self.nos.values():
            # Aceleração logarítmica baseada na diversidade de impactos
            base = no.nivel_apreciacao * math.log(len(no.impactos) + 2)
            
            # Efeito cascata propagado para nós conectados
            cascata = sum(
                peso * self.nos[alvo].nivel_apreciacao 
                for alvo, peso in no.conexoes.items() 
                if alvo in self.nos
            )
            ressonancia_total += base + (cascata * 0.5)
            
        return round(ressonancia_total, 2)

    def gerar_sintese(self) -> str:
        ressonancia = self.calcular_ressonancia_acumulada()
        tags_unicas = {tag for no in self.nos.values() for tag in no.impactos}
        
        linhas = [
            f"=== SINTETIZADOR SISTÊMICO DE GRATIDÃO: {self.sistema_foco.upper()} ===",
            f"Nós Mapeados: {len(self.nos)} | Áreas de Impacto: {len(tags_unicas)}",
            f"Índice Global de Ressonância: {ressonancia} Hz",
            "-" * 55
        ]
        
        for nome, no in self.nos.items():
            vinculos = ", ".join(f"{k} (peso={v})" for k, v in no.conexoes.items()) or "Nenhum"
            linhas.append(f"• [{nome.upper()}] Nível: {no.nivel_apreciacao}/10")
            linhas.append(f"  Impactos: {', '.join(no.impactos)}")
            linhas.append(f"  Propagação: {vinculos}\n")
            
        return "\n".join(linhas)


# Instanciação e execução da rede
rede = RededeGratidao("Desenvolvimento Pessoal & Aprendizado")

# Adicionando elementos
rede.registrar_reconhecimento("Mentores e Guias", 9.5, ["sabedoria", "direção", "suporte"])
rede.registrar_reconhecimento("Desafios Complexos", 8.2, ["resiliência", "adaptabilidade"])
rede.registrar_reconhecimento("Saúde e Vitalidade", 9.8, ["energia", "foco", "estabilidade"])

# Estabelecendo conexões de reforço mútuo (efeito cascata)
rede.vincular_efeito_cascata("Mentores e Guias", "Desafios Complexos", 0.8)
rede.vincular_efeito_cascata("Saúde e Vitalidade", "Desafios Complexos", 0.9)

print(rede.gerar_sintese())
