import socket
from bb84.bb84 import BB84Protocol
from messaging import xor_encrypt_decrypt

HOST = "127.0.0.1"
PORT = 65432

def main():
    # 1. Generate BB84 shared key
    bb84 = BB84Protocol(n_bits=32)
    alice_sifted = bb84.run()
    key_str = "".join(map(str, alice_sifted))
    print(f"[Alice] Shared key: {key_str}")

    # 2. Connect to Bob
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        # 3. Send BB84 key first
        s.sendall(key_str.encode("utf-8"))
        print("[Alice] BB84 key sent to Bob.")

        # 4. Input message
        message = input("Enter your message to Bob: ")

        # 5. Encrypt message
        encrypted = xor_encrypt_decrypt(message, key_str)
        print(f"[Alice] Encrypted message: {encrypted}")

        # 6. Send encrypted message
        s.sendall(encrypted.encode("utf-8"))
        print("[Alice] Message sent!")

if __name__ == "__main__":
    main()
