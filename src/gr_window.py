import sys
import json
import os
from PyQt5.QtWidgets import QApplication, QDialog, QLineEdit, QPushButton, QVBoxLayout, QRadioButton, QWidget, QFormLayout, QFrame, QHBoxLayout, QCheckBox
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QGridLayout, QLabel, QButtonGroup, QScrollArea,QMenu
from PyQt5.QtGui import QFont
from xml_creation import *
from file_dispatcher import *
from gr_creation import *
from message_sender_window import * 
from message_sender_controller import * 
class GRWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Good Receival Message configuration")
        self.setMinimumSize(1000, 800)
        self.communication_protocol = ""
        self.message_sender_controller=MessageSenderController()
        self.message_sender_window=MultipleMessageSender(1)
        # Create a widget for the internal content of the window
        content_widget = QWidget()

        # Main layout with spacing between horizontal layouts
        layout = QVBoxLayout(self)

        # Create Scroll Area
        self.scroll_layout = QVBoxLayout()
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_widget.setLayout(self.scroll_layout)
        scroll_area.setWidget(scroll_widget)

        # Layout for scrollable fields

        # Initialize a list to store data
        self.data_list = []

        # Add initial fields
        self.field_sets = []
        self.add_field_set(self.scroll_layout)

        # Button to add a new set of fields
        add_button = QPushButton("Add Field Set")
        add_button.setDefault(False)
        add_button.setFocusPolicy(Qt.NoFocus)
        add_button.setAutoDefault(False)
        add_button.setFont(QFont("Arial", 12))
        add_button.clicked.connect(lambda: self.add_field_set(self.scroll_layout))

        # Button to confirm (Generate Good Receival label) and close the window
        confirm_button = QPushButton("Generate Good Receival")
        confirm_button.setStyleSheet("background-color: #4CAF50; color: white;")
        confirm_button.setDefault(False)
        confirm_button.setFocusPolicy(Qt.NoFocus)
        confirm_button.setFont(QFont("Arial", 12))
        confirm_button.setAutoDefault(False)
        confirm_button.clicked.connect(self.generateGoodsReceival)

        cancel_button = QPushButton("Clear Fields")
        cancel_button.setDefault(False)
        cancel_button.setFocusPolicy(Qt.NoFocus)
        cancel_button.setAutoDefault(False)
        cancel_button.clicked.connect(self.clear_fields)
        cancel_button.setFont(QFont("Arial", 12))

        save_button = QPushButton("Save Data")
        save_button.setDefault(False)
        save_button.setFocusPolicy(Qt.NoFocus)
        save_button.setAutoDefault(False)
        save_button.setFont(QFont("Arial", 12))
        save_button.clicked.connect(self.save_fields_on_file)

        # Checkboxes to enable/disable fields
        self.enable_expiring_date_checkbox = QCheckBox("Enable Expiring Date Field")
        self.enable_expiring_date_checkbox.setFont(QFont("Arial", 12))
        self.enable_expiring_date_checkbox.stateChanged.connect(self.toggle_expiring_date_field)

        # "More button":
        self.more_button=QPushButton("More....",self)
        self.more_button.setMaximumSize(80, 120)
        self.more_button.setFont(QFont("Arial", 12))
        self.more_button.clicked.connect(self.toggle_more_btn)

        # Radio buttons to choose between JSON and XML
        self.format_file_label = QLabel("File Type:")
        self.format_file_label.setFont(QFont("Arial", 12))
        self.json_radio = QRadioButton("JSON")
        self.json_radio.setFont(QFont("Arial", 12))
        self.xml_radio = QRadioButton("XML")
        self.xml_radio.setFont(QFont("Arial", 12))

        # Add a line edit field for URL or path
        self.fileshare_path_label = QLabel("FileShare Path")
        self.fileshare_path_label.setFont(QFont("Arial", 12))
        self.fileshare_path_input = QLineEdit()
        self.fileshare_path_input.setFont(QFont("Arial", 12))
        self.fileshare_path_input.setPlaceholderText('Enter Fileshare path')

        fileshare_path_layout = QHBoxLayout()
        fileshare_path_layout.addWidget(self.fileshare_path_label)
        fileshare_path_layout.addWidget(self.fileshare_path_input)

        self.http_address_label = QLabel("Http Address")
        self.http_address_label.setFont(QFont("Arial", 12))
        self.http_address_input = QLineEdit()
        self.http_address_input.setFont(QFont("Arial", 12))
        self.http_address_input.setPlaceholderText('Enter http address request')
        self.http_address_input.textChanged.connect

        http_request_layout = QHBoxLayout()
        http_request_layout.addWidget(self.http_address_label)
        http_request_layout.addWidget(self.http_address_input)

        # Create a button group for JSON and XML radio buttons
        self.format_button_group = QButtonGroup()
        self.format_button_group.addButton(self.json_radio)
        self.format_button_group.addButton(self.xml_radio)

        # Radio buttons for transmission options
        self.transmission_label = QLabel("Transmission Options:")
        self.transmission_label.setFont(QFont("Arial", 12))
        self.transmission_label.setAlignment(Qt.AlignCenter)
        self.http_radio = QRadioButton("HTTP")
        self.http_radio.setFont(QFont("Arial", 12))
        self.http_radio.clicked.connect(lambda: self.toggle_trasmission_options(1))
        self.file_share_radio = QRadioButton("File Share")
        self.file_share_radio.setFont(QFont("Arial", 12))
        self.file_share_radio.clicked.connect(lambda: self.toggle_trasmission_options(2))

        # Create a button group for transmission options radio buttons
        self.transmission_button_group = QButtonGroup()
        self.transmission_button_group.addButton(self.http_radio)
        self.transmission_button_group.addButton(self.file_share_radio)

        # Create a layout for the "Enable Expiring Date" checkbox
        expiring_date_checkbox_layout = QHBoxLayout()
        expiring_date_checkbox_layout.addWidget(self.enable_expiring_date_checkbox)
        expiring_date_checkbox_layout.addStretch(1)

        # Add buttons and radio buttons to the main layout
        layout.addLayout(self.scroll_layout)
        layout.addWidget(add_button)
        layout.addWidget(scroll_area)
        button_layout = QHBoxLayout()
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(confirm_button)
        button_layout.addWidget(save_button)


        format_layout = QVBoxLayout()
        format_layout.addWidget(self.format_file_label)
        format_layout.addWidget(self.json_radio)
        format_layout.addWidget(self.xml_radio)
        # Create vertical layout for more button
        v_more_btn_layout=QVBoxLayout()
        v_more_btn_layout.addWidget(self.more_button)
        
        # Arrange everything in a grid layout
        grid_layout = QGridLayout()
        grid_layout.addLayout(format_layout, 0, 0)
        grid_layout.addWidget(self.transmission_label, 1, 1)
        grid_layout.addWidget(self.http_radio, 1, 2)
        grid_layout.addWidget(self.file_share_radio, 2, 2)
        grid_layout.addLayout(expiring_date_checkbox_layout, 1, 0)
        grid_layout.addLayout(button_layout, 4, 0, 1, 2)
        grid_layout.addLayout(fileshare_path_layout, 5, 0, 1, 3)
        grid_layout.addLayout(http_request_layout, 6, 0, 1, 3)
        grid_layout.addLayout(v_more_btn_layout, 7, 0)
        layout.addLayout(grid_layout)

        content_widget.setLayout(layout)
        self.setLayout(layout)

        # Load data if available and populate the fields
        self.load_data()

    def add_field_set(self, scroll_layout):
        field_set_layout = QFormLayout()

        # Create input QLineEdit fields with custom font size
        product_id_input = QLineEdit()
        product_id_input.setFont(QFont("Arial", 12))
        quantity_input = QLineEdit()
        quantity_input.setFont(QFont("Arial", 12))
        expiring_date_input = QLineEdit()
        expiring_date_input.setFont(QFont("Arial", 12))
        external_order_id_input = QLineEdit()
        external_order_id_input.setFont(QFont("Arial", 12))
        external_order_line_id_input = QLineEdit()
        external_order_line_id_input.setFont(QFont("Arial", 12))
        # Create QLabel labels with custom font sizes
        product_id_label = QLabel("Product Id")
        product_id_label.setFont(QFont("Arial", 12))
        quantity_label = QLabel("Quantity")
        quantity_label.setFont(QFont("Arial", 12))
        expiring_date_label = QLabel("Expiring Date")
        expiring_date_label.setFont(QFont("Arial", 12))

        field_set_layout.addRow(product_id_label, product_id_input)
        field_set_layout.addRow(quantity_label, quantity_input)
        field_set_layout.addRow(expiring_date_label, expiring_date_input)

        field_set_widget = QWidget()
        field_set_widget.setLayout(field_set_layout)

        # Add a horizontal line
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)

        field_set_layout.addWidget(line)
        scroll_layout.addWidget(field_set_widget)

        self.field_sets.append([field_set_widget, product_id_input, quantity_input, expiring_date_input])
        self.adjustSize()

    def save_fields_on_file(self):
        # Retrieve data from fields and save it to the data list
        data = {
            "Product Id": [],
            "Quantity": [],
            "Expiring Date": [],
            "Enable Expiring Date": self.enable_expiring_date_checkbox.isChecked(),
            "Transmission Options": "HTTP" if self.http_radio.isChecked() else "Fileshare",
            "Data Format": "JSON" if self.json_radio.isChecked() else "XML",
            "Http Addr": self.http_address_input.text(),
            "Fileshare Path": self.fileshare_path_input.text(),
        }

        for field_set in self.field_sets:
            _, product_id, quantity, expiring_date = field_set
            data["Product Id"].append(product_id.text())
            data["Quantity"].append(quantity.text())
            data["Expiring Date"].append(expiring_date.text())

        # Save the data including the number of field sets created
        self.data_list = [{"Data": data, "FieldSets": len(self.field_sets)}]

        # Save the data to a JSON file, overwriting the existing data
        with open("gr_data.json", "w") as file:
            json.dump(self.data_list, file)
            print("GR Data saved:", self.data_list)

    def load_data(self):
        try:
            with open("gr_data.json", "r") as file:
                self.data_list = json.load(file)
                print("Data loaded:", self.data_list)
                if self.data_list:
                    # Populate the fields with the loaded data
                    data = self.data_list[0]["Data"]
                    num_field_sets = self.data_list[0].get("FieldSets", 1)
                    self.file_format = data.get("Data Format")

                    if data.get("Data Format") == 'XML':
                        self.xml_radio.setChecked(True)
                        self.json_radio.setChecked(False)
                    elif data.get("Data Format") == 'JSON':
                        self.xml_radio.setChecked(False)
                        self.json_radio.setChecked(True)
                    self.commFormat = data.get("Transmission Options")
                    if self.commFormat == "HTTP":
                        self.http_radio.setChecked(True)
                        self.http_address_input.setEnabled(True)
                        self.file_share_radio.setChecked(False)
                        self.fileshare_path_input.setEnabled(False)
                        self.communication_protocol = 1
                    elif self.commFormat == "Fileshare":
                        self.file_share_radio.setChecked(True)
                        self.fileshare_path_input.setEnabled(True)
                        self.http_radio.setChecked(False)
                        self.http_address_input.setEnabled(False)
                        self.communication_protocol = 2
                    http_addr = data.get("Http Addr")
                    self.http_address_input.setText(http_addr)
                    fileshare_addr = data.get("Fileshare Path")
                    self.fileshare_path_input.setText(fileshare_addr)
                    is_expiring_date_checked = data.get("Enable Expiring Date", False)
                    self.enable_expiring_date_checkbox.setChecked(is_expiring_date_checked)


                    for _ in range(num_field_sets - 1):
                        self.add_field_set(self.scroll_layout)
                    for i, field_set in enumerate(self.field_sets):
                        _, product_id, quantity, expiring_date = field_set
                        product_id.setText(data["Product Id"][i])
                        quantity.setText(data["Quantity"][i])
                        expiring_date.setText(data["Expiring Date"][i])
                        if is_expiring_date_checked:
                            expiring_date.setEnabled(True)
                            expiring_date.setText(data["Expiring Date"][i])
                        else:
                            expiring_date.setEnabled(False)
        except FileNotFoundError:
            print("No existing data file found. Starting with an empty list.")
            return -1

    def generateGoodsReceival(self):
        self.save_fields_on_file()
        xml = GR_XMLInputDataManager()
        xml.setLists()
        file_name = xml.generate_goods_receival_xml()
        if self.communication_protocol == 1:
            HTTP = HttpFileSender()
            address = HTTP.get_http_address_from_config_file(1) #identifies GoodsReceival
            HTTP.set_http_address(address)
            HTTP.send_file(file_name)
        elif self.communication_protocol == 2:
            fshare = FileShareSender()
            path = fshare.get_fileshare_path_from_config_file(1) #identifies GoodsReceival
            fshare.set_fileshare_path(path)
            fshare.copy_file_in_path(file_name)

    def toggle_expiring_date_field(self, state):
        self.expiring_date_enabled = state == Qt.Checked
        for field_set in self.field_sets:
            _, _,_,expiring_date_input = field_set
            expiring_date_input.setEnabled(self.expiring_date_enabled)

    def toggle_trasmission_options(self, method):
        self.communication_protocol = method
        if self.communication_protocol == 1:
            self.http_address_input.setEnabled(True)
            self.http_radio.setChecked(True)
            self.file_share_radio.setChecked(False)
            self.fileshare_path_input.setEnabled(False)
            print("Http option")
        elif self.communication_protocol == 2:
            self.fileshare_path_input.setEnabled(True)
            self.file_share_radio.setChecked(True)
            self.http_address_input.setEnabled(False)
            self.http_radio.setChecked(False)
            print("Fileshare option")
    
    def show_error_message(self):
        error_box = QMessageBox()
        error_box.setIcon(QMessageBox.Critical)
        error_box.setWindowTitle("Error:data field not valid")
        error_box.exec()
    
    def check_fields_before_send(self,prod_id,quantity,http):
        if not prod_id or not quantity or not http:
                return -1  # Almeno uno dei campi è vuoto
        elif not quantity.isdigit():
                return -2  # Quantity non è un numero intero
        else:
                return 0  # Tutti i campi sono stati compilati correttamente

    def azione1(self):
        print("azione 1 ")
        if  self.communication_protocol == 2 :
            error_box = QMessageBox()
            error_box.setIcon(QMessageBox.Critical)
            error_box.setWindowTitle("Error")
            error_box.setText("Error: Please switch to Http")
            error_box.exec()
        elif self.communication_protocol == 1 :
            self.message_sender_window.show()
    

    def toggle_more_btn(self):
        print("toggle_more_btn")
        context_menu = QMenu(self)
        # Aggiungi azioni (voci di menu) al menu contestuale
        action1 = context_menu.addAction("Massive Good Receival Messages Test")
        # Visualizza il menu contestuale al punto in cui è stato cliccato il pulsante "More..."
        action1.triggered.connect(self.azione1)
        pos = self.more_button.mapToGlobal(self.more_button.rect().bottomLeft())
        context_menu.exec_(pos)

    def clear_fields(self):
        confirm_dialog = QMessageBox()
        confirm_dialog.setIcon(QMessageBox.Question)
        confirm_dialog.setText("Are you sure you want to clear the last field set?")
        confirm_dialog.setWindowTitle("Confirmation")
        confirm_dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        response = confirm_dialog.exec()
        if response == QMessageBox.Yes:
            if len(self.field_sets) > 1:
                field_set = self.field_sets.pop()
                for widget in field_set:
                    if isinstance(widget, QWidget):
                        widget.setParent(None)
            else:
                for field_set in self.field_sets:
                    for widget in field_set:
                        if isinstance(widget, QLineEdit):
                            widget.clear()

            if os.path.exists("gr_data.json"):
                os.remove("gr_data.json")

        self.adjustSize()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GRWindow()
    window.show()
    sys.exit(app.exec_())
