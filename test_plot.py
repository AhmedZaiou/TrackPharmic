import random
import datetime


def generer_all_data_jour(nb_jours=30):
    # Génère les dates des nb_jours derniers jours
    jours = [
        (datetime.date.today() - datetime.timedelta(days=i)).strftime("%d-%m")
        for i in range(nb_jours)
    ][::-1]

    # Génère des valeurs aléatoires pour chaque type de donnée
    credits = [random.randint(500, 5000) for _ in range(nb_jours)]
    echanges_envoyer = [random.randint(0, 2000) for _ in range(nb_jours)]
    echanges_recu = [random.randint(0, 2000) for _ in range(nb_jours)]
    paiements = [random.randint(300, 4000) for _ in range(nb_jours)]
    retours = [random.randint(0, 500) for _ in range(nb_jours)]
    ventes = [random.randint(500, 6000) for _ in range(nb_jours)]

    # Construction du dictionnaire dans le format demandé
    all_data_jour = {
        "jours": jours,
        "credits": credits,
        "echanges_envoyer": echanges_envoyer,
        "echanges_recu": echanges_recu,
        "paiements": paiements,
        "retours": retours,
        "ventes": ventes,
    }
    return all_data_jour


# Exemple d'utilisation
if __name__ == "__main__":
    data = generer_all_data_jour(10)  # 10 derniers jours
    print(data)
