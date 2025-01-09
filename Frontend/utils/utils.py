from pathlib import Path 


current_directory = Path(__file__).parent
Front_end = current_directory.parent 

Tracpharmic = Path.home()/"Tracpharmic"

images = Tracpharmic/"images"

dataset = Tracpharmic/"dataset"/"pharmadataset.db"


name_application = "TracPharmic"  


def set_styles():
    try:
        with open(Front_end/"style"/"style.qss", "r") as file:
            style = file.read()
            """background_path_str =  str(background_path).replace("\\", "/") 
            arrowdrop_str =  str(arrowdrop).replace("\\", "/") 
            style = style.replace("background_image",background_path_str)
            style = style.replace("arrowdrop", arrowdrop_str)""" 
            return style
    except FileNotFoundError:
        print("Style file not found. Using default styles.")






deconexion_logo = "/Users/ahmedzaiou/Documents/ProjetsApps/TrackPharmic/Frontend/images/deconexion.png"

salare_logo = "/Users/ahmedzaiou/Documents/ProjetsApps/TrackPharmic/Frontend/images/salarielogo.png"

kpi_logo = "/Users/ahmedzaiou/Documents/ProjetsApps/TrackPharmic/Frontend/images/kpi.png"
acceuil_logo = "/Users/ahmedzaiou/Documents/ProjetsApps/TrackPharmic/Frontend/images/logoacceuil.png"
commande_logo = "/Users/ahmedzaiou/Documents/ProjetsApps/TrackPharmic/Frontend/images/commandelogo.png"
credit_logo = "/Users/ahmedzaiou/Documents/ProjetsApps/TrackPharmic/Frontend/images/creditlogo.png"
vente_logo = "/Users/ahmedzaiou/Documents/ProjetsApps/TrackPharmic/Frontend/images/ventelogo.svg"
client_logo = "/Users/ahmedzaiou/Documents/ProjetsApps/TrackPharmic/Frontend/images/clientlogo.png"
echange_logo = "/Users/ahmedzaiou/Documents/ProjetsApps/TrackPharmic/Frontend/images/echangelogo.png"
stock_logo = "/Users/ahmedzaiou/Documents/ProjetsApps/TrackPharmic/Frontend/images/stocklogo.png"
