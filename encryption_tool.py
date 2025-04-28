from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os
import argparse

# Generate a random 32-byte (256-bit) AES key
def generate_key():
    key = os.urandom(32)  # 32 bytes = 256 bits
    with open("aes.key", "wb") as key_file:
        key_file.write(key)
    print("[+] AES-256 key saved as 'aes.key'")

# Load AES key
def load_key():
    return open("aes.key", "rb").read()

# Encrypt file
def encrypt_file(file_path):
    key = load_key()
    backend = default_backend()
    iv = os.urandom(16)  # AES block size
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()

    with open(file_path, "rb") as f:
        data = f.read()

    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()

    encrypted = encryptor.update(padded_data) + encryptor.finalize()

    with open(file_path + ".enc", "wb") as f:
        f.write(iv + encrypted)  # Prepend IV for use during decryption

    print(f"[+] File encrypted and saved as {file_path}.enc")

# Decrypt file
def decrypt_file(encrypted_file_path):
    key = load_key()
    backend = default_backend()

    with open(encrypted_file_path, "rb") as f:
        iv = f.read(16)  # Read IV first
        encrypted_data = f.read()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    decryptor = cipher.decryptor()

    decrypted_padded = decryptor.update(encrypted_data) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    decrypted_data = unpadder.update(decrypted_padded) + unpadder.finalize()

    original_file = encrypted_file_path.replace(".enc", "_decrypted")
    with open(original_file, "wb") as f:
        f.write(decrypted_data)

    print(f"[+] File decrypted and saved as {original_file}")

def main():
    parser = argparse.ArgumentParser(description="Advanced AES-256 File Encryption Tool")
    parser.add_argument("-g", "--generate", help="Generate AES-256 key", action="store_true")
    parser.add_argument("-e", "--encrypt", help="Encrypt a file (Usage: -e <filepath>)", type=str)
    parser.add_argument("-d", "--decrypt", help="Decrypt a file (Usage: -d <filepath.enc>)", type=str)

    args = parser.parse_args()

    if args.generate:
        generate_key()
    elif args.encrypt:
        encrypt_file(args.encrypt)
    elif args.decrypt:
        decrypt_file(args.decrypt)
    else:
        print("[-] Use -h for help.")

if __name__ == "__main__":
    main()
