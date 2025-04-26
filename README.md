# TrackPharmic


pyinstaller main.py

https://dmp.sante.gov.ma/recherche-medicaments




 pharmacieapplication@gmail.com
 Pharmaciehajra



# Steps to create app in mac 

pyinstaller --onefile --windowed --name "Pharma" --add-data  "Frontend/images:Frontend/images" --add-data  "Frontend/style:Frontend/style"  --icon="Frontend/images/pharmacie_bloc.png" main.py



pyinstaller --onefile --windowed --name "Pharma"   --add-data "Frontend/images:Frontend/images"   --add-data "Frontend/style:Frontend/style"   --icon="Frontend/images/pharmacie_bloc.png" main.py

pyinstaller --onefile --windowed --name "Pharma" --add-data "Frontend/images:Frontend/images" --add-data "Frontend/style:Frontend/style" --icon="Frontend/images/pharmacie_bloc.png" --hidden-import="reportlab.graphics.barcode.common" --hidden-import="reportlab.graphics.barcode.code128" --hidden-import="reportlab.graphics.barcode.code93" --hidden-import="reportlab.graphics.barcode.code39" --hidden-import="reportlab.graphics.barcode.usps" --hidden-import="reportlab.graphics.barcode.usps4s" --hidden-import="reportlab.graphics.barcode.ecc200datamatrix" main.py


