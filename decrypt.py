from Crypto.Cipher import AES
from binascii import unhexlify

key_hex = "4255794d3dccfd46953146e701b7db68"

payload_hex = (
    "a144c5142785895070078c20607a9d00902537ca231fa2da5889be8df367"
    "3ec136aebfb80d4ce395ba98f6b3844a115e4be1b1c9f0a2d5ffbb92906aa388deaa"
    "82c929310e9e5c4c0922a784df89cf0ded833be8da996eb5885409b6c9867978dea"
    "24001d68c603408d758a1e2b91c42ebad86a9b9d287880083bb0702850574d7b51"
    "e9c209ed68e0374e9b01febfd92b4cb9410fdeaf7fb526b742dc9a8d0682653"
)

key = unhexlify(key_hex)
data = unhexlify(payload_hex)

# Trim to AES block size
block_size = 16
trim_len = len(data) - (len(data) % block_size)
data = data[:trim_len]

iv = bytes(16)  # OMS default IV = 0x00..00

cipher = AES.new(key, AES.MODE_CBC, iv)
decrypted = cipher.decrypt(data)

print("Decrypted payload (HEX):")
print(decrypted.hex())

print("\nDecrypted payload (ASCII, best effort):")
print(decrypted.decode(errors="replace"))
