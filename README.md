# TrackPharmic


pyinstaller main.py

https://dmp.sante.gov.ma/recherche-medicaments




 pharmacieapplication@gmail.com
 Pharmaciehajra



# Steps to create app in mac 

pyinstaller --onefile --windowed --name "Pharma" --add-data  "Frontend/images:Frontend/images" --add-data  "Frontend/style:Frontend/style"  --icon="Frontend/images/pharmacie_bloc.png" main.py



pyinstaller --onefile --windowed --name "Pharma"   --add-data "Frontend/images:Frontend/images"   --add-data "Frontend/style:Frontend/style"   --icon="Frontend/images/pharmacie_bloc.png" main.py

pyinstaller --onefile --windowed --name "Pharma" \
--add-data "Frontend/images:Frontend/images" \
--add-data "Frontend/style:Frontend/style" \
--icon="Frontend/images/pharmacie_bloc.png" \
--hidden-import=[ 'reportlab.graphics.barcode.common',
'reportlab.graphics.barcode.code128',
'reportlab.graphics.barcode.code93',
'reportlab.graphics.barcode.code39',
'reportlab.graphics.barcode.code93',
'reportlab.graphics.barcode.usps',
'reportlab.graphics.barcode.usps4s',
'reportlab.graphics.barcode.ecc200datamatrix'] main.py

