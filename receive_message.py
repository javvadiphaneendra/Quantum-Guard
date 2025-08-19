import socket
from messaging import xor_encrypt_decrypt
from utils.visualize_bb84 import animate_bb84

HOST = "127.0.0.1"
PORT = 65432

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("[Bob] Waiting for Alice...")
        conn, addr = s.accept()
        with conn:
            # 1. Receive BB84 key
            key_str = conn.recv(1024).decode("utf-8")
            print(f"[Bob] Received shared key: {key_str}")

            # 2. Animate BB84 reception
            bob_bits = [int(b) for b in key_str]
            animate_bb84(alice_bits=bob_bits, bob_bits=bob_bits, interval=200, save=False)

            # 3. Receive encrypted message
            encrypted = conn.recv(1024).decode("utf-8")
            print(f"[Bob] Encrypted message received: {encrypted}")

            # 4. Decrypt message
            decrypted = xor_encrypt_decrypt(encrypted, key_str)
            print(f"[Bob] Decrypted message: {decrypted}")

if __name__ == "__main__":
    main()
