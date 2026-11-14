
"""Démonstration de traitement de données avec Apache Spark."""

import json
from pathlib import Path

from pyspark.sql import SparkSession


def main():
    """Lit les clients unifiés et calcule des statistiques simples."""

    chemin = Path("data/processed/clients_unifies.json")

    with chemin.open(encoding="utf-8") as fichier:
        contenu = json.load(fichier)

    # Le pipeline produit un document JSON structuré.
    if isinstance(contenu, list):
        clients = contenu
    elif isinstance(contenu, dict):
        clients = contenu.get("clients", [])
    else:
        raise TypeError("Format JSON inattendu")

    spark = (
        SparkSession.builder
        .appName("AbAssurance-Bachelor-Spark")
        .master("local[2]")
        .getOrCreate()
    )

    try:
        print("=== Démonstration Apache Spark ===")

        if not clients:
            print("Aucun client à analyser.")
            return

        donnees = [
            (json.dumps(client, ensure_ascii=False),)
            for client in clients
        ]

        dataframe = spark.createDataFrame(
            donnees,
            ["client_json"],
        )

        print(f"Nombre de clients unifiés : {dataframe.count()}")
        dataframe.show(truncate=False)

    finally:
        spark.stop()


if __name__ == "__main__":
    main()
