#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pipeline - Grupo 1 | Setor Primario (Agropecuaria e Extrativismo)
Vitoria da Conquista (BA) | periodo 2021-2025

Etapas:
  baixar-rfb    baixa os arquivos abertos do CNPJ (Receita Federal)
  rfb           filtra municipio + CNAEs 01-03 e 05-09, limpa, remove duplicados
  baixar-caged  baixa os microdados do Novo CAGED (MOV, FOR, EXC) por mes
  caged         filtra municipio + subclasses 01-03 e 05-09, aplica MOV+FOR-EXC
  sidra         baixa tabelas do SIDRA/IBGE para o municipio (API)
  tudo          rfb + caged + sidra (assume que os brutos ja foram baixados)

Dependencias: pip install pandas numpy py7zr
Uso:          python pipeline_setor_primario_vca.py rfb

ATENCAO: confira as constantes da secao CONFIG (URLs e pasta do mes) antes de
rodar. Os enderecos dos portais mudam com o tempo.
"""
import argparse
import ftplib
import io
import json
import sys
import unicodedata
import urllib.request
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

# ----------------------------------------------------------------------------
# CONFIG
# ----------------------------------------------------------------------------
UF = "BA"
MUNICIPIO_NOME = "VITORIA DA CONQUISTA"   # nome sem acento, como na tabela Municipios da RFB
COD_IBGE_7 = "2933307"                    # codigo IBGE (SIDRA)
COD_IBGE_6 = "293330"                     # codigo IBGE de 6 digitos (Novo CAGED)
ANO_INI, ANO_FIM = 2021, 2025

# Divisoes CNAE 2.0: Secao A (01 agricultura/pecuaria, 02 florestal/extrativismo vegetal,
# 03 pesca/aquicultura) e Secao B (05-09 industrias extrativas)
DIVISOES = {"01", "02", "03", "05", "06", "07", "08", "09"}
SECAO_A = {"01", "02", "03"}

DIR_RFB = Path("dados/brutos/rfb")
DIR_CAGED = Path("dados/brutos/caged")
DIR_SIDRA = Path("dados/brutos/sidra")
DIR_OUT = Path("dados/tratados")

# Receita Federal - confirme a URL e a pasta do mes mais recente no portal
RFB_BASE_URL = "https://arquivos.receitafederal.gov.br/dados/cnpj/dados_abertos_cnpj/"
RFB_PASTA = "AAAA-MM"   # ex.: a pasta do mes mais recente publicada

# Novo CAGED - confirme host/caminho no portal do MTE (PDET)
CAGED_FTP_HOST = "ftp.mtps.gov.br"
CAGED_FTP_RAIZ = "/pdet/microdados/NOVO CAGED"

# SIDRA: cole aqui o "Link da API" gerado no proprio site (sidra.ibge.gov.br)
# para cada tabela. Os exemplos abaixo precisam ser conferidos.
SIDRA_CONSULTAS = {
    "pam_5457_lavouras": "t/5457/n6/2933307/v/all/p/all/c782/all",
    "ppm_3939_rebanhos": "t/3939/n6/2933307/v/all/p/all/c79/all",
    # "cempre_unidades_locais": "t/XXXX/n6/2933307/v/all/p/all/c...",  # montar no SIDRA
}

# ----------------------------------------------------------------------------
# LAYOUTS (arquivos da Receita Federal nao tem cabecalho)
# ----------------------------------------------------------------------------
COLS_ESTAB = [
    "cnpj_basico", "cnpj_ordem", "cnpj_dv", "identificador_matriz_filial",
    "nome_fantasia", "situacao_cadastral", "data_situacao_cadastral",
    "motivo_situacao_cadastral", "nome_cidade_exterior", "pais",
    "data_inicio_atividade", "cnae_fiscal_principal", "cnae_fiscal_secundaria",
    "tipo_logradouro", "logradouro", "numero", "complemento", "bairro", "cep",
    "uf", "municipio", "ddd_1", "telefone_1", "ddd_2", "telefone_2",
    "ddd_fax", "fax", "correio_eletronico", "situacao_especial",
    "data_situacao_especial",
]
USO_ESTAB = [
    "cnpj_basico", "cnpj_ordem", "cnpj_dv", "identificador_matriz_filial",
    "nome_fantasia", "situacao_cadastral", "data_situacao_cadastral",
    "motivo_situacao_cadastral", "data_inicio_atividade", "cnae_fiscal_principal",
    "cnae_fiscal_secundaria", "tipo_logradouro", "logradouro", "numero",
    "bairro", "cep", "uf", "municipio",
]
COLS_EMPRESAS = [
    "cnpj_basico", "razao_social", "natureza_juridica",
    "qualificacao_responsavel", "capital_social", "porte_empresa",
    "ente_federativo",
]
COLS_SIMPLES = [
    "cnpj_basico", "opcao_simples", "data_opcao_simples", "data_exclusao_simples",
    "opcao_mei", "data_opcao_mei", "data_exclusao_mei",
]
SITUACAO = {"01": "NULA", "02": "ATIVA", "03": "SUSPENSA", "04": "INAPTA", "08": "BAIXADA"}
PORTE = {"00": "NAO INFORMADO", "01": "MICROEMPRESA", "03": "EMPRESA DE PEQUENO PORTE", "05": "DEMAIS"}


# ----------------------------------------------------------------------------
# UTILITARIOS
# ----------------------------------------------------------------------------
def sem_acento(s):
    return "".join(c for c in unicodedata.normalize("NFKD", str(s)) if not unicodedata.combining(c))


def ler_zip_csv(caminho, nomes, usecols=None, chunksize=500_000):
    """Le um .zip da RFB (CSV ';' sem cabecalho, latin-1) em blocos."""
    with zipfile.ZipFile(caminho) as z:
        with z.open(z.namelist()[0]) as f:
            yield from pd.read_csv(
                f, sep=";", header=None, names=nomes, usecols=usecols,
                dtype=str, encoding="latin-1", chunksize=chunksize,
                keep_default_na=False,
            )


def baixar(url, destino):
    destino = Path(destino)
    if destino.exists():
        print(f"  ja existe: {destino.name}")
        return
    destino.parent.mkdir(parents=True, exist_ok=True)
    tmp = destino.with_suffix(destino.suffix + ".part")
    print(f"  baixando {url}")
    urllib.request.urlretrieve(url, tmp)
    tmp.rename(destino)


# ----------------------------------------------------------------------------
# 1) RECEITA FEDERAL (CNPJ)
# ----------------------------------------------------------------------------
def baixar_rfb():
    nomes = (
        [f"Estabelecimentos{i}.zip" for i in range(10)]
        + [f"Empresas{i}.zip" for i in range(10)]
        + ["Simples.zip", "Municipios.zip", "Cnaes.zip", "Naturezas.zip"]
    )
    for n in nomes:
        try:
            baixar(f"{RFB_BASE_URL}{RFB_PASTA}/{n}", DIR_RFB / n)
        except Exception as e:  # noqa: BLE001
            print(f"  FALHOU {n}: {e}")


def resolver_codigo_municipio():
    alvo = sem_acento(MUNICIPIO_NOME).upper()
    for ch in ler_zip_csv(DIR_RFB / "Municipios.zip", ["codigo", "descricao"]):
        achou = ch[ch["descricao"].map(lambda x: sem_acento(x).upper().strip()) == alvo]
        if not achou.empty:
            return achou.iloc[0]["codigo"]
    raise SystemExit(f"Municipio {MUNICIPIO_NOME} nao encontrado em Municipios.zip")


def extrair_estabelecimentos(cod_mun, log):
    partes = []
    total_lidas = 0
    for arq in sorted(DIR_RFB.glob("Estabelecimentos*.zip")):
        print(f"  lendo {arq.name}")
        for ch in ler_zip_csv(arq, COLS_ESTAB, USO_ESTAB):
            total_lidas += len(ch)
            m = (
                (ch["uf"] == UF)
                & (ch["municipio"] == cod_mun)
                & ch["cnae_fiscal_principal"].str[:2].isin(DIVISOES)
            )
            if m.any():
                partes.append(ch[m])
    log["estabelecimentos_lidos_brasil"] = int(total_lidas)
    if not partes:
        raise SystemExit("Nenhum estabelecimento encontrado com os filtros.")
    return pd.concat(partes, ignore_index=True)


def limpar_estabelecimentos(df, log):
    df = df.copy()
    log["estab_filtrados_bruto"] = int(len(df))

    for c in df.columns:
        df[c] = df[c].astype(str).str.strip()
    df["cnpj_basico"] = df["cnpj_basico"].str.zfill(8)
    df["cnpj_ordem"] = df["cnpj_ordem"].str.zfill(4)
    df["cnpj_dv"] = df["cnpj_dv"].str.zfill(2)
    df["cnpj"] = df["cnpj_basico"] + df["cnpj_ordem"] + df["cnpj_dv"]
    df["cnae_fiscal_principal"] = df["cnae_fiscal_principal"].str.zfill(7)
    df["divisao_cnae"] = df["cnae_fiscal_principal"].str[:2]
    df["secao_cnae"] = np.where(df["divisao_cnae"].isin(SECAO_A), "A", "B")
    df["cep"] = df["cep"].str.replace(r"\D", "", regex=True).str.zfill(8)

    for c in ["data_inicio_atividade", "data_situacao_cadastral"]:
        df[c] = pd.to_datetime(df[c], format="%Y%m%d", errors="coerce")  # '0'/'00000000' -> NaT

    for c in ["nome_fantasia", "tipo_logradouro", "logradouro", "numero", "bairro"]:
        df[c] = df[c].str.upper().map(sem_acento).str.replace(r"\s+", " ", regex=True)
    df["bairro"] = df["bairro"].replace({"": "NAO INFORMADO"})
    df["situacao"] = df["situacao_cadastral"].map(SITUACAO).fillna("OUTRA")
    df["tipo_unidade"] = df["identificador_matriz_filial"].map({"1": "MATRIZ", "2": "FILIAL"})

    # Remocao de duplicados: o mesmo CNPJ completo (14 digitos) so pode aparecer uma vez.
    # Se houver repeticao, mantem o registro com a data de situacao mais recente.
    df = df.sort_values(["cnpj", "data_situacao_cadastral"], na_position="first")
    antes = len(df)
    df = df.drop_duplicates(subset="cnpj", keep="last")
    log["duplicados_removidos_cnpj"] = int(antes - len(df))

    # Registros sem data de inicio de atividade nao permitem a serie temporal
    sem_data = df["data_inicio_atividade"].isna()
    log["sem_data_inicio_atividade_removidos"] = int(sem_data.sum())
    df = df[~sem_data]

    # Universo do periodo: abriu ate 31/12/ANO_FIM e nao foi baixado antes de 01/01/ANO_INI
    ini, fim = pd.Timestamp(f"{ANO_INI}-01-01"), pd.Timestamp(f"{ANO_FIM}-12-31")
    baixada_antes = (df["situacao_cadastral"] == "08") & (df["data_situacao_cadastral"] < ini)
    fora = (df["data_inicio_atividade"] > fim) | baixada_antes
    log["fora_do_periodo_removidos"] = int(fora.sum())
    df = df[~fora]
    log["estab_final"] = int(len(df))
    return df.reset_index(drop=True)


def enriquecer_empresas(df):
    bases = set(df["cnpj_basico"])
    emp = []
    for arq in sorted(DIR_RFB.glob("Empresas*.zip")):
        print(f"  lendo {arq.name}")
        for ch in ler_zip_csv(arq, COLS_EMPRESAS):
            ch = ch[ch["cnpj_basico"].str.zfill(8).isin(bases)]
            if not ch.empty:
                emp.append(ch)
    emp = pd.concat(emp, ignore_index=True) if emp else pd.DataFrame(columns=COLS_EMPRESAS)
    emp["cnpj_basico"] = emp["cnpj_basico"].str.zfill(8)
    emp = emp.drop_duplicates("cnpj_basico", keep="last")
    emp["capital_social"] = pd.to_numeric(emp["capital_social"].str.replace(",", "."), errors="coerce")
    emp["porte"] = emp["porte_empresa"].map(PORTE).fillna("NAO INFORMADO")
    emp["razao_social"] = emp["razao_social"].str.upper().map(sem_acento)

    sim = []
    arq = DIR_RFB / "Simples.zip"
    if arq.exists():
        for ch in ler_zip_csv(arq, COLS_SIMPLES):
            ch = ch[ch["cnpj_basico"].str.zfill(8).isin(bases)]
            if not ch.empty:
                sim.append(ch)
    sim = pd.concat(sim, ignore_index=True) if sim else pd.DataFrame(columns=COLS_SIMPLES)
    sim["cnpj_basico"] = sim["cnpj_basico"].str.zfill(8)
    sim = sim.drop_duplicates("cnpj_basico", keep="last")[["cnpj_basico", "opcao_simples", "opcao_mei"]]

    out = df.merge(
        emp[["cnpj_basico", "razao_social", "natureza_juridica", "capital_social", "porte"]],
        on="cnpj_basico", how="left",
    ).merge(sim, on="cnpj_basico", how="left")
    out["porte"] = out["porte"].fillna("NAO INFORMADO")
    out.loc[out["opcao_mei"] == "S", "porte"] = "MEI"   # MEI e destacado do porte "microempresa"

    cnaes = DIR_RFB / "Cnaes.zip"
    if cnaes.exists():
        desc = pd.concat(list(ler_zip_csv(cnaes, ["cnae", "descricao_cnae"])))
        out = out.merge(desc, left_on="cnae_fiscal_principal", right_on="cnae", how="left").drop(columns="cnae")
    return out


def serie_anual(df):
    linhas = []
    grupos = [("TOTAL", df)] + [(d, g) for d, g in df.groupby("divisao_cnae")]
    for nome, g in grupos:
        for ano in range(ANO_INI, ANO_FIM + 1):
            ini, fim = pd.Timestamp(f"{ano}-01-01"), pd.Timestamp(f"{ano}-12-31")
            baixa = (g["situacao_cadastral"] == "08") & g["data_situacao_cadastral"].notna()
            baixada_ate = baixa & (g["data_situacao_cadastral"] <= fim)
            linhas.append({
                "divisao_cnae": nome,
                "ano": ano,
                "aberturas": int(g["data_inicio_atividade"].between(ini, fim).sum()),
                "baixas": int((baixa & g["data_situacao_cadastral"].between(ini, fim)).sum()),
                "ativas_em_31dez": int(((g["data_inicio_atividade"] <= fim) & ~baixada_ate).sum()),
            })
    return pd.DataFrame(linhas)


def salvar(df, nome):
    DIR_OUT.mkdir(parents=True, exist_ok=True)
    df.to_csv(DIR_OUT / nome, index=False, sep=";", encoding="utf-8-sig")
    print(f"  salvo: {DIR_OUT / nome} ({len(df)} linhas)")


def processar_rfb():
    log = {}
    cod = resolver_codigo_municipio()
    log["codigo_municipio_rfb"] = cod
    bruto = extrair_estabelecimentos(cod, log)
    limpo = limpar_estabelecimentos(bruto, log)
    base = enriquecer_empresas(limpo)

    salvar(base, "empresas_vca_setor_primario_2021_2025.csv")
    salvar(serie_anual(base), "serie_anual_empresas.csv")

    ativas = base[base["situacao"] == "ATIVA"]
    salvar(ativas.groupby("porte").size().rename("empresas_ativas").reset_index(), "resumo_porte.csv")
    salvar(ativas.groupby("bairro").size().rename("empresas_ativas").reset_index()
           .sort_values("empresas_ativas", ascending=False), "resumo_bairro.csv")
    salvar(ativas.groupby(["divisao_cnae", "cnae_fiscal_principal"]).size().rename("empresas_ativas")
           .reset_index().sort_values("empresas_ativas", ascending=False), "resumo_cnae.csv")

    DIR_OUT.mkdir(parents=True, exist_ok=True)
    (DIR_OUT / "relatorio_limpeza_rfb.json").write_text(json.dumps(log, indent=2, ensure_ascii=False), encoding="utf-8")
    print("  log de limpeza:", json.dumps(log, ensure_ascii=False))


# ----------------------------------------------------------------------------
# 2) NOVO CAGED
# ----------------------------------------------------------------------------
def baixar_caged():
    DIR_CAGED.mkdir(parents=True, exist_ok=True)
    ftp = ftplib.FTP(CAGED_FTP_HOST, timeout=60)
    ftp.login()
    for ano in range(ANO_INI, ANO_FIM + 1):
        for mes in range(1, 13):
            comp = f"{ano}{mes:02d}"
            for tipo in ("MOV", "FOR", "EXC"):
                nome = f"CAGED{tipo}{comp}.7z"
                destino = DIR_CAGED / nome
                if destino.exists():
                    continue
                caminho = f"{CAGED_FTP_RAIZ}/{ano}/{comp}/{nome}"
                try:
                    with open(destino, "wb") as f:
                        ftp.retrbinary(f"RETR {caminho}", f.write)
                    print(f"  ok {nome}")
                except ftplib.all_errors as e:
                    destino.unlink(missing_ok=True)
                    print(f"  nao disponivel {nome}: {e}")
    ftp.quit()


def normaliza_coluna(c):
    return sem_acento(str(c)).lower().strip().replace(" ", "")


def _ler_7z(caminho):
    try:
        import py7zr
    except ImportError:
        raise SystemExit("Instale o py7zr: pip install py7zr")
    with py7zr.SevenZipFile(caminho) as z:
        dados = z.readall()
    return next(iter(dados.values()))


def _filtrar_municipio(buf):
    primeira = buf.readline()
    buf.seek(0)
    try:
        primeira.decode("utf-8")
        enc = "utf-8"
    except UnicodeDecodeError:
        enc = "latin-1"
    partes = []
    for ch in pd.read_csv(buf, sep=";", dtype=str, encoding=enc, chunksize=500_000):
        ch.columns = [normaliza_coluna(c) for c in ch.columns]
        ch = ch[ch["municipio"] == COD_IBGE_6]
        if not ch.empty:
            partes.append(ch)
    return pd.concat(partes, ignore_index=True) if partes else pd.DataFrame()


def combinar_mov_for_exc(mov, forp, exc):
    """MOV + FOR (fora do prazo) menos EXC (registros excluidos).

    Obs.: NAO se aplica drop_duplicates nos microdados do CAGED: nao ha identificador
    do trabalhador, e linhas identicas podem ser pessoas diferentes.
    """
    base = pd.concat([x for x in (mov, forp) if not x.empty], ignore_index=True) if (not mov.empty or not forp.empty) else pd.DataFrame()
    if base.empty or exc.empty:
        return base
    chave = [c for c in base.columns if c in exc.columns]
    marca = exc[chave].drop_duplicates().assign(_exc=1)
    base = base.merge(marca, on=chave, how="left")
    return base[base["_exc"].isna()].drop(columns="_exc").reset_index(drop=True)


def tratar_caged(df):
    df = df.copy()
    df["divisao_cnae"] = df["subclasse"].str.zfill(7).str[:2]
    df = df[df["divisao_cnae"].isin(DIVISOES)]
    df["ano"] = df["competenciamov"].str[:4].astype(int)
    df = df[df["ano"].between(ANO_INI, ANO_FIM)]
    df["saldomovimentacao"] = pd.to_numeric(df["saldomovimentacao"], errors="coerce")
    df["salario"] = pd.to_numeric(df["salario"].str.replace(",", "."), errors="coerce")
    df["idade"] = pd.to_numeric(df["idade"], errors="coerce")
    return df.reset_index(drop=True)


def resumo_caged(df):
    df = df.assign(adm=(df["saldomovimentacao"] == 1).astype(int),
                   des=(df["saldomovimentacao"] == -1).astype(int))
    df["salario_adm"] = df["salario"].where(df["adm"] == 1)
    ag = df.groupby(["competenciamov", "divisao_cnae"]).agg(
        admissoes=("adm", "sum"), desligamentos=("des", "sum"),
        saldo=("saldomovimentacao", "sum"), salario_medio_admitidos=("salario_adm", "mean"),
    ).reset_index()
    return ag


def processar_caged():
    meses = sorted({p.name[-9:-3] for p in DIR_CAGED.glob("CAGEDMOV*.7z")})
    if not meses:
        raise SystemExit(f"Nenhum CAGEDMOV*.7z em {DIR_CAGED}")
    todos = []
    for comp in meses:
        print(f"  competencia {comp}")
        partes = {}
        for tipo in ("MOV", "FOR", "EXC"):
            arq = DIR_CAGED / f"CAGED{tipo}{comp}.7z"
            partes[tipo] = _filtrar_municipio(_ler_7z(arq)) if arq.exists() else pd.DataFrame()
        liquido = combinar_mov_for_exc(partes["MOV"], partes["FOR"], partes["EXC"])
        if not liquido.empty:
            todos.append(liquido)
    if not todos:
        raise SystemExit("Sem movimentacoes para o municipio.")
    base = tratar_caged(pd.concat(todos, ignore_index=True))
    salvar(base, "caged_vca_setor_primario_microdados.csv")
    salvar(resumo_caged(base), "caged_vca_setor_primario_mensal.csv")


# ----------------------------------------------------------------------------
# 3) SIDRA / IBGE
# ----------------------------------------------------------------------------
def processar_sidra():
    DIR_SIDRA.mkdir(parents=True, exist_ok=True)
    for nome, params in SIDRA_CONSULTAS.items():
        url = f"https://apisidra.ibge.gov.br/values/{params}"
        print(f"  {nome}: {url}")
        try:
            with urllib.request.urlopen(url, timeout=120) as r:
                dados = json.load(r)
        except Exception as e:  # noqa: BLE001
            print(f"  FALHOU {nome}: {e}")
            continue
        cab = dados[0]
        df = pd.DataFrame(dados[1:]).rename(columns=cab)
        if "Ano" in df.columns:
            df = df[df["Ano"].astype(int).between(ANO_INI, ANO_FIM)]
        if "Valor" in df.columns:
            df["Valor"] = pd.to_numeric(df["Valor"], errors="coerce")  # '-', '...', 'X' viram NaN
        df = df.drop_duplicates()
        salvar(df, f"sidra_{nome}.csv")


# ----------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("etapa", choices=["baixar-rfb", "rfb", "baixar-caged", "caged", "sidra", "tudo"])
    a = ap.parse_args()
    if a.etapa == "baixar-rfb":
        baixar_rfb()
    elif a.etapa == "rfb":
        processar_rfb()
    elif a.etapa == "baixar-caged":
        baixar_caged()
    elif a.etapa == "caged":
        processar_caged()
    elif a.etapa == "sidra":
        processar_sidra()
    else:
        processar_rfb()
        processar_caged()
        processar_sidra()


if __name__ == "__main__":
    main()