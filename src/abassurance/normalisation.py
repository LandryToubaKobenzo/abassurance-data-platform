
from datetime import datetime


def normaliser_texte(valeur):
    """Nettoie un texte sans inventer de valeur."""
    if valeur is None:
        return None
    texte = str(valeur).strip()
    return " ".join(texte.split()) or None


def normaliser_date(valeur):
    """Convertit une date connue au format ISO AAAA-MM-JJ."""
    if valeur is None:
        return None

    if isinstance(valeur, datetime):
        return valeur.date().isoformat()

    texte = normaliser_texte(valeur)
    if texte is None:
        return None

    try:
        return datetime.strptime(texte, "%Y-%m-%d").date().isoformat()
    except ValueError as exc:
        raise ValueError(f"Date invalide : {valeur}") from exc


def normaliser_email(valeur):
    """Uniformise la casse et les espaces d'un email."""
    texte = normaliser_texte(valeur)
    return texte.lower() if texte else None


def normaliser_client_ab(enregistrement):
    """Transforme un client Oracle AbAssurance."""
    return {
        "systeme_source": "ABASSURANCE",
        "identifiant_source": str(enregistrement["AB_CLIENT_ID"]),
        "nom": normaliser_texte(enregistrement.get("AB_NOM")),
        "prenom": normaliser_texte(enregistrement.get("AB_PRENOM")),
        "date_naissance": normaliser_date(
            enregistrement.get("AB_DATE_NAISSANCE")
        ),
        "email": normaliser_email(enregistrement.get("AB_EMAIL")),
        "telephone": normaliser_texte(
            enregistrement.get("AB_TELEPHONE")
        ),
    }


def normaliser_client_ap(enregistrement):
    """Transforme un client SQL Server AssurePlus."""
    return {
        "systeme_source": "ASSUREPLUS",
        "identifiant_source": str(enregistrement["AP_USER_ID"]),
        "nom_complet": normaliser_texte(
            enregistrement.get("AP_FULL_NAME")
        ),
        "date_naissance": normaliser_date(
            enregistrement.get("AP_BIRTH_DATE")
        ),
        "email": normaliser_email(
            enregistrement.get("AP_MAIL_ADDRESS")
        ),
        "telephone": normaliser_texte(
            enregistrement.get("AP_PHONE_NUMBER")
        ),
    }
