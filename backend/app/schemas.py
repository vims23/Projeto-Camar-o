from pydantic import BaseModel, Field


class MedicaoNictemeralEntrada(BaseModel):
    temperatura: float = Field(..., description="Temperatura da agua em graus Celsius")
    ph: float = Field(..., description="pH da agua")
    od: float = Field(..., description="Oxigenio dissolvido em mg/L")
    salinidade: float = Field(..., description="Salinidade")
    condutividade: float = Field(..., description="Condutividade")
    transparencia: float = Field(..., description="Transparencia")
    hora_decimal: float = Field(..., ge=0, le=24, description="Hora em formato decimal. Ex: 5.5 = 05:30")


class ClassificacaoNictemeralSaida(BaseModel):
    cluster: int
    estado_agua: str
    mensagem: str
    pca1: float
    pca2: float


class HealthResponse(BaseModel):
    status: str
    modelo_carregado: bool
