import sys
from PyQt5.QtWidgets import QApplication, QCheckBox,QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton,QMessageBox
from PyQt5.QtGui import QFont
import string
from PyQt5.QtCore import QTimer
from message_sender_controller import *

class MultipleMessageSender(QMainWindow):
    def __init__(self, ptype):
        super().__init__()
        self.setWindowTitle("Message Sender")
        self.setGeometry(100, 100, 400, 200)
        self.max_msg_per_sec=900
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.process_type=ptype
        layout = QVBoxLayout()
        self.message_sender_controller=MessageSenderController()
        self.message_count_label = QLabel("Number of messages to send")
        self.message_count_label.setFont(QFont("Arial", 12))
        self.message_count_input = QLineEdit()
        self.message_count_input.setPlaceholderText("Insert the number of messages to send")
        self.message_count_input.setFont(QFont("Arial", 12))
        self.interval_label = QLabel("Time Window (seconds):")
        self.interval_label.setFont(QFont("Arial", 12))
        self.interval_input = QLineEdit()
        self.interval_input.setPlaceholderText("Insert the time window (seconds)")
        self.interval_input.setFont(QFont("Arial", 12))
        self.start_button = QPushButton("Start...")
        self.start_button.setFont(QFont("Arial", 12))
        self.save_checkbox = QCheckBox("Save generated payload files")
        self.save_checkbox.setFont(QFont("Arial", 8))
        self.start_button.clicked.connect(self.start_pressed)
        layout.addWidget(self.message_count_label)
        layout.addWidget(self.message_count_input)
        layout.addWidget(self.interval_label)
        layout.addWidget(self.interval_input)
        layout.addWidget(self.start_button)
        layout.addWidget(self.save_checkbox)
        central_widget.setLayout(layout)


    def start_pressed(self):
        message_num_text = self.message_count_input.text()
        time_window_text = self.interval_input.text()
        print("<start_pressed> Number of messages:", message_num_text, "Time Window (seconds):", time_window_text)
        try:
            message_num = int(message_num_text)
        except ValueError:
            message_num = None
        try:
            time_window_num = int(time_window_text)
        except ValueError:
            time_window_num = None      
        if message_num is None or time_window_num is None or message_num<=0 or time_window_num<=0:
            dialog = QMessageBox()
            dialog.setIcon(QMessageBox.Critical)
            dialog.setWindowTitle("Error")
            dialog.setText("Input not valid: Check number field and time interval field")
            dialog.exec()
        elif (int(message_num/time_window_num) > self.max_msg_per_sec):
            dialog = QMessageBox()
            dialog.setIcon(QMessageBox.Critical)
            dialog.setWindowTitle("Error")
            dialog.setText(f"Max message frequency exceeded.Reduce number of messages or increase time window. Maximum frequency is: {self.max_msg_per_sec} msg/sec")
            dialog.exec()
        else:
            print("asinc")
            Params=TestParameter(message_num,time_window_num,self.save_checkbox.isChecked(),self.process_type)
            self.message_sender_controller.set_test_parameter(Params)
            self.message_sender_controller.run_async()


def main():
    app = QApplication(sys.argv)  # Inizializza l'applicazione PyQt5
    window = MultipleMessageSender(1)  # Sostituisci con il tuo tipo di processo
    window.show()  # Mostra la finestra principale
    sys.exit(app.exec_())  # Avvia l'applicazione e gestisci l'uscita

if __name__ == "__main__":
    main()  # Esegui la funzione main al lancio del programma