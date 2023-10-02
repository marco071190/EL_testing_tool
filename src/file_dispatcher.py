import requests
import json
import shutil
import os
import time
import threading

class HttpFileSender:
        def __init__(self,content_type,save_file=True):
            self.http_send_address=""
            self.user='adm'
            self.pwd='2040'
            self.timeout_seconds=10
            self.save_process_file=save_file
            self.response_times=[]
            self.content_type=content_type
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
                if self.content_type==1:
                    headers = {'Content-Type': 'application/xml'}
                elif self.content_type==2:
                    headers = {'Content-Type': 'application/json'}
                  # Send the POST request with the file
                start_time = time.time()  # Record the start time
                response = requests.post(self.http_send_address,data=open(filename,'rb').read(),auth=auth, headers=headers, timeout=self.timeout_seconds)
                response_time = time.time() - start_time
                # Check the response
                if response.status_code == 202:
                    print("Code 202:File sent successfully.",f"Response time:{response_time}")
                    if self.save_process_file==False:
                        os.remove(filename)
                    self.response_times.append(response_time) #use this only for asinconous
                    return response_time
                else:
                    print(f"File upload failed with status code: {response.status_code}")
                    error_str="Error Number: " + str(response.status_code)
                    self.response_times.append(error_str) #use this only for asinconous
                    if self.save_process_file==False:
                        os.remove(filename)
                    # Continue with sending the file using the 'requests' library
                    # For example:
                    # response = requests.post(self.http_send_address, files=files)
                    # Check the response and handle it as needed
            except Exception as e:
                print(f"An error occurred while sending the file: {e}")
                self.response_times.append(e) #use this only for asinconous
                if self.save_process_file==False:
                    os.remove(filename)

        def send_file_asynconous(self,folder_path,num_messages,time_window):
            print("<send_file_asynconous>")
            filenames = [os.path.join(folder_path, filename) for filename in os.listdir(folder_path) if filename.endswith('.xml') or filename.endswith('.json')]
            if not filenames:
                print("Nessun file trovato nella cartella.")
                return 0
            interval = time_window / num_messages
            threads = []
            # Crea un thread separato per ciascun file da inviare
            count=0
            for filename in filenames[:num_messages]:
                count=count+1
                thread = threading.Thread(target=self.send_file, args=(filename,))
                thread.start()
                threads.append(thread)
                print("Message number:",count)
                time.sleep(interval)  # Attendi per l'intervallo specificato
            
            for thread in threads:
                    thread.join()
            
            return self.response_times


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
