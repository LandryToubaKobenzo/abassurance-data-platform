"""Tests automatisés de l'API FastAPI AbAssurance."""

from fastapi.testclient import TestClient

from abassurance.api import app

client = TestClient(app)


def test_health():
    """L'API doit répondre avec un statut OK."""
    reponse = client.get("/health")

    assert reponse.status_code == 200
    assert reponse.json() == {"statut": "ok"}


def test_prediction_valide(monkeypatch):
    """Une requête valide doit retourner une prédiction."""
    monkeypatch.setattr(
        "abassurance.api.predire_risque",
        lambda age, sinistres_precedents, anciennete_contrat: "Élevé",
    )

    reponse = client.post(
        "/predict",
        json={
            "age": 51,
            "sinistres_precedents": 6,
            "anciennete_contrat": 3,
        },
    )

    assert reponse.status_code == 200
    assert reponse.json() == {"risque_predit": "Élevé"}


def test_age_invalide():
    """Un âge inférieur à 18 ans doit être refusé."""
    reponse = client.post(
        "/predict",
        json={
            "age": 15,
            "sinistres_precedents": 2,
            "anciennete_contrat": 3,
        },
    )

    assert reponse.status_code == 422


def test_sinistres_invalides():
    """Un nombre de sinistres négatif doit être refusé."""
    reponse = client.post(
        "/predict",
        json={
            "age": 45,
            "sinistres_precedents": -1,
            "anciennete_contrat": 3,
        },
    )

    assert reponse.status_code == 422


def test_modele_indisponible(monkeypatch):
    """L'API doit retourner 503 si le modèle est introuvable."""

    def modele_absent(*args):
        raise FileNotFoundError("Modèle introuvable")

    monkeypatch.setattr(
        "abassurance.api.predire_risque",
        modele_absent,
    )

    reponse = client.post(
        "/predict",
        json={
            "age": 45,
            "sinistres_precedents": 2,
            "anciennete_contrat": 3,
        },
    )

    assert reponse.status_code == 503
    assert reponse.json() == {
        "detail": "Modèle de prédiction indisponible."
    }
