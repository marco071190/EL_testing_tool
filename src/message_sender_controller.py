import json
import os
from PyQt5.QtWidgets import QMessageBox
from gr_creation import *
from xml_creation import *
from file_dispatcher import * 
import time
import csv
import shutil
class TestParameter:
    def __init__(self,num,time,flag, ptype):
        self.number_of_msg = num
        self.time_window = time
        self.save_file = flag
        self.process_type= ptype

class MessageSenderController:
    def __init__(self):
        self.product_id = None
        self.quantity = None
        self.http_addr = None
        self.response_time_list=[]
        self.file_format=None
    def set_data(self, product_id, quantity, http_addr):
            self.product_id = product_id
            self.quantity = quantity
            self.http_addr = http_addr

    def set_test_parameter(self,TestParameter):
        self.test_parameter=TestParameter
        print("<set_test_parameter> number of messages:",self.test_parameter.number_of_msg,"Time Window [sec]",self.test_parameter.time_window)

    def save_report(self):
        current_datetime = datetime.datetime.now()
        unique_filename = current_datetime.strftime("file_%Y%m%d_%H%M%S%f.csv")
        if self.test_parameter.process_type==1:
            folder_name = "reports/gr"
            os.makedirs(folder_name, exist_ok=True)  # Create the folder if it doesn't exist
            csv_filename = os.path.join(folder_name, unique_filename)
        elif self.test_parameter.process_type==2:
            folder_name = "reports/pl"
            os.makedirs(folder_name, exist_ok=True)  # Create the folder if it doesn't exist
            csv_filename = os.path.join(folder_name, unique_filename)
        with open(csv_filename, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Message Number', 'Response Time (seconds)'])  # Write the header row

            for i, response_time in enumerate(self.response_time_list, start=1):
                csv_writer.writerow([i, response_time])

    def create_file_list(self,folder_path):
        if self.test_parameter.process_type==1:
            GR = GR_InputDataManager()
            GR.setLists()
            for _ in range(self.test_parameter.number_of_msg):
                time.sleep(0.002)
                if GR.format_file_number == 1:
                    self.file_format=1
                    file_name = GR.generate_goods_receival_xml(folder_path)
                elif GR.format_file_number == 2:
                    self.file_format=2
                    file_name = GR.generate_goods_receival_json(folder_path)

        elif self.test_parameter.process_type==2:
            PL = PL_InputDataManager()
            PL.setLists()
            for _ in range(self.test_parameter.number_of_msg):
                time.sleep(0.002)
                if PL.format_file_number == 1:
                    self.file_format=1
                    file_name = PL.generate_picklist_xml(folder_path)
                elif PL.format_file_number == 2:
                    self.file_format=2
                    file_name = PL.generate_picklist_json(folder_path)

    def create_report_folders(self):
            report_folder = "report" 
            pl_subfolder_name = "pl"
            subfolder_path = os.path.join(report_folder, pl_subfolder_name)
            if not os.path.exists(subfolder_path):
                os.makedirs(subfolder_path)
            subfolder_path=[]
            gr_subfolder_name = "gr"
            subfolder_path = os.path.join(report_folder, gr_subfolder_name)
            if not os.path.exists(subfolder_path):
                os.makedirs(subfolder_path)
            


    def run_async(self):
        self.create_report_folders()
        folder_path = "temp" 
        report_folder="report"
        self.create_file_list(folder_path)
        file_sender_ASYNC = HttpFileSender(self.file_format,self.test_parameter.save_file)
        if self.test_parameter.process_type is 1:
            address=file_sender_ASYNC.get_http_address_from_config_file(1)
        elif self.test_parameter.process_type is 2:
            address=file_sender_ASYNC.get_http_address_from_config_file(2)

        file_sender_ASYNC.set_http_address(address)
        res_times = file_sender_ASYNC.send_file_asynconous(folder_path,self.test_parameter.number_of_msg,self.test_parameter.time_window)
        timestamp = "async_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".csv" 
        if self.test_parameter.process_type == 1:
            subfolder_path = os.path.join(report_folder, "gr")
            csv_filename = os.path.join(subfolder_path,timestamp)
        elif self.test_parameter.process_type == 2:
            subfolder_path = os.path.join(report_folder, "pl")
            csv_filename = os.path.join(subfolder_path,timestamp)


        with open(csv_filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Test Parameters:", f"File Path: {csv_filename}", f"Number of Messages: {self.test_parameter.number_of_msg}", f"Time Window: {self.test_parameter.time_window}"])
            writer.writerow(["\nThread Number", "Response Time (seconds)"])
            for thread_number, response_time in enumerate(res_times, start=1):
                writer.writerow([thread_number, response_time])
        print("Test completed!")