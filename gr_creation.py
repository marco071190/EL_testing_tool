import xml.etree.ElementTree as ET
import json
import random
import datetime
import string
from file_dispatcher import HttpFileSender

class GR_XMLInputDataManager:
    def __init__(self):
        self.in_data = None
        self.load_data()
        self.get_number_of_fields()
        self.get_options()

    def load_data(self):
        with open("gr_data.json") as in_file:
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

    def set_expiry_date_list(self):
        self.expiry_date_list = self.data["ExpiryDate"]
        print("ExpiryDate list:", self.expiry_date_list)
    def set_expiry_date_list(self):
        self.expiry_date_list = self.data["ExpiryDate"]
        print("ExpiryDate list:", self.expiry_date_list)

    def get_options(self):
        if "HTTP" == self.data["Transmission Options"]:
            self.protocolNumber = 1  # Protocol number for http
        elif "FileShare" == self.data["Transmission Options"]:
            self.protocolNumber = 2  # Protocol number for FileShare
        if "XML" == self.data["Data Format"]:
            self.format_file_number = 1  # Format file number for XML
        elif "JSON" == self.data["Data Format"]:
            self.format_file_number = 2  # Format file number for JSON
    def setLists(self):
        self.set_product_id_list()
        self.set_quantity_list()
    
    def generate_random_number(self):
        current_date_time=datetime.datetime.now()
        seed_value = int(current_date_time.timestamp())
        random.seed(seed_value)
        random_number = random.randint(1, 10000000)
        return random_number

    def generate_random_string(self,length):
    # Define the characters you want in your random string
        characters = string.ascii_uppercase + string.digits + string.hexdigits
    # Generate the random string of the specified length
        random_string = ''.join(random.choice(characters) for _ in range(length))
        return random_string

    def generate_goods_receival_xml(self):
        
        random_ext_receival_list_id = self.generate_random_string(10)
        n_transaction_id = self.generate_random_number()

        # Crea un oggetto ElementTree con la radice "ImportOperation"
        import_operation = ET.Element("ImportOperation")

        # Crea l'elemento "Lines"
        lines = ET.SubElement(import_operation, "Lines")
        for i in range(self.num_of_fields):
            # Crea l'elemento "PicklistLine"
            goods_receival_line = ET.SubElement(lines, "GoodsReceivalLine")

            # Aggiungi gli elementi figli a "PicklistLine" con i loro valori
            transaction_id = ET.SubElement(goods_receival_line, "TransactionId")
            transaction_id.text = str(n_transaction_id)

            ext_receival_list_id = ET.SubElement(goods_receival_line,"ExtReceivalListId")
            ext_receival_list_id.text = random_ext_receival_list_id

            ext_product_id = ET.SubElement(goods_receival_line, "ExtProductId")
            ext_product_id.text = self.product_id_list[i]
            
            quantity = ET.SubElement(goods_receival_line,"Quantity")
            quantity.text = self.quantity_list[i]
        
        tree = ET.ElementTree(import_operation)

        # Crea la dichiarazione XML come intestazione del documento
        declaration = '<?xml version="1.0" encoding="UTF-8" ?>'
        filename='PL'+ str()
        # Scrivi l'ElementTree su un file XML con l'intestazione XML
        current_date_time = datetime.datetime.now()
        output_file = current_date_time.strftime("GR-%Y%m%d_%H_%M_%S.xml")
        with open(output_file, "wb") as file:
            file.write(declaration.encode("utf-8"))
            tree.write(file, encoding="utf-8")

        print("<generate_good_receival_xml> File XML creato con successo: ", output_file)
        return output_file
        
if __name__ == "__main__":
    
    in_data = XMLInputDataManager()
    in_data.setLists()
    output_file=in_data.generate_xml()
    HTTP=HttpFileSender()
    address=HTTP.get_http_address_from_config_file()
    HTTP.set_http_address(address)
    HTTP.send_file(output_file)
