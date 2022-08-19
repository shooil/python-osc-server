from time import sleep
from pythonosc import udp_client
import json
import datetime

class osc_base():
    def __init__(self, client:udp_client.SimpleUDPClient,config_path:str):
        self.client:udp_client.SimpleUDPClient = client
        self.addr_dict:dict = self.addr_parser(config_path)
    
    def addr_parser(self,config_path:str):
        with open(config_path,encoding='utf-8-sig') as f:
            params:list = json.load(f)["parameters"]
        address_dict:dict={}
        for param in params:
            try:
                name = param["name"]
                address = param["input"]["address"]
                address_dict[name] = address
            except:
                continue
        return address_dict
    
    def data_packer(self):
        '''
        Data calculating and packing at here, should out put 2 lists
        '''
        raise NotImplementedError

    def send(self):
        '''
        Send data has packed by data_packer
        '''
        data_list, addr_list, wait_list = self.data_packer()
        for (data,addr,wait_time) in zip(data_list, addr_list,wait_list):
            self.client.send_message(addr,data)
            print("Sended data to ", addr,", data:", data, " datetime:", datetime.datetime.now())
            sleep(wait_time)