**QuantumGuard: BB84 Quantum Key Distribution Simulator**

---

## 1. Project Overview

**Problem Statement:** Develop a BB84-based simulator to demonstrate secure communication using quantum principles.

**Objectives:**

* Demonstrate secure key exchange between Alice and Bob.
* Detect eavesdropping using Quantum Bit Error Rate (QBER).
* Enable secure message encryption/decryption using the generated key.

**Real-world Significance:**

* Educational tool for quantum cryptography.
* Prototype for secure messaging applications.

---

## 2. System Architecture

**BB84 Protocol Simulation:**

* Alice generates random bits and bases.
* Bob generates random bases.
* Qubits are simulated; measurement outcomes are probabilistic.
* Sifted key is created where bases match.
* QBER is calculated to detect eavesdropping.

**QRNG Usage:**

* Quantum Random Number Generator simulator produces bits for Alice and Bob.
* Ensures high entropy and unpredictability.

**Message Encryption/Decryption Flow:**

1. Alice generates a message.
2. Encrypts the message using XOR with the shared BB84 key.
3. Sends encrypted message to Bob.
4. Bob decrypts message using shared key.

**Diagrams:**

* Clean channel: Alice → Bob (smooth line)
* Attacked channel: Alice → Eve → Bob (zigzag line)
* QBER values displayed side-by-side (e.g., 0% vs 23%).

---

## 3. Folder Structure & File Descriptions

```
QuantumGuard/
│
├─ bb84/
│   ├─ bb84.py               # BB84 protocol simulator
│   └─ bb84_eve.py           # BB84 with Eve interception
│
├─ eve/
│   └─ eve.py                # Eve interceptor class
│
├─ qrng/
│   └─ qrng.py               # Quantum Random Number Generator simulator
│
├─ utils/
│   ├─ logger.py             # Logging utility
│   └─ visualize.py          # Visualization functions
│
├─ send_message.py           # Script to send encrypted message
├─ receive_message.py        # Script to receive and decrypt message
├─ main.py                   # Runs clean and Eve simulations
├─ requirements.txt          # Python dependencies
└─ README.md
```

---

## 4. Code Listing

### bb84.py

```python
# Code for BB84Protocol class here (full corrected version)
```

### bb84\_eve.py

```python
# Code for BB84WithEve class here (full corrected version)
```

### eve.py

```python
# EveInterceptor class here
```

### qrng.py

```python
# QuantumRandomGenerator class here
```

### logger.py

```python
# Logger class here
```

### visualize.py

```python
# Functions for visualize_bb84() and animate_bb84()
```

### send\_message.py

```python
# Send message script using BB84-generated key
```

### receive\_message.py

```python
# Receive and decrypt message using BB84-generated key
```

---

## 5. Installation & Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/QuantumGuard.git
cd QuantumGuard
```

2. Create Python virtual environment:

```bash
python -m venv quantumguard-env
```

3. Activate environment:

* Windows: `quantumguard-env\Scripts\activate`
* Linux/Mac: `source quantumguard-env/bin/activate`

4. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 6. Usage Instructions

### Run BB84 Simulation

```bash
python main.py
```

### Send a Message

```bash
python send_message.py
```

### Receive a Message

```bash
python receive_message.py
```

### Visualization

```python
from utils.visualize import visualize_bb84, animate_bb84
visualize_bb84(qber)
animate_bb84(qber, save=True)
```

---

## 7. Results

* Sample shared keys generated for clean and attacked channels.
* Messages encrypted and decrypted successfully.
* Diagrams show key exchange and eavesdropping detection.

---

## 8. Future Work

* Integrate IBM Quantum hardware for real qubit key generation.
* Multi-user BB84 simulation over network sockets.
* Web interface using Flask, HTML/CSS/JS.

---

## 9. References

* [BB84 Protocol](https://en.wikipedia.org/wiki/BB84)
* [Qiskit Documentation](https://qiskit.org/documentation/)
* Quantum cryptography papers and tutorials

---

## License

MIT License © \[Javvadi Phaneendra]
