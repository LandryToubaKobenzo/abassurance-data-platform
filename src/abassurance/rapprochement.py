
"""Détection de correspondances entre clients des deux compagnies."""

from collections import defaultdict

from abassurance.normalisation import normaliser_email, normaliser_texte


def nom_complet_client(client):
    """Construit un nom comparable sans découper les noms AssurePlus."""
    if client.get("nom_complet"):
        return normaliser_texte(client["nom_complet"]).casefold()

    nom = normaliser_texte(client.get("nom"))
    prenom = normaliser_texte(client.get("prenom"))

    if not nom or not prenom:
        return None

    return f"{prenom} {nom}".casefold()


def cle_rapprochement(client):
    """Retourne une clé uniquement si tous les critères sont présents."""
    nom = nom_complet_client(client)
    naissance = client.get("date_naissance")
    email = normaliser_email(client.get("email"))

    if not nom or not naissance or not email:
        return None

    return (nom, naissance, email)


def detecter_correspondances(clients):
    """Détecte des groupes candidats provenant de sources distinctes."""
    groupes = defaultdict(list)

    for client in clients:
        cle = cle_rapprochement(client)
        if cle is not None:
            groupes[cle].append(client)

    correspondances = []

    for groupe in groupes.values():
        sources = {client["systeme_source"] for client in groupe}

        if len(groupe) > 1 and len(sources) > 1:
            correspondances.append(groupe)

    return correspondances
