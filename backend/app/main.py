from fastapi import FastAPI

from app.model_service import modelo_nictemeral_service
from app.schemas import (
    ClassificacaoNictemeralSaida,
    HealthResponse,
    MedicaoNictemeralEntrada,
)


app = FastAPI(
    title="Projeto Camarao API",
    description="API para classificacao operacional da qualidade da agua em viveiros de camarao.",
    version="0.1.0",
)


@app.get("/", response_model=HealthResponse)
def root():
    return {
        "status": "ok",
        "modelo_carregado": modelo_nictemeral_service is not None,
    }


@app.get("/health", response_model=HealthResponse)
def health():
    return {
        "status": "ok",
        "modelo_carregado": modelo_nictemeral_service is not None,
    }


@app.post("/classificar-nictemeral", response_model=ClassificacaoNictemeralSaida)
def classificar_nictemeral(medicao: MedicaoNictemeralEntrada):
    return modelo_nictemeral_service.classificar(medicao.dict())
