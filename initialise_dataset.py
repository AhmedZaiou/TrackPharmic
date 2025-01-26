from Backend.Dataset.dataset import *



supprimer_toute_base_donnees()


create_table_medicament()

create_table_phaemacies()
create_table_stock()

create_table_ventes()

create_table_achats()

create_table_commandes()

create_table_salaries()
create_table_clients()

create_table_echanges()
create_table_credit()
create_table_fournisseur()
create_table_payment()

ajouter_salarie("user", "prenom", "cin","Telephone", "Email", "Adresse", "photo", "199", "type_contrat", "", "grade", "user")
ajouter_salarie("admin", "prenom", "cin","Telephone", "Email", "Adresse", "photo", "199", "type_contrat", "", "admin", "admin")