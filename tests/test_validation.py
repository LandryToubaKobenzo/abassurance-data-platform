
import pytest

from abassurance.validation import (
    client_key,
    normalize_email,
    validate_premium,
)


def test_normalize_email():
    assert normalize_email(
        "  CLIENT@EXEMPLE.FR "
    ) == "client@exemple.fr"


def test_empty_email():
    assert normalize_email("   ") is None


def test_missing_email():
    assert normalize_email(None) is None


def test_positive_premium():
    assert validate_premium("1250.50") is True


def test_negative_premium():
    assert validate_premium("-100") is False


def test_invalid_premium():
    assert validate_premium("inconnu") is False


def test_missing_premium():
    assert validate_premium(None) is False


def test_nan_premium():
    assert validate_premium("NaN") is False


def test_different_client_sources():
    oracle = client_key("ORACLE", "1001")
    sqlserver = client_key("SQLSERVER", "1001")

    assert oracle != sqlserver


def test_missing_client_id():
    with pytest.raises(ValueError):
        client_key("ORACLE", "  ")
