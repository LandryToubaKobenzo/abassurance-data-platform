
"""Tests du rapprochement des clients AbAssurance et AssurePlus."""

from abassurance.rapprochement import (
    cle_rapprochement,
    detecter_correspondances,
    nom_complet_client,
)


def test_nom_complet_ab():
    client = {"nom": "Dupont", "prenom": "Jean"}

    assert nom_complet_client(client) == "jean dupont"


def test_nom_complet_ap():
    client = {"nom_complet": "  Jean   Dupont  "}

    assert nom_complet_client(client) == "jean dupont"


def test_cle_rapprochement_identique():
    client_ab = {
        "nom": "Dupont",
        "prenom": "Jean",
        "date_naissance": "1990-05-12",
        "email": "Jean.Dupont@example.fr",
    }

    client_ap = {
        "nom_complet": "Jean Dupont",
        "date_naissance": "1990-05-12",
        "email": "jean.dupont@example.fr",
    }

    assert cle_rapprochement(client_ab) == cle_rapprochement(client_ap)


def test_detection_correspondance_entre_sources():
    clients = [
        {
            "systeme_source": "ABASSURANCE",
            "identifiant_source": "101",
            "nom": "Dupont",
            "prenom": "Jean",
            "date_naissance": "1990-05-12",
            "email": "jean.dupont@example.fr",
        },
        {
            "systeme_source": "ASSUREPLUS",
            "identifiant_source": "201",
            "nom_complet": "Jean Dupont",
            "date_naissance": "1990-05-12",
            "email": "jean.dupont@example.fr",
        },
    ]

    correspondances = detecter_correspondances(clients)

    assert len(correspondances) == 1
    assert len(correspondances[0]) == 2

    identifiants = {
        (client["systeme_source"], client["identifiant_source"])
        for client in correspondances[0]
    }

    assert identifiants == {
        ("ABASSURANCE", "101"),
        ("ASSUREPLUS", "201"),
    }


def test_pas_de_correspondance_clients_differents():
    clients = [
        {
            "systeme_source": "ABASSURANCE",
            "nom": "Martin",
            "prenom": "Sophie",
            "date_naissance": "1985-08-20",
            "email": "sophie.martin@example.fr",
        },
        {
            "systeme_source": "ASSUREPLUS",
            "nom_complet": "Marie Bernard",
            "date_naissance": "1992-11-03",
            "email": "marie.bernard@example.fr",
        },
    ]

    assert detecter_correspondances(clients) == []


def test_pas_de_rapprochement_sans_email():
    client = {
        "nom": "Dupont",
        "prenom": "Jean",
        "date_naissance": "1990-05-12",
        "email": None,
    }

    assert cle_rapprochement(client) is None


def test_pas_de_rapprochement_meme_source():
    client = {
        "systeme_source": "ABASSURANCE",
        "nom": "Dupont",
        "prenom": "Jean",
        "date_naissance": "1990-05-12",
        "email": "jean.dupont@example.fr",
    }

    assert detecter_correspondances([client, client.copy()]) == []
