import xml.etree.ElementTree as ET
import json
import random
import datetime
import string
from file_dispatcher import HttpFileSender
import os

class PL_InputDataManager:
    def __init__(self):
        self.in_data = None
        self.load_data()
        self.get_number_of_fields()
        self.get_options()

    def load_data(self):
        with open("pl_data.json") as in_file:
            self.in_data = json.load(in_file)
            self.data = self.in_data[0]["Data"]
            print(self.data)

    def get_number_of_fields(self):
        self.num_of_fields = self.in_data[0].get("FieldSets")
        print("<get_number_of_fields> n.Fields:", self.num_of_fields)

    def set_product_id_list(self):
        self.product_id_list = self.data["Product Id"]
        print("Product id list:", self.product_id_list)

    def set_quantity_list(self):
        self.quantity_list = self.data["Quantity"]
        print("Quantity list:", self.quantity_list)

    def set_sequence_list(self):
        self.sequence_list = self.data["Sequence"]
        print("Sequence list:", self.sequence_list)

    def set_order_type_list(self):
        self.order_type_list = self.data["Order Type"]
        print("Order Type list:", self.order_type_list)

    def get_options(self):
        self.isOrderTypeEnabled = self.data["Enable Order Type"]
        self.isSequenceEnabled = self.data["Enable Sequence"]
        if "HTTP" == self.data["Transmission Options"]:
            self.protocolNumber = 1  # Protocol number for http
        elif "FileShare" == self.data["Transmission Options"]:
            self.protocolNumber = 2  # Protocol number for FileShare
        if "XML" == self.data["File Format"]:
            self.format_file_number = 1  # Format file number for XML
        elif "JSON" == self.data["File Format"]:
            self.format_file_number = 2  # Format file number for JSON
    def setLists(self):
        self.set_product_id_list()
        self.set_quantity_list()
        self.set_sequence_list()
        self.set_order_type_list()
    
    def generate_random_number(self):
        current_date_time = datetime.datetime.now()
        seed_value = int(current_date_time.timestamp())
        random.seed(seed_value)
        random_number = random.randint(1, 10000000)
        microsecondi = int(current_date_time.strftime("%f"))
        random_number += microsecondi 
        return random_number

    def generate_random_string(self, length):
        # Define the characters you want in your random string
        characters = string.ascii_uppercase + string.digits + string.hexdigits
        # Generate the random string of the specified length
        random_string = ''.join(random.choice(characters) for _ in range(length))

        # Aggiungi i microsecondi alla stringa casuale
        microsecondi = datetime.datetime.now().strftime("%f")
        microsecondi = ''.join(filter(str.isdigit, microsecondi))  # Rimuovi caratteri non numerici
        random_string += microsecondi

        return random_string

    def generate_picklist_xml(self,pathname=None):
        picklist_id = self.generate_random_string(10)
        n_transaction_id = self.generate_random_number()

        # Crea un oggetto ElementTree con la radice "ImportOperation"
        import_operation = ET.Element("ImportOperation")

        # Crea l'elemento "Lines"
        lines = ET.SubElement(import_operation, "Lines")
        for i in range(self.num_of_fields):
            # Crea l'elemento "PicklistLine"
            picklist_line = ET.SubElement(lines, "PicklistLine")

            # Aggiungi gli elementi figli a "PicklistLine" con i loro valori
            transaction_id = ET.SubElement(picklist_line, "TransactionId")
            transaction_id.text = str(n_transaction_id)

            ext_picklist_id = ET.SubElement(picklist_line,"ExtPicklistId")
            ext_picklist_id.text = picklist_id

            ext_product_id = ET.SubElement(picklist_line, "ExtProductId")
            ext_product_id.text = self.product_id_list[i]
            
            quantity = ET.SubElement(picklist_line,"Quantity")
            quantity.text = self.quantity_list[i]
            ext_order_line_id = ET.SubElement(picklist_line,"ExtOrderlineId")
            ext_order_line_id.text=str(i+1)#str(i)
            # Aggiungi altri elementi come Quantity, Sequence, ecc. allo stesso modo
            # Esegui un controllo simile per le altre liste
            if self.isOrderTypeEnabled:
                order_type_id = ET.SubElement(picklist_line,"OrderTypeId")
                order_type_id.text= self.order_type_list[i]
            if self.isSequenceEnabled:
                sequence_id = ET.SubElement(picklist_line,"Sequence")
                sequence_id.text = self.sequence_list[i]
        # Crea un oggetto ElementTree con la radice "import_operation"
        
        tree = ET.ElementTree(import_operation)

        # Crea la dichiarazione XML come intestazione del documento
        declaration = '<?xml version="1.0" encoding="UTF-8" ?>'
        filename='PL'+ str()
        # Scrivi l'ElementTree su un file XML con l'intestazione XML
        current_date_time = datetime.datetime.now()
        output_file = current_date_time.strftime("PL-%Y%m%d_%H_%M_%S.xml")
        if pathname:
            if not os.path.exists(pathname):
                os.makedirs(pathname)
            microsecondi = datetime.datetime.now().strftime("%f")
            microsecondi = ''.join(filter(str.isdigit, microsecondi))  # Rimuovi caratteri non numerici
            output_file = f"PL-{microsecondi}.xml"
            output_file = os.path.join(pathname, output_file)
        else:
            output_file = datetime.datetime.now().strftime("PL-%Y%m%d_%H_%M_%S.xml")

        with open(output_file, "wb") as file:
            file.write(declaration.encode("utf-8"))
            tree.write(file, encoding="utf-8")

        print("<generate_picklist_xml> XML file  created successfully: ", output_file)
        return output_file

    def generate_picklist_json(self, pathname=None):
        picklist_id = self.generate_random_string(10)
        n_transaction_id = self.generate_random_number()

        picklist_data = {
            "ImportOperation": {
                "Lines": {
                    "PicklistLine": []
                }
            }
        }

        for i in range(self.num_of_fields):
            picklist_line = {
                "TransactionId": n_transaction_id,
                "ExtPicklistId": picklist_id,
                "ExtProductId": self.product_id_list[i],
                "Quantity": self.quantity_list[i],
                "ExtOrderlineId": str(i + 1)
            }

            if self.isOrderTypeEnabled:
                picklist_line["OrderTypeId"] = self.order_type_list[i]

            if self.isSequenceEnabled:
                picklist_line["Sequence"] = self.sequence_list[i]

            picklist_data["ImportOperation"]["Lines"]["PicklistLine"].append(picklist_line)

        current_date_time = datetime.datetime.now()
        output_file = current_date_time.strftime("PL-%Y%m%d_%H_%M_%S.json")

        if pathname:
            if not os.path.exists(pathname):
                os.makedirs(pathname)

            microsecondi = datetime.datetime.now().strftime("%f")
            microsecondi = ''.join(filter(str.isdigit, microsecondi))
            output_file = f"PL-{microsecondi}.json"
            output_file = os.path.join(pathname, output_file)
        else:
            output_file = datetime.datetime.now().strftime("PL-%Y%m%d_%H_%M_%S.json")

        with open(output_file, "w") as file:
            json.dump(picklist_data, file, indent=4)

        print("<generate_picklist_json> JSON file created successfully:", output_file)
        return output_file

if __name__ == "__main__":
    
    in_data = PL_InputDataManager()
    in_data.setLists()
    output_file=in_data.generate_xml()
    HTTP=HttpFileSender()
    address=HTTP.get_http_address_from_config_file()
    HTTP.set_http_address(address)
    HTTP.send_file(output_file)
