from qtpy.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget
from qtpy.QtCore import Qt

class BarcodeReaderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Barcode Reader")
        self.resize(400, 200)

        # Widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout principal
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Zone de texte pour afficher les codes-barres
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)  # Rendre la zone en lecture seule
        self.layout.addWidget(self.text_edit)

        # Variable pour stocker le code en cours de saisie
        self.current_input = ""

    def keyPressEvent(self, event):
        """Gérer les entrées clavier, comme les données du lecteur de code-barres."""
        key = event.text()  

        if key == '\r':  # Lorsque le lecteur envoie un saut de ligne
            self.text_edit.append(self.current_input)  # Afficher le code scanné
            self.current_input = ""  # Réinitialiser pour le prochain scan
            print(self.text_edit)
        else:
            self.current_input += key  # Ajouter le caractère au code en cours
            if len(self.current_input)  == 10:
                print(self.current_input)

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = BarcodeReaderApp()
    window.show()
    sys.exit(app.exec_())
