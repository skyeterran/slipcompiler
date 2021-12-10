instruction_opcodes = {
    "IDK": 0x00,
    "LIT": 0x01,
    "SWAP": 0x02,
    "DEL": 0x03,
    "COPY": 0x04,
    "DEF": 0x05,
    "END": 0x06,
    "ADD": 0x10,
    "SUB": 0x11,
    "MUL": 0x12,
    "DIV": 0x13,
    "POW": 0x14,
    "SQRT": 0x15,
    "ONEMIN": 0x16,
    "ROUND": 0x17,
    "CEIL": 0x18,
    "FLOOR": 0x19,
    "MOD": 0x1a,
    "FRACT": 0x1b,
    "COMP": 0x1c,
    "LERP": 0x1d,
    "MIN": 0x1e,
    "MAX": 0x1f
}

type_opcodes = {
    "BOOL": {"code": 0x00, "length": 1},
    "INT": {"code": 0x01, "length": 4},
    "FLT": {"code": 0x02, "length": 4},
    "VEC": {"code": 0x03, "length": 12}
}

source_file = open("Test.slc")
source_code = source_file.read()
source_code = source_code.replace(" ", "\n")
source_code = source_code.split("\n")

import struct

byte_code = bytearray()
code_type = ""
lit_type = ""
for word in source_code:
    print(f"\nIn: \"{word}\"")
    # Handle literal types
    if code_type == "lit_type":
        print("Consuming literal type...")
        print("Expecting next input to be a literal value.")

        # Consume a literal of this word's type next
        code_type = "literal"
        lit_type = word

        # Push the type opcode onto the instruction stack
        opcode = type_opcodes[word]["code"]
        byte_code.append(opcode)
        print(f"Out: {hex(opcode)}")
        continue
    # Handle literal values
    if code_type == "literal":
        print("Consuming literal value...")

        # Consume a generic command next
        code_type = ""

        # Handle float literals
        if lit_type == "FLT":
            lit_bytes = bytearray(struct.pack(">f", float(word)))
            byte_code.extend(lit_bytes)
            print(f"Out: 0x{bytes(lit_bytes).hex()}")
        # Handle vector literals
        if lit_type == "VEC":
            # Creates an array of floats from a string like "-1.0,7.3,10.5"
            vector_components = word.split(",")
            lit_bytes = bytearray()
            for component in vector_components:
                component_bytes = bytearray(struct.pack(">f", float(component)))
                lit_bytes.extend(component_bytes)
            byte_code.extend(lit_bytes)
            print(f"Out: 0x{bytes(lit_bytes).hex()}")
        continue
    # Handle generic commands
    else:
        print("Consuming generic command...")
        if word == "LIT":
            print("Expecting next input to be a literal type.")
            code_type = "lit_type"
        opcode = instruction_opcodes[word]
        byte_code.append(opcode)
        print(f"Out: {hex(opcode)}")
        continue

pure_bytes = bytes(byte_code)
with open("Test.vcr", "wb") as binary_file:
    binary_file.write(pure_bytes)

print("\nWrote binary file to disk!")