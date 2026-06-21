
from pathlib import Path
import sys

import numpy as np
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))

from app.model_service import modelo_nictemeral_service


MODELOS_DIR = BASE_DIR / "modelos_camarao"
ARQUIVO_REAL = MODELOS_DIR / "dados_nictemerais_rotulados.csv"
ARQUIVO_SAIDA = MODELOS_DIR / "dados_sinteticos_nictemerais.csv"


VARIAVEIS_MODELO = [
    "temperatura",
    "ph",
    "od",
    "salinidade",
    "condutividade",
    "transparencia",
    "hora_decimal",
]


RUIDO = {
    "temperatura": 0.5,
    "ph": 0.12,
    "od": 0.5,
    "salinidade": 1.0,
    "condutividade": 1.0,
    "transparencia": 3.0,
    "hora_decimal": 0.5,
}


LIMITES_PLAUSIVEIS = {
    "temperatura": (25.0, 35.0),
    "ph": (7.0, 9.5),
    "od": (0.5, 12.0),
    "salinidade": (25.0, 45.0),
    "condutividade": (40.0, 65.0),
    "transparencia": (10.0, 45.0),
    "hora_decimal": (0.0, 23.99),
}


def periodo_do_dia(hora_decimal: float) -> str:
    hora = int(hora_decimal)

    if 5 <= hora < 12:
        return "manha"
    if 12 <= hora < 18:
        return "tarde"
    if 18 <= hora < 24:
        return "noite"
    return "madrugada"


def gerar_dados_sinteticos(n_amostras: int = 1000, seed: int = 42) -> pd.DataFrame:
    np.random.seed(seed)

    df_real = pd.read_csv(ARQUIVO_REAL)

    registros_sinteticos = []

    for i in range(n_amostras):
        registro_base = df_real.sample(1).iloc[0].copy()
        novo = {}

        for variavel in VARIAVEIS_MODELO:
            valor_base = float(registro_base[variavel])
            desvio = RUIDO[variavel]

            valor_sintetico = np.random.normal(loc=valor_base, scale=desvio)

            limite_min, limite_max = LIMITES_PLAUSIVEIS[variavel]
            valor_sintetico = np.clip(valor_sintetico, limite_min, limite_max)

            novo[variavel] = round(float(valor_sintetico), 3)

        classificacao = modelo_nictemeral_service.classificar(novo)

        novo["cluster"] = classificacao["cluster"]
        novo["estado_agua"] = classificacao["estado_agua"]
        novo["mensagem"] = classificacao["mensagem"]
        novo["pca1"] = classificacao["pca1"]
        novo["pca2"] = classificacao["pca2"]

        novo["periodo_dia"] = periodo_do_dia(novo["hora_decimal"])
        novo["origem"] = "sintetico"
        novo["id_sintetico"] = i + 1

        registros_sinteticos.append(novo)

    return pd.DataFrame(registros_sinteticos)


if __name__ == "__main__":
    df_sintetico = gerar_dados_sinteticos(n_amostras=1000, seed=42)

    df_sintetico.to_csv(ARQUIVO_SAIDA, index=False, encoding="utf-8-sig")

    print(f"Arquivo gerado: {ARQUIVO_SAIDA}")
    print(f"Total de registros sinteticos: {len(df_sintetico)}")

    print("\nDistribuicao por estado da agua:")
    print(df_sintetico["estado_agua"].value_counts())

    print("\nDistribuicao por periodo do dia:")
    print(df_sintetico["periodo_dia"].value_counts())
