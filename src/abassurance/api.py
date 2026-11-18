
"""API REST pédagogique pour la prédiction du risque de sinistre."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from abassurance.prediction import predire_risque

app = FastAPI(
    title="AbAssurance - API de prédiction",
    description=(
        "API pédagogique de prédiction du risque de sinistre "
        "sur des données synthétiques. Ne pas utiliser pour "
        "des décisions réelles concernant des assurés."
    ),
    version="1.0.0",
)

class DonneesAssure(BaseModel):
    """Caractéristiques fictives utilisées pour la prédiction."""

    age: int = Field(ge=18, le=100, description="Âge de l’assuré")
    sinistres_precedents: int = Field(
        ge=0, le=20, description="Nombre de sinistres précédents"
    )
    anciennete_contrat: int = Field(
        ge=0, le=80, description="Ancienneté du contrat en années"
    )

class ResultatPrediction(BaseModel):
    """Résultat retourné par l’API."""

    risque_predit: str

@app.get("/health")
def verifier_api():
    """Vérifie que le service API répond."""
    return {"statut": "ok"}

@app.post("/predict", response_model=ResultatPrediction)
def predire(donnees: DonneesAssure):
    """Prédit le niveau de risque à partir du modèle sauvegardé."""
    try:
        risque = predire_risque(
            donnees.age,
            donnees.sinistres_precedents,
            donnees.anciennete_contrat,
        )
    except FileNotFoundError as erreur:
        raise HTTPException(
            status_code=503, detail="Modèle de prédiction indisponible."
        ) from erreur

    return ResultatPrediction(risque_predit=risque)
