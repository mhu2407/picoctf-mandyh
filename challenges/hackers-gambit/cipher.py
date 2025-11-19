from pathlib import Path
from Crypto.Cipher import AES

BLOCK_SIZE = 16

KEY = b'\x1e\xd7\x8b\xfc\x49\x74\xfc\xb5\x3c\x29\x77\xa0\xae\xfa\xea\x26'
IV  = b'\x2f\x9d\x0d\xb7\x9f\x4f\x58\xc2\xcb\x01\xe1\xcb\x07\xfd\x71\x51' 

def main():
    base_dir = Path(__file__).resolve().parent

    board_file = base_dir / "starting-board.txt"
    output = base_dir / "ciphertext.bin"

    board_text = board_file.read_text(encoding="utf-8")
    board_bytes = board_text.encode("utf-8")

    length = BLOCK_SIZE - (len(board_bytes) % BLOCK_SIZE)
    padded_text = board_bytes + bytes([length]) * length

    c = AES.new(KEY, AES.MODE_CBC, IV)
    ciphertext = c.encrypt(padded_text)

    output.write_bytes(ciphertext)
    print(ciphertext.hex())


if __name__ == "__main__":
    main()
