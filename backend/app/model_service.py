import json
from pathlib import Path

import joblib
import pandas as pd


class ModeloNictemeralService:
    def __init__(self):
        base_dir = Path(__file__).resolve().parents[1]
        self.modelos_dir = base_dir / "modelos_camarao"

        self.imputador = joblib.load(self.modelos_dir / "imputador_nict.joblib")
        self.padronizador = joblib.load(self.modelos_dir / "padronizador_nict.joblib")
        self.pca = joblib.load(self.modelos_dir / "pca_nict.joblib")
        self.kmeans = joblib.load(self.modelos_dir / "kmeans_nict.joblib")

        with open(self.modelos_dir / "config_modelo_nict.json", "r", encoding="utf-8") as arquivo:
            self.config = json.load(arquivo)

        self.variaveis_entrada = self.config["variaveis_entrada"]
        self.mapa_estado = {
            int(cluster): estado
            for cluster, estado in self.config["mapa_estado_nictemeral"].items()
        }
        self.mensagens = self.config["mensagens"]

    def classificar(self, medicao: dict) -> dict:
        entrada = pd.DataFrame([medicao])

        entrada = entrada[self.variaveis_entrada]

        entrada_imputada = self.imputador.transform(entrada)
        entrada_padronizada = self.padronizador.transform(entrada_imputada)

        cluster = int(self.kmeans.predict(entrada_padronizada)[0])
        pca_xy = self.pca.transform(entrada_padronizada)[0]

        estado = self.mapa_estado.get(cluster, "indefinido")
        mensagem = self.mensagens.get(estado, "Estado nao identificado.")

        return {
            "cluster": cluster,
            "estado_agua": estado,
            "mensagem": mensagem,
            "pca1": float(pca_xy[0]),
            "pca2": float(pca_xy[1]),
        }


modelo_nictemeral_service = ModeloNictemeralService()
