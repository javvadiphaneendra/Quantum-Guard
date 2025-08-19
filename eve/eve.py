# eve/eve.py

import random
from qiskit import QuantumCircuit

class EveInterceptor:
    """
    Intercept-resend attacker for BB84.
    Eve randomly chooses a basis, measures, then re-encodes and forwards.
    """
    def __init__(self, intercept_prob=1.0):
        self.intercept_prob = intercept_prob

    def maybe_intercept(self, bit: int, alice_basis: str):
        """
        Returns (forward_bit, forward_basis, intercepted)
        - forward_bit: bit value Eve forwards to Bob (after her measurement)
        - forward_basis: basis Eve used to encode the resent qubit
        - intercepted: whether Eve actually intercepted
        """
        intercepted = random.random() < self.intercept_prob
        if not intercepted:
            # Eve does nothing; the original bit and basis propagate ideally
            return bit, alice_basis, False

        # Eve chooses a random basis and measures (conceptually)
        eve_basis = random.choice(['+', 'x'])

        # If Eve’s basis matches Alice’s, she gets the correct bit.
        # If not, she gets a random bit (50/50).
        if eve_basis == alice_basis:
            eve_measured_bit = bit
        else:
            eve_measured_bit = random.randint(0, 1)

        # Eve re-encodes using her basis and forwards that to Bob.
        return eve_measured_bit, eve_basis, True
