import win32print
import win32ui

printer_name = win32print.GetDefaultPrinter()
hprinter = win32print.OpenPrinter(printer_name)
printer_info = win32print.GetPrinter(hprinter, 2)
pdc = win32ui.CreateDC()
pdc.CreatePrinterDC(printer_name)
pdc.StartDoc('Document')
pdc.StartPage()
pdc.TextOut(100, 100, "Ceci est un test d'impression direct")
pdc.EndPage()
pdc.EndDoc()
pdc.DeleteDC()



