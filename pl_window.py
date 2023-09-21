import sys
import json
import os
from PyQt5.QtWidgets import QApplication, QDialog, QLineEdit, QPushButton, QVBoxLayout, QRadioButton, QWidget, QFormLayout, QFrame, QHBoxLayout, QCheckBox
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QGridLayout, QLabel, QButtonGroup, QScrollArea
from PyQt5.QtGui import QFont
from xml_creation import *
from file_dispatcher import * 

class PLWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Picklist message configuration")
        #self.setGeometry(100, 100, 600, 400)  # Increased width for transmission options
        self.setMinimumSize(1000,800)
        self.communication_protocol = ""

        # Create a widget for the internal content of the window
        content_widget = QWidget()

        # Main layout with spacing between horizontal layouts
        layout = QVBoxLayout(self)
        # Create Scroll Area
        self.scroll_layout = QVBoxLayout()  # Define scroll_layout as a class attribute
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # Rende il widget all'interno della QScrollArea ridimensionabile
        scroll_widget = QWidget()
        scroll_widget.setLayout(self.scroll_layout)  # Usa self.scroll_layout
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
        add_button.setFocusPolicy(Qt.NoFocus)  # Rimuovi il focus dal pulsante
        add_button.setAutoDefault(False)  # Disabilita il comportamento predefinito alla pressione di Invio
        add_button.setFont(QFont("Arial", 12))  # Imposta la famiglia di caratteri e la dimensione del font desiderata
        add_button.clicked.connect(lambda: self.add_field_set(self.scroll_layout))
        # Button to confirm (Generate PickList label) and close the window
        confirm_button = QPushButton("Generate PickList")
        confirm_button.setStyleSheet("background-color: #4CAF50; color: white;")
        confirm_button.setDefault(False)
        confirm_button.setFocusPolicy(Qt.NoFocus)  # Rimuovi il focus dal pulsante
        confirm_button.setFont(QFont("Arial", 12))  # Imposta la famiglia di caratteri e la dimensione del font desiderata
        confirm_button.setAutoDefault(False)  # Disabilita il comportamento predefinito alla pressione di Invio
        confirm_button.clicked.connect(self.generatePickList)
        cancel_button = QPushButton("Clear Fields")
        cancel_button.setDefault(False)
        cancel_button.setFocusPolicy(Qt.NoFocus)  # Rimuovi il focus dal pulsante
        cancel_button.setAutoDefault(False)  # Disabilita il comportamento predefinito alla pressione di Invio
        cancel_button.clicked.connect(self.clear_fields)
        cancel_button.setFont(QFont("Arial", 12))  # Imposta la famiglia di caratteri e la dimensione del font desiderata
        save_button = QPushButton("Save Data")
        save_button.setDefault(False)
        save_button.setFocusPolicy(Qt.NoFocus)  # Rimuovi il focus dal pulsante
        save_button.setAutoDefault(False)  # Disabilita il comportamento predefinito alla pressione di Invio
        save_button.setFont(QFont("Arial", 12))  # Imposta la famiglia di caratteri e la dimensione del font desiderata
        save_button.clicked.connect(self.save_fields_on_file)

        # Checkboxes to enable/disable fields
        self.enable_order_type_checkbox = QCheckBox("Enable Order Type Field")
        self.enable_order_type_checkbox.setFont(QFont("Arial", 12))
        self.enable_order_type_checkbox.stateChanged.connect(self.toggle_order_type_field)

        self.enable_sequence_checkbox = QCheckBox("Enable Sequence Field")
        self.enable_sequence_checkbox.setFont(QFont("Arial", 12))
        self.enable_sequence_checkbox.stateChanged.connect(self.toggle_sequence_field)

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

        # Create a layout for the "Enable Order Type" checkbox
        order_type_checkbox_layout = QHBoxLayout()
        order_type_checkbox_layout.addWidget(self.enable_order_type_checkbox)
        order_type_checkbox_layout.addStretch(1)  # Add stretch to push checkbox to the right

        # Create a layout for the "Enable Sequence" checkbox
        sequence_checkbox_layout = QHBoxLayout()
        sequence_checkbox_layout.addWidget(self.enable_sequence_checkbox)
        sequence_checkbox_layout.addStretch(1)  # Add stretch to push checkbox to the right

        # Add buttons and radio buttons to the main layout
        layout.addLayout(self.scroll_layout)  # Use self.scroll_layout
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

        # Arrange everything in a grid layout
        grid_layout = QGridLayout()
        grid_layout.addLayout(format_layout, 0, 0)  # JSON and XML radio buttons
        grid_layout.addWidget(self.transmission_label, 1, 1)  # Transmission options label
        grid_layout.addWidget(self.http_radio, 1, 2)  # HTTP radio button
        grid_layout.addWidget(self.file_share_radio, 2, 2)  # File Share radio button
        grid_layout.addLayout(order_type_checkbox_layout, 1, 0)  # Enable Order Type checkbox
        grid_layout.addLayout(sequence_checkbox_layout, 2, 0)  # Enable Sequence checkbox
        grid_layout.addLayout(button_layout, 3, 0, 1, 2)  # Buttons
        grid_layout.addLayout(fileshare_path_layout, 4, 0, 1, 3)
        grid_layout.addLayout(http_request_layout, 5, 0, 1, 3,)
        layout.addLayout(grid_layout)

        content_widget.setLayout(layout)
        self.setLayout(layout)
        # Load data if available and populate the fields
        self.load_data()

    def add_field_set(self, scroll_layout):
        field_set_layout = QFormLayout()

        # Crea campi di input QLineEdit con una dimensione del font personalizzata
        product_id_input = QLineEdit()
        product_id_input.setFont(QFont("Arial", 12))  # Imposta la dimensione del font a 14
        quantity_input = QLineEdit()
        quantity_input.setFont(QFont("Arial", 12))  # Imposta la dimensione del font a 14
        order_type_input = QLineEdit()
        order_type_input.setFont(QFont("Arial", 12))  # Imposta la dimensione del font a 14
        sequence_input = QLineEdit()
        sequence_input.setFont(QFont("Arial", 12))  # Imposta la dimensione del font a 14

        # Crea etichette QLabel con dimensioni del font personalizzate
        product_id_label = QLabel("Product Id")
        product_id_label.setFont(QFont("Arial", 12))  # Imposta la dimensione del font a 14
        quantity_label = QLabel("Quantity")
        quantity_label.setFont(QFont("Arial", 12))  # Imposta la dimensione del font a 14
        order_type_label = QLabel("Order Type")
        order_type_label.setFont(QFont("Arial", 12))  # Imposta la dimensione del font a 14
        sequence_label = QLabel("Sequence")
        sequence_label.setFont(QFont("Arial", 12))  # Imposta la dimensione del font a 14

        field_set_layout.addRow(product_id_label, product_id_input)
        field_set_layout.addRow(quantity_label, quantity_input)
        field_set_layout.addRow(order_type_label, order_type_input)
        field_set_layout.addRow(sequence_label, sequence_input)

        field_set_widget = QWidget()
        field_set_widget.setLayout(field_set_layout)

        # Aggiungi una linea orizzontale
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)

        field_set_layout.addWidget(line)
        scroll_layout.addWidget(field_set_widget)

        self.field_sets.append([field_set_widget, product_id_input, quantity_input, order_type_input, sequence_input])
        self.adjustSize()

    def save_fields_on_file(self):
        # Retrieve data from fields and save it to the data list
        data = {
            "Product Id": [],
            "Quantity": [],
            "Order Type": [],
            "Sequence": [],
            "Enable Order Type": self.enable_order_type_checkbox.isChecked(),
            "Enable Sequence": self.enable_sequence_checkbox.isChecked(),
            "Transmission Options": "HTTP" if self.http_radio.isChecked() else "Fileshare",
            "Data Format": "JSON" if self.json_radio.isChecked() else "XML",
            "Http Addr": self.http_address_input.text(),
            "Fileshare Path": self.fileshare_path_input.text(),
        }

        for field_set in self.field_sets:
            _, product_id, quantity, order_type, sequence = field_set  # Skip the first element, which is the field_set widget
            data["Product Id"].append(product_id.text())
            data["Quantity"].append(quantity.text())
            data["Order Type"].append(order_type.text())
            data["Sequence"].append(sequence.text())

        # Save the data including the number of field sets created
        self.data_list = [{"Data": data, "FieldSets": len(self.field_sets)}]

        # Save the data to a JSON file, overwriting the existing data
        with open("pl_data.json", "w") as file:
            json.dump(self.data_list, file)
            print("Data saved:", self.data_list)

    def load_data(self):
        try:
            with open("pl_data.json", "r") as file:
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
                    is_order_type_checked = data.get("Enable Order Type", False)  # Default to False if the key is missing
                    is_sequence_checked = data.get("Enable Sequence", False)  # Default to False if the key is missing
                    self.enable_order_type_checkbox.setChecked(is_order_type_checked)
                    self.enable_sequence_checkbox.setChecked(is_sequence_checked)

                    for _ in range(num_field_sets - 1):
                        self.add_field_set(self.scroll_layout)
                    for i, field_set in enumerate(self.field_sets):
                        _, product_id, quantity, order_type, sequence = field_set  # Skip the first element, which is the field_set widget
                        product_id.setText(data["Product Id"][i])
                        quantity.setText(data["Quantity"][i])
                        order_type.setText(data["Order Type"][i])
                        sequence.setText(data["Sequence"][i])
                        if is_order_type_checked:
                            order_type.setEnabled(True)
                            order_type.setText(data["Order Type"][i])
                        else:
                            order_type.setEnabled(False)
                        if is_sequence_checked:
                            sequence.setEnabled(True)
                            sequence.setText(data["Sequence"][i])
                        else:
                            sequence.setEnabled(False)
        except FileNotFoundError:
            print("No existing data file found. Starting with an empty list.")

    def generatePickList(self):
        self.save_fields_on_file()
        xml = XMLInputDataManager()
        xml.setLists()
        file_name = xml.generate_picklist_xml()
        if self.communication_protocol == 1:
            HTTP = HttpFileSender()
            address = HTTP.get_http_address_from_config_file(2)     #identifies the picklist 
            HTTP.set_http_address(address)
            HTTP.send_file(file_name)
        elif self.communication_protocol == 2:
            fshare = FileShareSender()
            path = fshare.get_fileshare_path_from_config_file(2)    #identifies the picklist 
            fshare.set_fileshare_path(path)
            fshare.copy_file_in_path(file_name)

    def toggle_order_type_field(self, state):
        # State is either Qt.Checked (2) or Qt.Unchecked (0)
        if state == Qt.Checked:
            self.order_type_enabled = True
        else:
            self.order_type_enabled = False
        # Enable/disable Order Type fields in all field sets
        for field_set in self.field_sets:
            _, _, _, order_type, _ = field_set
            order_type.setEnabled(self.order_type_enabled)
        return self.order_type_enabled

    def toggle_sequence_field(self, state):
        # State is either Qt.Checked (2) or Qt.Unchecked (0)
        if state == Qt.Checked:
            self.sequence_enabled = True
        else:
            self.sequence_enabled = False
        # Enable/disable Sequence fields in all field sets
        for field_set in self.field_sets:
            _, _, _, _, sequence = field_set
            sequence.setEnabled(self.sequence_enabled)

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

    def clear_fields(self):
        confirm_dialog = QMessageBox()
        confirm_dialog.setIcon(QMessageBox.Question)
        confirm_dialog.setText("Are you sure you want to clear the last field set?")
        confirm_dialog.setWindowTitle("Confirmation")
        confirm_dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        # Check the user's response
        response = confirm_dialog.exec()
        if response == QMessageBox.Yes:
            if len(self.field_sets) > 1:
                field_set = self.field_sets.pop()
                for widget in field_set:
                    if isinstance(widget, QWidget):
                        widget.setParent(None)
            else:
                # If there is only one field set, clear its field values instead of removing it
                for field_set in self.field_sets:
                    for widget in field_set:
                        if isinstance(widget, QLineEdit):
                            widget.clear()

            if os.path.exists("pl_data.json"):
                os.remove("pl_data.json")

        self.adjustSize()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PLWindow()
    window.show()
    sys.exit(app.exec_())
