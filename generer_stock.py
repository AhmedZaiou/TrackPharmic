from Backend.Dataset.stock import Stock
from Backend.Dataset.medicament import Medicament
import datetime
import random
import pymysql
from Frontend.utils.utils import *


def random_datetime_within_2_years():
    start = datetime.datetime.now()
    end = start + datetime.timedelta(days=365 * 2)  # 2 ans
    # Générer un timestamp aléatoire entre les deux dates
    random_timestamp = random.uniform(start.timestamp(), end.timestamp())
    return datetime.datetime.fromtimestamp(random_timestamp)


def generer_stock():
    # Stock initial entre 50 et 500 unités
    stock_initial = random.randint(5, 30)

    # Quantité maximale (au moins égale au stock initial, mais avec une marge)
    quantite_maximale = stock_initial + random.randint(5, 30)

    # Quantité minimale (au moins 10, mais toujours < stock_initial)
    quantite_minimale = random.randint(15, max(15, stock_initial // 2))

    # Quantité actuelle (entre 0 et quantite_maximale)
    quantite_actuelle = random.randint(0, quantite_maximale)

    return {
        "stock_initial": stock_initial,
        "quantite_actuelle": quantite_actuelle,
        "quantite_minimale": quantite_minimale,
        "quantite_maximale": quantite_maximale,
    }


conn = pymysql.connect(host=host, user=user, password=password, database=database)

medicaments = Medicament.extraire_tous_medicament(conn)

for element, i in zip(medicaments, range(10000)):
    stock_values = generer_stock()

    Stock.ajouter_stock(
        conn,
        element["id_medicament"],
        0,
        1,
        float(element["PPV"]) - float(element["PPV"]) * 0.3,
        float(element["PPV"]),
        float(element["PPV"]),
        datetime.datetime.now(),
        random_datetime_within_2_years(),
        stock_values["stock_initial"],
        stock_values["quantite_actuelle"],
        stock_values["quantite_minimale"],
        stock_values["quantite_maximale"],
        datetime.datetime.now(),
        datetime.datetime.now(),
    )
