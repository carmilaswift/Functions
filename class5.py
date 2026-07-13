"""
mini_db.py — Um mini banco de dados em Python (arquivo único, sem dependências).

Recursos:
- Persistência em disco (arquivo JSON)
- Múltiplas "tabelas" (coleções)
- CRUD: insert, find, update, delete
- Consultas simples com filtros (funções ou dicionário de igualdade)
- IDs automáticos incrementais
- Uso como biblioteca ou via linha de comando

Exemplo rápido:
    from mini_db import MiniDB

    db = MiniDB("meubanco.json")
    usuarios = db.table("usuarios")

    usuarios.insert({"nome": "Ana", "idade": 28})
    usuarios.insert({"nome": "Bruno", "idade": 35})

    print(usuarios.find({"nome": "Ana"}))
    usuarios.update({"nome": "Ana"}, {"idade": 29})
    usuarios.delete({"nome": "Bruno"})

    db.save()
"""

import json
import os
import uuid
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Union


Filtro = Union[Dict[str, Any], Callable[[Dict[str, Any]], bool]]


class Tabela:
    """Representa uma tabela (coleção) do mini banco de dados."""

    def __init__(self, nome: str, dados: Optional[List[Dict[str, Any]]] = None):
        self.nome = nome
        self.registros: List[Dict[str, Any]] = dados if dados is not None else []
        self._proximo_id = self._calcular_proximo_id()

    def _calcular_proximo_id(self) -> int:
        if not self.registros:
            return 1
        return max(r.get("_id", 0) for r in self.registros) + 1

    def _corresponde(self, registro: Dict[str, Any], filtro: Filtro) -> bool:
        if filtro is None:
            return True
        if callable(filtro):
            return filtro(registro)
        return all(registro.get(chave) == valor for chave, valor in filtro.items())

    def insert(self, dados: Dict[str, Any]) -> Dict[str, Any]:
        """Insere um novo registro e retorna o registro criado (com _id)."""
        registro = dict(dados)
        registro["_id"] = self._proximo_id
        registro["_criado_em"] = datetime.now().isoformat()
        self.registros.append(registro)
        self._proximo_id += 1
        return registro

    def insert_many(self, lista_dados: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [self.insert(d) for d in lista_dados]

    def find(self, filtro: Filtro = None) -> List[Dict[str, Any]]:
        """Retorna todos os registros que casam com o filtro (ou todos, se filtro=None)."""
        return [r for r in self.registros if self._corresponde(r, filtro)]

    def find_one(self, filtro: Filtro = None) -> Optional[Dict[str, Any]]:
        """Retorna o primeiro registro que casa com o filtro."""
        for r in self.registros:
            if self._corresponde(r, filtro):
                return r
        return None

    def find_by_id(self, _id: int) -> Optional[Dict[str, Any]]:
        return self.find_one({"_id": _id})

    def update(self, filtro: Filtro, novos_dados: Dict[str, Any]) -> int:
        """Atualiza todos os registros que casam com o filtro. Retorna quantos foram alterados."""
        count = 0
        for r in self.registros:
            if self._corresponde(r, filtro):
                r.update(novos_dados)
                r["_atualizado_em"] = datetime.now().isoformat()
                count += 1
        return count

    def delete(self, filtro: Filtro) -> int:
        """Remove todos os registros que casam com o filtro. Retorna quantos foram removidos."""
        antes = len(self.registros)
        self.registros = [r for r in self.registros if not self._corresponde(r, filtro)]
        return antes - len(self.registros)

    def count(self, filtro: Filtro = None) -> int:
        return len(self.find(filtro))

    def all(self) -> List[Dict[str, Any]]:
        return list(self.registros)

    def clear(self) -> None:
        self.registros = []
        self._proximo_id = 1

    def __len__(self) -> int:
        return len(self.registros)

    def __repr__(self) -> str:
        return f"<Tabela '{self.nome}' com {len(self.registros)} registro(s)>"


class MiniDB:
    """Mini banco de dados baseado em arquivo JSON, com múltiplas tabelas."""

    def __init__(self, arquivo: str = "mini_db.json", auto_save: bool = False):
        self.arquivo = arquivo
        self.auto_save = auto_save
        self._tabelas: Dict[str, Tabela] = {}
        self._carregar()

    def _carregar(self) -> None:
        if os.path.exists(self.arquivo):
            with open(self.arquivo, "r", encoding="utf-8") as f:
                try:
                    dados = json.load(f)
                except json.JSONDecodeError:
                    dados = {}
            for nome_tabela, registros in dados.items():
                self._tabelas[nome_tabela] = Tabela(nome_tabela, registros)

    def save(self) -> None:
        """Salva o estado atual do banco no arquivo em disco."""
        dados = {nome: t.registros for nome, t in self._tabelas.items()}
        with open(self.arquivo, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)

    def table(self, nome: str) -> Tabela:
        """Obtém (ou cria) uma tabela pelo nome."""
        if nome not in self._tabelas:
            self._tabelas[nome] = Tabela(nome)
        tabela = self._tabelas[nome]
        if self.auto_save:
            tabela = _TabelaAutoSave(tabela, self)
        return tabela

    def tabelas(self) -> List[str]:
        return list(self._tabelas.keys())

    def drop_table(self, nome: str) -> None:
        self._tabelas.pop(nome, None)

    def __repr__(self) -> str:
        resumo = ", ".join(f"{n}({len(t)})" for n, t in self._tabelas.items())
        return f"<MiniDB arquivo='{self.arquivo}' tabelas: {resumo or 'nenhuma'}>"


class _TabelaAutoSave:
    """Wrapper que salva o banco automaticamente após operações de escrita."""

    def __init__(self, tabela: Tabela, db: MiniDB):
        self._tabela = tabela
        self._db = db

    def __getattr__(self, item):
        return getattr(self._tabela, item)

    def insert(self, *a, **kw):
        r = self._tabela.insert(*a, **kw)
        self._db.save()
        return r

    def insert_many(self, *a, **kw):
        r = self._tabela.insert_many(*a, **kw)
        self._db.save()
        return r

    def update(self, *a, **kw):
        r = self._tabela.update(*a, **kw)
        self._db.save()
        return r

    def delete(self, *a, **kw):
        r = self._tabela.delete(*a, **kw)
        self._db.save()
        return r

    def clear(self):
        self._tabela.clear()
        self._db.save()


# ---------------------------------------------------------------------------
# Demonstração / uso via linha de comando
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=== Demonstração do mini_db.py ===\n")

    caminho = "exemplo_banco.json"
    db = MiniDB(caminho)
    usuarios = db.table("usuarios")

    if usuarios.count() == 0:
        usuarios.insert({"nome": "Ana", "idade": 28, "cidade": "Salvador"})
        usuarios.insert({"nome": "Bruno", "idade": 35, "cidade": "Vitória da Conquista"})
        usuarios.insert({"nome": "Carla", "idade": 22, "cidade": "Salvador"})
        print("Registros iniciais inseridos.\n")

    print("Todos os usuários:")
    for u in usuarios.all():
        print(" ", u)

    print("\nUsuários de Salvador:")
    for u in usuarios.find({"cidade": "Salvador"}):
        print(" ", u)

    print("\nUsuários com idade > 25 (consulta com função):")
    for u in usuarios.find(lambda r: r["idade"] > 25):
        print(" ", u)

    alterados = usuarios.update({"nome": "Bruno"}, {"idade": 36})
    print(f"\nRegistros atualizados: {alterados}")

    print(f"\nTotal de usuários: {usuarios.count()}")

    db.save()
    print(f"\nBanco salvo em: {caminho}")