
'''
Idea is to source the IOC template from the location where the 
present IOC is and modify parameters based on new location code.
Second step would be to combine with group change to do this iteratively.
Run this where you want new cfg to be stored, for sake of simplicity

'''
import os
from os import path
import shutil
import argparse 
import sys
import re
import subprocess
import json
import pandas as pd

from happi import Client
from happi.errors import DuplicateError
#from tile_move import GroupChange
'''
class Config_gen:
    def __init__():
'''
# open the file and if the field to be updated exists, record its value and update it
def update_cfg(cfg_path, device_name, loc_code):
    #try:
        with open(cfg_path, 'r') as file:
            cfg=file.read
        
        client= Client(path='/reg/g/pcds/epics-dev/nagar123/mods/db.json')
        device=client.search(name=device_name)
        for d in device:
            print(d)
        old_code=d.item.location_group.split('_')[1]# to substitute all instances of old loc with new loc_code
        # create a directory for storing new cfg file in the current working directory
        dir_name="test_cfg"
        current_dir=os.getcwd()
        dir_path = os.path.join(current_dir, dir_name)
        os.makedirs(dir_path, exist_ok=True)

        source_cfg=os.path.basename(cfg_path)
        dest_cfg=os.path.join(dir_path, source_cfg)
        #created a copy of the cfg file in current dir/test_cfg
        shutil.copy2(source_cfg, dest_cfg)
        
        with open(dest_cfg, 'r') as file:
            mod_cfg= file.read()




        #ioc_release, ioc_serial, ioc_model, ioc_arch, ioc_channel do not change
        #ioc_alias, ioc_base, ioc_name associated fields in cfg change
        #clean_cfg= clean_ansi(mod_cfg)
            
        #generate a pattern 
        pattern = re.compile(re.escape(old_code), re.IGNORECASE)
        #print(pattern)
        mod_cfg= pattern.sub(lambda match: loc_code.upper() if match.group().isupper() else loc_code.lower(), mod_cfg)
        with open(dest_cfg, 'w') as file:
            file.write(mod_cfg)
    #except OSError:
       #  print("Input valid path to cfg file")


        
        
#def main(device_name,cfg_path,loc_code):
     #update_cfg(cfg_path, device_name, loc_code)
     #update_cfg('/reg/g/pcds/epics-dev/nagar123/mods/mods_tile_move/tile-move', 'lm2k2_inj_dp1_tf1_sl1', 'lm9k9')
def main():   
    device_name = "lm2k2_inj_dp1_tf1_sl1"
    cfg_path = "/reg/g/pcds/epics-dev/nagar123/mods/mods_tile_move/tile-move/ioc-test-file.cfg"
    loc_code = "lm9k9"
    update_cfg(cfg_path,device_name,loc_code)
     
if __name__ == "__main__":
        #conda_activate_cmd="source pcds_conda"
        #subprocess.run(conda_activate_cmd, shell=True, executable="/bin/sh")
        #argumments for argparse can be improved
        main()
        '''
        parser = argparse.ArgumentParser()
        parser.add_argument("--n", help="name of device to be shifted")
        parser.add_argument("--cfg", help="absolute path to ioc cfg file")
        parser.add_argument("--f", help="final destination location code for the devices after shifting")
        args = parser.parse_args()
        device_name = args.n
        cfg_path = args.cfg
        loc_code=args.f
        '''
