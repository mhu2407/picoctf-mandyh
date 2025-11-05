#!/usr/bin/env python3
import requests
import base64
import sys

URL = "http://localhost:8001"
session = requests.Session()

def encrypt(m0, m1):
    r = session.post(f"{URL}/encrypt", json={"m0": m0, "m1": m1})
    return r.json()["ciphertext"]

def solve(guess):
    r = session.post(f"{URL}/solve", json={"guess": guess})
    return r.json()

def has_repeated_block(ciphertext_b64):
    ciphertext = base64.b64decode(ciphertext_b64)
    blocks = [ciphertext[i:i+16] for i in range(0, len(ciphertext), 16)]
    return len(set(blocks)) < len(blocks)

def play_game():
    score = 0
    while score < 10:
        m0 = "A" * 32              # Two identical blocks
        m1 = "B" * 16 + "C" * 16    # Two different blocks
        ct = encrypt(m0, m1)
        guess = 0 if has_repeated_block(ct) else 1
        res = solve(guess)
        score = res["score"]
        print(f"Guessed {guess}, new score: {score}")
        if "flag" in res:
            print(f"\n🎉 FLAG: {res['flag']}")
            return

if __name__ == "__main__":
    URL=sys.argv[1]
    play_game()
