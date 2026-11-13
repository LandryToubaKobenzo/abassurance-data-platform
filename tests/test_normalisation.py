
import pytest

from abassurance.normalisation import (
    normaliser_client_ab,
    normaliser_client_ap,
    normaliser_date,
    normaliser_email,
    normaliser_texte,
)


def test_normaliser_texte():
    assert normaliser_texte("  Jean   Dupont  ") == "Jean Dupont"
    assert normaliser_texte(None) is None
    assert normaliser_texte("   ") is None


def test_normaliser_email():
    assert normaliser_email("  TEST@EXEMPLE.FR ") == "test@exemple.fr"
    assert normaliser_email(None) is None


def test_normaliser_date():
    assert normaliser_date("1990-05-12") == "1990-05-12"
    assert normaliser_date(None) is None


def test_date_invalide():
    with pytest.raises(ValueError, match="Date invalide"):
        normaliser_date("2026-99-99")


def test_normaliser_client_ab():
    client = {
        "AB_CLIENT_ID": 101,
        "AB_NOM": "  DUPONT ",
        "AB_PRENOM": " Jean ",
        "AB_DATE_NAISSANCE": "1990-05-12",
        "AB_EMAIL": " JEAN@EXEMPLE.FR ",
        "AB_TELEPHONE": " 0601020304 ",
    }

    resultat = normaliser_client_ab(client)

    assert resultat["systeme_source"] == "ABASSURANCE"
    assert resultat["identifiant_source"] == "101"
    assert resultat["nom"] == "DUPONT"
    assert resultat["prenom"] == "Jean"
    assert resultat["email"] == "jean@exemple.fr"


def test_normaliser_client_ap():
    client = {
        "AP_USER_ID": 202,
        "AP_FULL_NAME": "  Marie   Martin ",
        "AP_BIRTH_DATE": "1988-09-21",
        "AP_MAIL_ADDRESS": " MARIE@EXEMPLE.FR ",
        "AP_PHONE_NUMBER": " 0611223344 ",
    }

    resultat = normaliser_client_ap(client)

    assert resultat["systeme_source"] == "ASSUREPLUS"
    assert resultat["identifiant_source"] == "202"
    assert resultat["nom_complet"] == "Marie Martin"
    assert resultat["date_naissance"] == "1988-09-21"
    assert resultat["email"] == "marie@exemple.fr"
