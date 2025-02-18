from Frontend.Interfaces.main_interface import MainInterface
from qtpy.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication([])
    window = MainInterface()
    window.show()
    app.exec_()
