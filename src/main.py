import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QLineEdit, QPushButton, QVBoxLayout, QTabWidget, QWidget, QLabel, QMessageBox
from PyQt5.QtCore import pyqtSignal, Qt
from pl_window import *
from gr_window import *
from PyQt5.QtGui import QPixmap, QFont

class ProductQuantity:
    def __init__(self, product_id=None, quantity=None):
        self.product_id = product_id
        self.quantity = quantity

class ProductEntryWidget(QWidget):
    data_saved = pyqtSignal(ProductQuantity)

    def __init__(self, product_name):
        super().__init__()

        # ... (Rest of your ProductEntryWidget code remains the same)

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(600,800)
        self.create_pl_btn=QPushButton()
        self.create_gr_btn=QPushButton()
        self.create_pl_btn.setText("Create PickList")
        self.create_gr_btn.setText("Create Good Receival")
        #self.create_btn_gr.setGeometry(100, 100, 200, 200)
        # Create an instance of the PLWindow but don't show it immediately
        self.pl_window = PLWindow()
        self.gr_window = GRWindow()
        # Connect the action 'actionXML_type' to open the PLWindow
        self.create_pl_btn.clicked.connect(self.show_pl_window)
        self.create_gr_btn.clicked.connect(self.show_gr_window)
        self.saved_values = []

        # Create a central widget and set the main layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.create_gr_btn)
        layout.addWidget(self.create_pl_btn)

        # Aggiungi il logo come QLabel
        logo_label = QLabel(self)
        pixmap = QPixmap("el_logo.jpg")  # Utilizza il nuovo nome del file
        scaled_pixmap = pixmap.scaled(pixmap.width() // 2, pixmap.height() // 2, Qt.KeepAspectRatio)
        logo_label.setPixmap(scaled_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)

        # Crea un layout per posizionare il logo sopra il pulsante
        layout.addWidget(logo_label)

        # Aumenta il font solo per il pulsante "Create Pick List"
        button_font = QFont()
        button_font.setPointSize(16)  # Imposta la dimensione del font desiderata
        self.create_pl_btn.setFont(button_font)
        self.create_gr_btn.setFont(button_font)

    def show_pl_window(self):
        # Show the PLWindow when the button is clicked
        self.pl_window.show()
    def show_gr_window(self):
        # Show the GRWindow when the button is clicked
        self.gr_window.show()

def main():
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
