#!/usr/bin/env python3
import yaml
import re
import pandas as pd

RED = "\033[31m"
RESET = "\033[0m"


class OpcodeChecker:

    def __init__(self, opcodes_path, arguments_path):
        self.opcodes = self._load_opcodes(opcodes_path)
        self.arguments = self._load_arguments(arguments_path)
        self.ranges = self._get_ranges()

    def _load_opcodes(self, yaml_file):
        with open(yaml_file, 'r') as file:
            opcodes = yaml.safe_load(file)
            return opcodes
    
    def _load_arguments(self, file_path):
        table = pd.read_csv(file_path, header=None)
        argument_lookup = []
        for index, row in table.iterrows():
            field_name = row[0]
            argument_lookup.append(field_name)    
        return argument_lookup

    def _get_ranges(self):
        ranges = {}
        for opcode_name, opcode_value in self.opcodes.items():
            encoding = opcode_value["encoding"]            
            results = re.finditer(r"(\d+)", encoding)
            ranges[opcode_name] = []          
            
            for item in results:
                msb = 31-item.start()
                lsb = 31-item.end()+1 #it must be added +1 as the match.end() returns a position after the last character.
                value = item.group(0)
                ranges[opcode_name].append([msb,lsb,value])
        return ranges
    
    def check_bit_ranges(self):
        print("\nBit Range check:")
        status = True
        for opcode_name, definitions in self.ranges.items():
            mask = int(self.opcodes[opcode_name]["mask"], 16)
            pseudo_mask = 0b0
            for definition in definitions:
                msb = definition[0]
                lsb = definition[1]
                pre_mask = msb-lsb+1                    
                ones = (1 << pre_mask)-1
                shift = msb-(msb-lsb)
                pseudo_mask |= (ones << shift)
                    
            if mask == pseudo_mask:
                print(f"{opcode_name} - OK")
            else:
                print(f"{RED}{opcode_name} - overlapping ERROR{RESET}")
                status = False
                
        return status
                    
    def do_values_fit(self):
        print("\nWidth check:")
        status = True
        for opcode_name, definitions in self.ranges.items():
            match = int(self.opcodes[opcode_name]["match"], 16)
            pseudo_match = 0b0
            for definition in definitions:
                msb = definition[0]
                lsb = definition[1]
                pre_match = int(definition[2],2)                  
                shift = msb-(msb-lsb)
                pseudo_match |= (pre_match << shift)
                
            if match == pseudo_match:
                print(f"{opcode_name} - OK")
            else:
                print(f"{RED}{opcode_name} - Width value ERROR{RESET}")
                status = False
                
        return status
        
    def check_arguments(self):
        print("\nArgument Check:")
        status = True
        for opcode_name, opcode_value in self.opcodes.items():
            variable_fields = opcode_value['variable_fields']
            for field in variable_fields:
                if field not in self.arguments:
                    print(f"{RED}{opcode_name} ({field}) Argument not found ERROR.{RESET}")
                    status = False                
                else:
                    print(f"{opcode_name} ({field}) - OK")
                    
        return status

if __name__ == "__main__":
    opcodeChecker = OpcodeChecker('instr_dict.yaml', "arg_lut.csv")
    
    a=opcodeChecker.check_bit_ranges()
    b=opcodeChecker.do_values_fit()
    c=opcodeChecker.check_arguments()
    
    if a and b and c:
        print("\nSuccesfull")
    else:
        print("\nUnsuccesfull")