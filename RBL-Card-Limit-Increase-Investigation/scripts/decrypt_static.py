from pathlib import Path
from hashlib import sha256
from cryptography.hazmat.primitives.ciphers import (
    Cipher, algorithms, modes
)
from cryptography.hazmat.primitives.padding import PKCS7

src = Path("recovery/payload_analysis/profile.encrypted")
dst = Path("recovery/payload_analysis/payload.decrypted")

key = bytes.fromhex(
    "b7fcadb82c9ee0bf873c9c1b670285c2"
    "2814b69201d01fe640cb2e409131b7f1"
)

data = src.read_bytes()

if len(data) <= 16:
    raise SystemExit("ERROR: Input is too short to contain IV and ciphertext.")

iv, ciphertext = data[:16], data[16:]

if len(ciphertext) == 0 or len(ciphertext) % 16:
    raise SystemExit(
        f"ERROR: Ciphertext length {len(ciphertext)} "
        "is not a positive multiple of AES's 16-byte block size."
    )

decryptor = Cipher(
    algorithms.AES(key), modes.CBC(iv)
).decryptor()

padded = decryptor.update(ciphertext) + decryptor.finalize()

unpadder = PKCS7(128).unpadder()
plaintext = unpadder.update(padded) + unpadder.finalize()

# Create a new output; never overwrite the encrypted evidence.
with dst.open("xb") as f:
    f.write(plaintext)

print("Static decryption completed.")
print("Output:", dst)
print("Size:", len(plaintext), "bytes")
print("SHA-256:", sha256(plaintext).hexdigest())