import os, binascii

key = os.urandom(16)
iv = os.urandom(16)

print("KEY (python bytes literal):", repr(key))
print("IV  (python bytes literal):", repr(iv))

print("KEY (hex):", binascii.hexlify(key).decode())
print("IV  (hex):", binascii.hexlify(iv).decode())
