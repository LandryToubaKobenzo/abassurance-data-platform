
"""Exécute le pipeline d'unification des clients."""

from abassurance.pipeline import executer_pipeline


def main():
    nombre_clients = executer_pipeline(
        "data/raw/clients_ab.json",
        "data/raw/clients_ap.json",
        "data/processed/clients_unifies.json",
    )

    print(f"Pipeline exécuté : {nombre_clients} clients traités.")


if __name__ == "__main__":
    main()
