
import json

import pytest

from abassurance.pipeline import (
    analyser_clients,
    executer_pipeline,
    unifier_clients,
)


def test_unifier_clients():
    clients_ab = [
        {
            "AB_CLIENT_ID": 101,
            "AB_NOM": " Dupont ",
            "AB_PRENOM": "Jean",
            "AB_EMAIL": " JEAN@EXEMPLE.FR ",
            "AB_DATE_NAISSANCE": "1990-05-12",
        }
    ]

    clients_ap = [
        {
            "AP_USER_ID": 202,
            "AP_FULL_NAME": "Marie Martin",
            "AP_MAIL_ADDRESS": "MARIE@EXEMPLE.FR",
            "AP_BIRTH_DATE": "1988-09-21",
        }
    ]

    resultat = unifier_clients(clients_ab, clients_ap)

    assert len(resultat) == 2
    assert resultat[0]["systeme_source"] == "ABASSURANCE"
    assert resultat[0]["identifiant_source"] == "101"
    assert resultat[0]["email"] == "jean@exemple.fr"
    assert resultat[1]["systeme_source"] == "ASSUREPLUS"
    assert resultat[1]["identifiant_source"] == "202"


def test_executer_pipeline(tmp_path):
    source_ab = tmp_path / "clients_ab.json"
    source_ap = tmp_path / "clients_ap.json"
    sortie = tmp_path / "resultats" / "clients_unifies.json"

    source_ab.write_text(
        json.dumps([{"AB_CLIENT_ID": 1, "AB_NOM": "Martin"}]),
        encoding="utf-8",
    )
    source_ap.write_text(
        json.dumps([{"AP_USER_ID": 2, "AP_FULL_NAME": "Marie Martin"}]),
        encoding="utf-8",
    )

    nombre = executer_pipeline(source_ab, source_ap, sortie)

    assert nombre == 2
    assert sortie.exists()

    resultat = json.loads(sortie.read_text(encoding="utf-8"))
    assert len(resultat) == 2
    assert resultat[0]["identifiant_source"] == "1"
    assert resultat[1]["identifiant_source"] == "2"


def test_rejeter_source_non_liste(tmp_path):
    source_ab = tmp_path / "clients_ab.json"
    source_ap = tmp_path / "clients_ap.json"
    sortie = tmp_path / "sortie.json"

    source_ab.write_text("{}", encoding="utf-8")
    source_ap.write_text("[]", encoding="utf-8")

    with pytest.raises(TypeError, match="listes JSON"):
        executer_pipeline(source_ab, source_ap, sortie)

    assert not sortie.exists()

def test_analyser_clients_detecte_correspondance():
    """Détecte un rapprochement candidat entre deux sources distinctes."""
    clients_ab = [
        {
            "AB_CLIENT_ID": 101,
            "AB_NOM": "Dupont",
            "AB_PRENOM": "Jean",
            "AB_EMAIL": "JEAN@EXEMPLE.FR",
            "AB_DATE_NAISSANCE": "1990-05-12",
        }
    ]

    clients_ap = [
        {
            "AP_USER_ID": 202,
            "AP_FULL_NAME": "Jean Dupont",
            "AP_MAIL_ADDRESS": "jean@exemple.fr",
            "AP_BIRTH_DATE": "1990-05-12",
        }
    ]

    resultat = analyser_clients(clients_ab, clients_ap)

    assert len(resultat["clients"]) == 2
    assert len(resultat["correspondances_candidates"]) == 1

    groupe = resultat["correspondances_candidates"][0]

    assert len(groupe) == 2
    assert {client["systeme_source"] for client in groupe} == {
        "ABASSURANCE",
        "ASSUREPLUS",
    }
    assert {client["identifiant_source"] for client in groupe} == {
        "101",
        "202",
    }
