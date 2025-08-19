# bb84_eve.py

import random
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qrng.qrng import QuantumRandomGenerator
from eve.eve import EveInterceptor

class BB84WithEve:
    def __init__(self, n_bits=128, intercept_prob=1.0, alert_threshold=0.11):
        self.n_bits = n_bits
        self.alert_threshold = alert_threshold
        self.backend = AerSimulator()
        self.qrng = QuantumRandomGenerator()

        # Initialize all attributes
        self.alice_bits = []
        self.alice_bases = []
        self.bob_bases = []
        self.bob_results = []
        self.sifted_alice = []
        self.sifted_bob = []
        self.intercept_flags = []

        # Eve interceptor
        self.eve = EveInterceptor(intercept_prob=intercept_prob)

    def generate_random_bits_and_bases(self):
        """Generate Alice and Bob bits and bases."""
        self.alice_bits = [self.qrng.get_bit() for _ in range(self.n_bits)]
        self.alice_bases = [random.choice(['+', 'x']) for _ in range(self.n_bits)]
        self.bob_bases = [random.choice(['+', 'x']) for _ in range(self.n_bits)]

    def transmit_with_eve(self):
        """Alice encodes -> Eve maybe intercepts & resends -> Bob measures."""
        self.bob_results = []
        self.intercept_flags = []

        for a_bit, a_basis, b_basis in zip(self.alice_bits, self.alice_bases, self.bob_bases):
            fwd_bit, fwd_basis, intercepted = self.eve.maybe_intercept(a_bit, a_basis)
            self.intercept_flags.append(intercepted)

            # Build Bob’s measurement circuit on the forwarded qubit
            qc = QuantumCircuit(1, 1)
            # Encode forwarded bit
            if fwd_bit == 1:
                qc.x(0)
            if fwd_basis == 'x':
                qc.h(0)
            # Bob measures in his basis
            if b_basis == 'x':
                qc.h(0)
            qc.measure(0, 0)

            compiled = transpile(qc, self.backend)
            job = self.backend.run(compiled, shots=1)
            result = job.result()
            counts = result.get_counts()
            bob_bit = int(list(counts.keys())[0])
            self.bob_results.append(bob_bit)

    def sift_key(self):
        """Keep only bits where Alice and Bob used the same basis."""
        self.sifted_alice = []
        self.sifted_bob = []

        for i in range(self.n_bits):
            if self.alice_bases[i] == self.bob_bases[i]:
                self.sifted_alice.append(self.alice_bits[i])
                self.sifted_bob.append(self.bob_results[i])

    def compute_qber(self):
        """Quantum Bit Error Rate on sifted bits."""
        if not self.sifted_alice:
            return 0.0
        errors = sum(1 for a, b in zip(self.sifted_alice, self.sifted_bob) if a != b)
        return errors / len(self.sifted_alice)

    def run(self):
        """Run BB84 protocol with Eve interception."""
        self.generate_random_bits_and_bases()
        self.transmit_with_eve()
        self.sift_key()
        qber_val = self.compute_qber()
        alert = qber_val > self.alert_threshold

        # Return dictionary compatible with main.py
        return {
            "key": self.sifted_bob,
            "sift_len": len(self.sifted_bob),
            "qber": qber_val,
            "alert": alert
        }


if __name__ == "__main__":
    bb84e = BB84WithEve(n_bits=128, intercept_prob=1.0, alert_threshold=0.11)
    stats = bb84e.run()
    print(f"Sifted length: {stats['sift_len']}")
    print(f"QBER: {stats['qber']:.3f}")
    print(f"Eavesdropping Detected? {'YES' if stats['alert'] else 'NO'}")
    print("Shared Key (Bob’s view):", stats["key"])
