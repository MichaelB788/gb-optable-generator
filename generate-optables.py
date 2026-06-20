#!/usr/bin/env python3
import json

def generate_optable(optable_data, prefix):
    # Write the array signature.
    optable_buf = f"static const struct opcode_info {prefix}[256] = {{"

    for opcode, data in optable_data[prefix].items(): 
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

        
        # Append the entry
        optable_buf += f"\n  {{ {opcode}, {cycles}, \"{mnemonic}\" }},"

    # Remove trailing comma at the last entry, and close the array
    return f"{optable_buf[:-1]}}};\n\n"

def main():
    with open("Opcodes.json", "r") as optable_json:
        optable_data = json.load(optable_json)
        with open("optables.h", "w") as output_file:
            output_file.write(
                "#pragma once\n"
                "#include <stdint.h>\n\n"
                "struct opcode_info {\n"
                "  uint8_t opcode;\n"
                "  uint8_t cycles_taken;\n"
                "  uint8_t cycles_untaken;\n"
                "  const char *mnemonic;\n"
                "};\n\n"
            )
            output_file.write(generate_optable(optable_data, "unprefixed"))
            output_file.write("")
            output_file.write(generate_optable(optable_data, "cbprefixed"))

if __name__ == "__main__":
    main()
