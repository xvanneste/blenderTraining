"""Compare une recherche linéaire répétée à un index par nom."""
from timeit import repeat


def mesure(taille=5000):
    lignes = [(f"PLAN_{i:05}", i) for i in range(taille)]
    demandes = [f"PLAN_{i:05}" for i in range(0, taille, 19)]

    def parcours():
        return [next(valeur for nom, valeur in lignes if nom == cle) for cle in demandes]

    def index():
        table = dict(lignes)
        return [table[cle] for cle in demandes]

    assert parcours() == index()
    return {
        test.__name__: min(repeat(test, number=3, repeat=3)) / 3
        for test in (parcours, index)
    }


if __name__ == "__main__":
    for methode, secondes in mesure().items():
        print(f"{methode}: {secondes * 1000:.3f} ms")
