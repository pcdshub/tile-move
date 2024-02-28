
import argparse
import json
import re
from happi import Client
from happi.errors import DuplicateError
#from validate import validate
import pandas as pd


class GroupChange:
    def __init__(self, db_path):
        self.client=Client(path='/reg/g/pcds/epics-dev/nagar123/mods/db.json')
       # self.validator =validate()

    #do we want a confirmation prompt for each entry or once for all in the location_group?
    def display_changes(self, entry):
            entry.item.show_info()
    
    def all_chars_caps_ignore_special(self, string):
        """
        Check if all alphabetic characters in the string are uppercase, ignoring special characters.
        """
        # Iterate through each character in the string
        for char in string:
            # Check if the character is an alphabetic character
            if char.isalpha():
                # Check if the alphabetic character is not uppercase
                if not char.isupper():
                    return False  # Return False if any alphabetic character is not uppercase
        return True
                
    def location_group_change(self, loc_grp, new_name):
        dict_beamline={'LM2K2':'CRIX_MODS','LM1K4':'IP1_MODS','LM1K2':'QRIX_MODS'}
        
        test_arr={'ioc_alias', 'ioc_base','prefix','ioc_name','location_group','name','beamline', 'ioc_location'}
        json_file_path = "/reg/g/pcds/epics-dev/nagar123/mods/db.json"

        loc_code = loc_grp.split('_')[1]
        entries_to_modify = self.client.search(location_group=loc_grp)
        print(f"Number of entries that will be modified are {len(entries_to_modify)}")
        # Read the JSON file
        with open(json_file_path, "r") as file:
          data = json.load(file)

        if not entries_to_modify:
            print("No entries found for the search criteria.")
        else:
            globalFlag=0
            confirm_ALL=input("\n Do you want to skip verification and confirm changes for all devices (y/N)").strip().lower()
            # set flag=1 if we want to skip verification for all devices
            if confirm_ALL == 'y':
                globalFlag=1

            for entry in entries_to_modify:
                initial_values={}
                final_values={}
                
                #try:
                for test_item in test_arr:
                                if test_item in entry:
                                    if(self.all_chars_caps_ignore_special(str(entry[test_item]))):
                                        initial_values[str(test_item)]= entry[test_item]
                                        print("if meta", entry.metadata['name'])
                                        entry.metadata[test_item]=str(entry.item.get(test_item)).replace(loc_code.upper(), new_name.upper())
                                        entry.item.save()
                                        final_values[str(test_item)]= entry[test_item]
                                    else:
                                        initial_values[str(test_item)]= entry[test_item]
                                        #print("before" ,entry)
                                        entry.metadata[test_item]=str(entry.item.get(test_item)).replace(loc_code.lower(), new_name.lower())
                                        #print("after ", entry, "\n")
                                        entry.item.save()                                        
                                        final_values[str(test_item)]= entry.metadata[test_item]
                                
                                if test_item == 'beamline':
                                    initial_values[str(test_item)]= entry[test_item]
                                    entry.metadata[test_item]=dict_beamline[new_name.upper()]    
                                    entry.item.save()
                                    final_values[str(test_item)]= entry[test_item]
                df_initial=pd.DataFrame.from_dict(initial_values, orient='index', columns=['Old Value'])
                df_initial.index.name='Device parameter'

                df_final=pd.DataFrame.from_dict(final_values, orient='index', columns=['New Value'])
                df_final.index.name='Device parameter'

                df_compare=pd.concat([df_initial, df_final], axis=1)
                print(df_compare)
    def main(self, loc_grp, new_name):
        if not loc_grp or not new_name:
                print("Please provide both location group (--loc_grp) and new name (--new_name)")
                return
        self.location_group_change(loc_grp, new_name)

        
if __name__ == "__main__":
        #conda_activate_cmd="source pcds_conda"
        #subprocess.run(conda_activate_cmd, shell=True, executable="/bin/sh")

        parser = argparse.ArgumentParser()
        parser.add_argument("--i", help="intial location group for devices to be shifted")
        parser.add_argument("--f", help="final destination location code for the devices after shifting")

        args = parser.parse_args()
        loc_grp = args.i
        new_name = args.f

        group_change = GroupChange('/reg/g/pcds/epics-dev/nagar123/mods/db.json')
        group_change.main(loc_grp, new_name)
        #conda_env_path = "/cds/group/pcds/pyps/conda/py39/envs/pcds-5.8.1"