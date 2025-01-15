portion = open("../dist/sonet_97_by_William_Shakespeare.txt", "rb").read()

# \x00 => 0
# \xa0 => 160

gathered_bits = ""

for byte in portion:
    if not byte:
        gathered_bits += "0"
    elif byte == 160:
        gathered_bits += "1"

flag = "".join(
    chr(
        int(gathered_bits[index : index+8], 2)
    ) for index in range(0, len(gathered_bits), 8)
)

print(f"{flag = }")