import time
import json


class ServerInformation():

    def __init__(self,server_info_path):
        self.server_info_path = server_info_path
        self.update()


    def update(self):
        with open(self.server_info_path,'r') as f:
            self.server_info = json.load(f)

