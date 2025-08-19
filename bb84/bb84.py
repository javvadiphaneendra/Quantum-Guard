# bb84.py
print("[DEBUG] Running bb84.py from correct file")

import random
from qrng.qrng import QuantumRandomGenerator

class BB84Protocol:
    def __init__(self, n_bits=128):
        self.n_bits = n_bits
        self.qrng = QuantumRandomGenerator()
        
        # Initialize all attributes
        self.alice_bits = []
        self.alice_bases = []
        self.bob_bases = []
        self.bob_results = []
        self.sifted_key = []

    def generate_random_bits_and_bases(self):
        """Generate Alice's bits and bases, and Bob's bases."""
        self.alice_bits = [self.qrng.get_bit() for _ in range(self.n_bits)]
        self.alice_bases = [random.choice(['+', 'x']) for _ in range(self.n_bits)]
        self.bob_bases = [random.choice(['+', 'x']) for _ in range(self.n_bits)]

    def encode_and_measure(self):
        """Simulate Bob measuring Alice’s qubits."""
        self.bob_results = []
        for bit, a_basis, b_basis in zip(self.alice_bits, self.alice_bases, self.bob_bases):
            if a_basis == b_basis:
                measured_bit = bit
            else:
                measured_bit = random.randint(0, 1)  # 50% chance if bases mismatch
            self.bob_results.append(measured_bit)

    def sift_key(self):
        """Keep only bits where Alice and Bob used the same basis."""
        self.sifted_key = [
            a_bit for a_bit, a_basis, b_basis, b_bit
            in zip(self.alice_bits, self.alice_bases, self.bob_bases, self.bob_results)
            if a_basis == b_basis
        ]
        return self.sifted_key

    def run_protocol(self):
        """Run full BB84 protocol simulation (generate, measure, sift)."""
        self.generate_random_bits_and_bases()
        self.encode_and_measure()
        return self.sift_key()

    def run(self):
        """Standardized run method for main.py. Returns sifted key."""
        return self.run_protocol()


if __name__ == "__main__":
    bb84 = BB84Protocol(n_bits=16)
    key = bb84.run()
    print("Shared Secret Key:", key)
