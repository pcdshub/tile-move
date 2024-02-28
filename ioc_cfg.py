#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 10:44:55 2024

@author: nagar123
"""
import json
from jinja2 import Environment, FileSystemLoader

env=Environment(loader=FileSystemLoader('.'), autoescape=True)

# Define the path to your JSON file
json_file_path = "/Users/nagar123/anaconda3/pcds_conda/db.json"


def happi_search(search_name, field):
   # search_name = "lm2k2_inj_dp1_tf1_sl1"  # The name you want to search for
    
    # Read the JSON file
    with open(json_file_path, "r") as file:
        data = json.load(file)
    
    # Search for the device by name
    found_device = None
    for key, value in data.items():
        if value.get(field) == search_name:
            found_device = value
            
            break
    
    # Check if the device was found
    if found_device:
        print("Device found:")
        return found_device
        print(found_device)
    else:
        print("Device not found.")
        return None
        
        
def elliptics():
    print("welcome to elliptecs")
    template=env.get_template('ell_template.txt')
    #search_name=input("Input the name of the device: ")
    search_name = "lm2k2_inj_dp1_tf1_sl1" 
    field='name'
    found_device=happi_search(search_name, field)
    print(found_device)
    vars={
    'release':found_device.get('ioc_release'),
    'engineer':found_device.get('ioc_engineer'),
    'location':found_device.get('beamline'),
    'ioc_pv':found_device.get('prefix'),
    'arch':found_device.get('ioc_arch'),
    'base':found_device.get('prefix'),
    'serial':found_device.get('ioc_serial'),
    'seq': int(found_device.get('ioc_channel')),
    'ioc_model': found_device.get('ioc_model'),
    'record':found_device.get('prefix'),
    'alias':found_device.get('ioc_alias')
    }
    output_ell=template.render(vars)
    print("writing output")
    output_file_path = "/Users/nagar123/anaconda3/pcds_conda/output_ell.cfg"
    with open(output_file_path, "w") as file:
        file.write(output_ell)
    
def ek9k():
    print("welcome to ek9k")
    template=env.get_template('ek9k_template.txt')
    
    search_name="ioc-lm2k2-atm-ek9000-01"
    field='ioc_name'
    port= int(input("Input port number: \n"))
    slaves=int(input("Input number of slaves: \n"))
    channels=int(input("Input number of channels: \n"))
    el3147="EL3147"

    found_device=happi_search(search_name, field)
    vars={
        'release':found_device.get('ioc_release'),
        'ioc_engineer':found_device.get('ioc_engineer'),
        'location':found_device.get('beamline'),
        'ioc_base':found_device.get('ioc_base'),
        'ioc_type':found_device.get('ioc_type'),
        'ioc_ip':found_device.get('ioc_ip'),
        'prefix':found_device.get('prefix'),
        'port':port, 'slaves' : slaves, 'channels':channels, 'type':el3147
    }
    output_ek9k=template.render(vars)
    print(output_ek9k)
    output_file_path = "/Users/nagar123/anaconda3/pcds_conda/output_ek9k.cfg"
    with open(output_file_path, "w") as file:
        file.write(output_ek9k)
    

def ioc_type():
    ioc_kind=input("Choose 1: Elleptics, 2: EK9000, 3: Smaract, 4:")
        
    if ioc_kind == '1':
        elliptics()
    elif ioc_kind == '2':
       ek9k()
    else :
        print("Awaiting smaracts")
       #else:
 #      smaract()
            
def main():
    ioc_type()

if __name__ == "__main__":
    main()