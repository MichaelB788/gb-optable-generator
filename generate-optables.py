#!/usr/bin/env python3
import json

def generate_optable(prefixed_optable_data):
    for opcode, data in prefixed_optable_data.items(): 
        # Form the mnemonic
        mnemonic = data["mnemonic"]
        for operand in data["operands"]:
            if not operand["immediate"] and not "bytes" in operand:
                operand_str = f" [{operand["name"]}]"
            else:
                operand_str = f" {operand["name"]}"
            mnemonic += operand_str

        # Form the cycles taken and untaken values
        cycles = f"{data["cycles"][0]}, {data["cycles"][0] if
                    len(data["cycles"]) == 1 else data["cycles"][1]}"

        
        print(f"{{ {opcode}, {cycles}, \"{mnemonic}\" }},")

def main():
    with open("Opcodes.json", "r") as optable_json:
        optable_data = json.load(optable_json)
        generate_optable(optable_data["unprefixed"])
        print("")
        generate_optable(optable_data["cbprefixed"])

if __name__ == "__main__":
    main()
