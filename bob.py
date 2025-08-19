# bob.py
import socket
import json
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation

HOST = "127.0.0.1"
PORT = 65432

def generate_bob_data(alice_bits, alice_bases):
    """Bob randomly chooses bases and measures bits accordingly"""
    bob_bases = [random.choice(["+", "x"]) for _ in alice_bits]
    bob_bits = []
    for bit, a_base, b_base in zip(alice_bits, alice_bases, bob_bases):
        if a_base == b_base:
            bob_bits.append(bit)  # Correct measurement
        else:
            bob_bits.append(random.randint(0, 1))  # Wrong measurement
    return bob_bits, bob_bases

def sift_key(alice_bits, alice_bases, bob_bits, bob_bases):
    sifted = []
    mismatches = 0
    total = 0
    match_positions = []
    for i, (a_bit, a_base, b_bit, b_base) in enumerate(zip(alice_bits, alice_bases, bob_bits, bob_bases)):
        if a_base == b_base:
            sifted.append(a_bit)
            match_positions.append(i)
            total += 1
            if a_bit != b_bit:
                mismatches += 1
    qber = mismatches / total if total > 0 else 0
    return sifted, qber, match_positions

def eve_attack(bits, bases):
    """ Eve randomly measures and resends, causing errors """
    eve_bases = [random.choice(["+", "x"]) for _ in bits]
    eve_measurements = []
    for bit, base, eve_base in zip(bits, bases, eve_bases):
        if base == eve_base:
            eve_measurements.append(bit)
        else:
            eve_measurements.append(random.randint(0, 1))
    return eve_measurements, eve_bases

def animate_bb84(alice_bits, alice_bases, bob_clean_bits, bob_clean_bases, bob_eve_bits, bob_eve_bases, sifted_clean, qber_clean, sifted_eve, qber_eve):
    n = len(alice_bits)
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle("QUANTUMQUARD(BB84 Quantum Key Distribution) — Clean vs Attacked (Bob’s View)")

    # CLEAN channel
    ax1, ax2 = axes[0]
    ax1.set_title("Alice → Bob (Clean)")
    line_alice_clean, = ax1.plot([], [], 'o-', label="Alice Bits")
    line_bob_clean, = ax1.plot([], [], 's-', label="Bob Bits")
    ax1.set_xlim(0, n)
    ax1.set_ylim(-0.5, 1.5)
    ax1.legend()

    line_sifted_clean, = ax2.plot([], [], 'o-', color="purple", label="Sifted Key")
    ax2.set_xlim(0, n)
    ax2.set_ylim(-0.5, 1.5)
    ax2.legend()

    # ATTACKED channel
    ax3, ax4 = axes[1]
    ax3.set_title("Alice → Eve → Bob (Attacked)")
    line_alice_eve, = ax3.plot([], [], 'o-', label="Alice Bits")
    line_bob_eve, = ax3.plot([], [], 's-', label="Bob Bits (after Eve)")
    ax3.set_xlim(0, n)
    ax3.set_ylim(-0.5, 1.5)
    ax3.legend()

    line_sifted_eve, = ax4.plot([], [], 'o-', color="red", label="Sifted Key (with Eve)")
    ax4.set_xlim(0, n)
    ax4.set_ylim(-0.5, 1.5)
    ax4.legend()

    # Holders
    alice_y_clean, bob_y_clean, sifted_y_clean = [], [], []
    alice_y_eve, bob_y_eve, sifted_y_eve = [], [], []

    def update(frame):
        # Clean
        alice_y_clean.append(alice_bits[frame])
        bob_y_clean.append(bob_clean_bits[frame])
        line_alice_clean.set_data(range(len(alice_y_clean)), alice_y_clean)
        line_bob_clean.set_data(range(len(bob_y_clean)), bob_y_clean)
        if alice_bases[frame] == bob_clean_bases[frame]:
            sifted_y_clean.append(alice_bits[frame])
        line_sifted_clean.set_data(range(len(sifted_y_clean)), sifted_y_clean)
        ax2.set_title(f"Clean QBER = {qber_clean*100:.1f}%")

        # Eve
        alice_y_eve.append(alice_bits[frame])
        bob_y_eve.append(bob_eve_bits[frame])
        line_alice_eve.set_data(range(len(alice_y_eve)), alice_y_eve)
        line_bob_eve.set_data(range(len(bob_y_eve)), bob_y_eve)
        if alice_bases[frame] == bob_eve_bases[frame]:
            sifted_y_eve.append(alice_bits[frame])
        line_sifted_eve.set_data(range(len(sifted_y_eve)), sifted_y_eve)
        ax4.set_title(f"Attacked QBER = {qber_eve*100:.1f}%")

        return line_alice_clean, line_bob_clean, line_sifted_clean, line_alice_eve, line_bob_eve, line_sifted_eve

    ani = animation.FuncAnimation(fig, update, frames=n, interval=800, blit=True, repeat=False)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("[Bob] Waiting for Alice...")
        conn, addr = s.accept()
        with conn:
            print(f"[Bob] Connected to {addr}")
            data = conn.recv(4096).decode()
            msg = json.loads(data)
            alice_bits = msg["alice_bits"]
            alice_bases = msg["alice_bases"]

            bob_bits, bob_bases = generate_bob_data(alice_bits, alice_bases)
            response = {"bob_bits": bob_bits, "bob_bases": bob_bases}
            conn.sendall(json.dumps(response).encode())

    # Case 1: Clean
    sifted_clean, qber_clean, _ = sift_key(alice_bits, alice_bases, bob_bits, bob_bases)

    # Case 2: Eve attack
    eve_measurements, eve_bases = eve_attack(alice_bits, alice_bases)
    sifted_eve, qber_eve, _ = sift_key(alice_bits, alice_bases, eve_measurements, eve_bases)

    print(f"[Bob] Clean QBER: {qber_clean*100:.1f}% | Attacked QBER: {qber_eve*100:.1f}%")

    animate_bb84(alice_bits, alice_bases, bob_bits, bob_bases, eve_measurements, eve_bases, sifted_clean, qber_clean, sifted_eve, qber_eve)
