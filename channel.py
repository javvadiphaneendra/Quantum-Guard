# channel.py
import socket
import json

def send_message(conn, data):
    """Send JSON-encoded message"""
    msg = json.dumps(data).encode()
    conn.sendall(msg + b"\n")

def recv_message(conn):
    """Receive JSON-encoded message"""
    buffer = b""
    while not buffer.endswith(b"\n"):
        chunk = conn.recv(4096)
        if not chunk:
            break
        buffer += chunk
    return json.loads(buffer.decode())
