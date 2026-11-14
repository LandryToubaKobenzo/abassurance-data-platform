
"""Validation des données d'assurance."""

from decimal import Decimal, InvalidOperation


def normalize_email(email: str | None) -> str | None:
    """Normalise une adresse email."""

    if email is None:
        return None

    normalized = email.strip().lower()

    return normalized or None


def validate_premium(amount: object) -> bool:
    """Vérifie qu'une prime est numérique et positive ou nulle."""

    if amount is None or isinstance(amount, bool):
        return False

    try:
        value = Decimal(str(amount))
    except (InvalidOperation, ValueError):
        return False

    return value.is_finite() and value >= 0


def client_key(source: str, client_id: str) -> str:
    """Construit une clé technique multi-sources."""

    if not source.strip() or not client_id.strip():
        raise ValueError("Source ou identifiant manquant")

    return f"{source.strip().upper()}:{client_id.strip()}"
