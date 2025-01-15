from cryptography.fernet import Fernet

# reading contents from cocktail.txt
key = open("../dist/cocktail.txt", "r").read()

# converting each number from hex to dec
key = [int(key_e, 16) for key_e in key.split()]

# converting each number to it's ascii representation
key = [chr(num) for num in key]

# joining the previous list together so as to get a new sequence of number
key = "".join(key)

# converting each number from oct to dec
key = [int(key_f, 8) for key_f in key.split()]

# onc again, converting each number to it's ascii representation
key = [chr(num) for num in key]

# once again, joining the previous list together so as to get a string, which represented the real Fernet key
key = "".join(key)

print(f"{key = }")

f = Fernet(
    key.encode()
)

with open("file.png", "wb") as file:
    file.write(
        f.decrypt(
            open("../dist/file.xxx", "rb").read()
        )
    )