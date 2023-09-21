import requests
import json
import shutil

class HttpFileSender:
        def __init__(self):
            self.http_send_address=""
            self.user='adm'
            self.pwd='2040'
            self.timeout_seconds=10
        def set_http_address(self,http_address):
            self.http_send_address=http_address
        #process: 1 INBOUND (GOODS RECEIVAL) 2: OUTBOUND (PICKLIST)
        def get_http_address_from_config_file(self,process):
            if process==1:
                with open("gr_data.json", "r") as file:
                    self.data_list = json.load(file)
                    http_addr = self.data_list[0]["Data"].get("Http Addr")
                    # Ensure the address includes the protocol (e.g., http://)
                    if not http_addr.startswith("http://"):
                        http_addr = "http://" + http_addr
                    print("get_http_address_from_config_file: ", http_addr)
                return http_addr
            elif process==2:
                with open("pl_data.json", "r") as file:
                    self.data_list = json.load(file)
                    http_addr = self.data_list[0]["Data"].get("Http Addr")
                    # Ensure the address includes the protocol (e.g., http://)
                    if not http_addr.startswith("http://"):
                        http_addr = "http://" + http_addr
                    print("get_http_address_from_config_file: ", http_addr)
                return http_addr
        def send_file(self, filename):
            auth=(self.user,self.pwd)
            if not self.http_send_address:
                raise ValueError("HTTP address is not set.")
            try:
                
                headers = {'Content-Type': 'application/xml'}
                  # Send the POST request with the file
                response = requests.post(self.http_send_address,data=open(filename,'rb').read(),auth=auth, headers=headers, timeout=self.timeout_seconds)
                # Check the response
                if response.status_code == 202:
                    print("Code 202:File sent successfully.")
                else:
                    print(f"File upload failed with status code: {response.status_code}")
                    # Continue with sending the file using the 'requests' library
                    # For example:
                    # response = requests.post(self.http_send_address, files=files)
                    # Check the response and handle it as needed
            except Exception as e:
                print(f"An error occurred while sending the file: {e}")

class FileShareSender:
        def __init__(self):
            self.fileshare_path=""
            self.user='adm'
            self.pwd='2040'
        def set_fileshare_path(self,path):
            self.fileshare_path=path
        #process: 1 INBOUND (GOODS RECEIVAL) 2: OUTBOUND (PICKLIST)
        def get_fileshare_path_from_config_file(self,process):
            if process==1:
                with open("gr_data.json", "r") as file:
                    self.data_list = json.load(file)
                    path = self.data_list[0]["Data"].get("Fileshare Path")
            elif process==2:
                with open("pl_data.json", "r") as file:
                    self.data_list = json.load(file)
                    path = self.data_list[0]["Data"].get("Fileshare Path")

            return path
        def copy_file_in_path(self,filename):
            try:
                shutil.copy2(filename,self.fileshare_path)
                print("File",filename,"copied successfull at path:",self.fileshare_path)      
            # If source and destination are same
            except shutil.SameFileError:
                print("Source and destination represents the same file.")
            
            # If destination is a directory.
            except IsADirectoryError:
                print("Destination is a directory.")
            
            # If there is any permission issue
            except PermissionError:
                print("Permission denied.")
            
            # For other errors
            except:
                print("Error occurred while copying file.")
