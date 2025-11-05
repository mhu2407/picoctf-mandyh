from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from itsdangerous import Signer
import base64
import os
import logging

app = FastAPI()
sessions = {}

SERVER_SECRET_KEY = os.environ.get("SEED")
if SERVER_SECRET_KEY is None:
    print("Server secret key not set. Picking random value.")
    SERVER_SECRET_KEY=os.urandom(32)

assert len(SERVER_SECRET_KEY) == 32  # Must be for AES-256

signer = Signer(SERVER_SECRET_KEY) 

logger = logging.getLogger("uvicorn")


BLOCK_SIZE = 16
PADDING = '{'

# Load flag once
with open("/challenge/flag", "r") as f:
    FLAG = f.read().strip()

# We send the user the bit we used to encrypt the message so 
# we can score them. Obviously we don't want them just reading
# that session bit, so we encrypt it with a secret key.
# Here we use an actually secure cipher mode. 
def encrypt_bit(bit: int) -> str:
    nonce = get_random_bytes(12)
    cipher = AES.new(SERVER_SECRET_KEY, AES.MODE_GCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(bytes([bit]))
    return base64.b64encode(nonce + tag + ciphertext).decode()

def decrypt_bit(blob_b64: str) -> int:
    blob = base64.b64decode(blob_b64)
    nonce, tag, ciphertext = blob[:12], blob[12:28], blob[28:]
    cipher = AES.new(SERVER_SECRET_KEY, AES.MODE_GCM, nonce=nonce)
    bit = cipher.decrypt_and_verify(ciphertext, tag)[0]
    return bit


# --- Utilities ---
def pad(s):
    return s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING

def encrypt_encode(cipher, pt):
    return base64.b64encode(cipher.encrypt(pad(pt).encode())).decode()

def init_session():
    return {
        "score": 0,
        "key": os.urandom(32),          # secret AES key (never exposed)
        "last_encryption": None         # stores {"bit": 0 or 1}
    }

def get_cipher(session):
    return AES.new(os.urandom(32), AES.MODE_ECB)

# --- Request Models ---
class EncryptInput(BaseModel):
    m0: str
    m1: str

class SolveInput(BaseModel):
    guess: int

# --- Session Middleware ---
@app.middleware("http")
async def add_session(request: Request, call_next):
    sid_cookie = request.cookies.get("session_id")
    sid = None
    if sid_cookie:
        try:
            sid = signer.unsign(sid_cookie.encode()).decode()
        except Exception:
            # prevent session forgery.
            print("⚠️ Invalid session signature detected. Starting fresh session.")
            sid = None

    if not sid or sid not in sessions:
        sid = os.urandom(8).hex()
        sessions[sid] = init_session()

    request.state.session_id = sid
    response = await call_next(request)
    signed_sid = signer.sign(sid.encode()).decode()
    response.set_cookie("session_id", signed_sid)
    return response

# --- Routes ---
@app.post("/encrypt")
def encrypt(input: EncryptInput, request: Request):
    session = sessions[request.state.session_id]

    if len(input.m0) != len(input.m1):
        return {"error": "Inputs must be the same length."}

    bit = os.urandom(1)[0] % 2
    session["last_encryption"] = {"bit": encrypt_bit(bit)}  # store the current challenge

    logger.info(f"Encrypting with bit: {bit}")

    pt = input.m0 if bit == 0 else input.m1
    ct = encrypt_encode(get_cipher(session), pt)
    return {"ciphertext": ct, "score": session["score"]}

@app.post("/solve")
def solve(input: SolveInput, request: Request):
    session = sessions[request.state.session_id]
    last = session.get("last_encryption")

    if last is None:
        return {"error": "No previous encryption to solve."}

    if input.guess == decrypt_bit(last["bit"]):
        session["score"] += 1
    else:
        session["score"] -= 1

    session["last_encryption"] = None  # prevent repeated guessing

    if session["score"] >= 10:
        return {"flag": FLAG, "score": session["score"]}

    return {"score": session["score"]}

@app.get("/status")
def status(request: Request):
    session = sessions[request.state.session_id]
    return {"score": session["score"]}

# --- Static Frontend ---
app.mount("/", StaticFiles(directory="static", html=True), name="static")

@app.get("/")
def root():
    return FileResponse("static/index.html")
