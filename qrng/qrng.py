# qrng.py

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

class QuantumRandomGenerator:
    def __init__(self):
        """Initialize QRNG with Aer simulator backend."""
        self.backend = AerSimulator()

    def get_bit(self):
        """Return a single quantum random bit (0 or 1)."""
        qc = QuantumCircuit(1, 1)
        qc.h(0)                # Hadamard → superposition
        qc.measure(0, 0)
        result = self.backend.run(qc, shots=1).result()
        counts = result.get_counts()
        return int(max(counts, key=counts.get))

    def get_bits(self, n=8):
        """Return a list of n quantum random bits."""
        return [self.get_bit() for _ in range(n)]

    def get_int(self, n=8):
        """Return a random integer generated from n quantum bits."""
        bits = self.get_bits(n)
        return int("".join(str(b) for b in bits), 2)

    def generate(self, num_bits=16):
        """Return a string of num_bits random quantum bits."""
        return "".join(str(self.get_bit()) for _ in range(num_bits))


if __name__ == "__main__":
    qrng = QuantumRandomGenerator()
    print("Random bit:", qrng.get_bit())
    print("Random 8 bits:", qrng.get_bits(8))
    print("Random integer (8 bits):", qrng.get_int(8))
    print("Random 16-bit string:", qrng.generate(16))
