# Opcode Checker

This project provides a tool to verify the consistency of metadata in opcode definitions.

## Description

The `OpcodeChecker` script reads a YAML file containing opcode definitions and a CSV file providing an argument lookup table. It verifies the consistency of the metadata by ensuring no overlapping bit ranges, validating that the values assigned to bit ranges are representable within their specified width, and checking that all arguments used in the instructions have mappings in the lookup table.

## Requirements

- Python 3.6 or higher
- pandas
- pyyaml

## Installation

1. Clone this repository to your local machine:

    ```sh
    git clone https://github.com/rodaciri/opcodeChecker.git
    cd opcodeChecker
    ```

2. Install the dependencies using `pip`:

    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Ensure you have the `instr_dict.yaml` and `arg_lut.csv` files in the same directory as the script.

2. Run the script:

    ```sh
    python opcodeChecker.py
    ```
3. Note: you can change the YAML that you want to examine in line 102, by replacing `instr_dict.yaml` with the rout of your own YAML file.

## Files

- `opcodeChecker.py`: Main script that performs the checks.
- `instr_dict.yaml`: YAML file containing opcode definitions.
- `arg_lut.csv`: CSV file providing the argument lookup table.
- `opcodes.yaml`: Just another YAML file there to test the script.

## Example Output

Bit Range check:
- add - OK
- add_uw - OK
- addi - OK

Width check:
- add - OK
- add_uw - OK
- addi - OK

Argument Check:
- add (rd) - OK
- add (rs1) - OK
- add (rs2) - OK
- add_uw (rd) - OK
- add_uw (rs1) - OK
- add_uw (rs2) - OK
- addi (rd) - OK
- addi (rs1) - OK
- addi (imm12) - OK

Succesfull
