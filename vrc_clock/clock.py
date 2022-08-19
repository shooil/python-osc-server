import datetime
from osc_base.osc_base import osc_base
from pythonosc import udp_client

#Define all parameter name used in this class at here
PARAM_NAME_CLOCK_SEC_TOGGLE = "clock_sec_toggle"
PARAM_NAME_CLOCK_MIN_TOGGLE = "clock_min_toggle"
PARAM_NAME_CLOCK_HOUR_TOGGLE = "clock_hour_toggle"
PARAM_NAME_CLOCK_ROTATE_RATE = "clock_rotate_rate"

class vrc_clock(osc_base):
    def __init__(self,client:udp_client.SimpleUDPClient):
        super().__init__(client)
        self.clock_sec_toggle_addr = self.addr + PARAM_NAME_CLOCK_SEC_TOGGLE
        self.clock_min_toggle_addr = self.addr + PARAM_NAME_CLOCK_MIN_TOGGLE
        self.clock_hour_toggle_addr = self.addr + PARAM_NAME_CLOCK_HOUR_TOGGLE
        self.clock_rotate_rate_addr = self.addr + PARAM_NAME_CLOCK_ROTATE_RATE
    
    def calc_perc(self)->list:
        #Get the current time
        t_now = str(datetime.datetime.now().time()).split(".")[0]
        hour_value = int(t_now.split(":")[0])
        min_value = int(t_now.split(":")[1])
        sec_value = int(t_now.split(":")[2])
        #Calculate rate in animation
        sec_perc = sec_value/60
        min_perc = (min_value + sec_value/60)/60
        hour_perc = (hour_value % 12 + min_value/60)/12
        return [sec_perc,min_perc,hour_perc]

    def data_packer(self):
        '''
        Overridden, calculate data to send and pack data and address into 2 lists
        '''
        #Rearrangement data to send
        rot_data = self.calc_perc()
        data_list = [rot_data[0],1,0,rot_data[1],1,0,rot_data[2],1,0]
        wait_list = [0.1]*9
        #Rearrangement address for data to send
        addr_list_sec = [self.clock_rotate_rate_addr,self.clock_sec_toggle_addr,self.clock_sec_toggle_addr]
        addr_list_min = [self.clock_rotate_rate_addr,self.clock_min_toggle_addr,self.clock_min_toggle_addr]
        addr_list_hour = [self.clock_rotate_rate_addr,self.clock_hour_toggle_addr,self.clock_hour_toggle_addr]
        addr_list = addr_list_sec + addr_list_min + addr_list_hour
        return data_list, addr_list, wait_list