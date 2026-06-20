#!/usr/bin/env python3
import json

def generate_optable(optable_data, prefix):
    entries = []

    for opcode, data in optable_data[prefix].items():
        operands = ",".join(
            f" [{operand['name']}]" if not operand["immediate"]
            else f" {operand['name']}"
            for operand in data["operands"]
        )
        mnemonic = data["mnemonic"] + operands

        taken = data["cycles"][0]
        untaken = data["cycles"][1] if len(data["cycles"]) > 1 else taken

        entries.append(
            f'  {{{opcode}, {taken}, {untaken}, "{mnemonic}"}}'
        )

    return (
        f"static const struct opcode_info {prefix}[256] = {{\n"
        + ",\n".join(entries)
        + "\n};\n\n"
    )

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
