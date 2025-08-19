from bb84.bb84 import BB84Protocol
from bb84.bb84_eve import BB84WithEve
from utils.logger import Logger
from utils.visualize import animate_bb84   # ✅ only using animation now
import os
from datetime import datetime

logger = Logger()


def save_key(key_bits, label="clean"):
    """
    Save sifted key into /keys folder
    Each run gets a timestamped file.
    """
    os.makedirs("keys", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"keys/{label}_key_{timestamp}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("".join(map(str, key_bits)))
    logger.log(f"Key saved: {filename}")
    return filename


def run_clean(n_bits=128):
    """
    Run BB84 without Eve
    """
    bb = BB84Protocol(n_bits=n_bits)
    key = bb.run()  # calls the run() method
    logger.log("=== CLEAN CHANNEL (No Eve) ===")
    logger.log(f"Sifted length: {len(key)}")
    logger.log("Expected QBER ~ 0 (aside from simulator noise)")
    save_key(key, "clean")
    return key


def run_with_eve(n_bits=128, alert_threshold=0.11):
    """
    Run BB84 with Eve (Intercept-Resend attack)
    """
    bbE = BB84WithEve(n_bits=n_bits, alert_threshold=alert_threshold)
    stats = bbE.run()  # returns dict with {sift_len, qber, alert, key}
    logger.log("\n=== WITH EVE (Intercept-Resend) ===")
    logger.log(f"Sifted length: {stats['sift_len']}")
    logger.log(f"QBER: {stats['qber']:.3f}")
    logger.log(f"Eavesdropping Detected? {'YES' if stats['alert'] else 'NO'}")
    save_key(stats["key"], "eve")
    return stats


if __name__ == "__main__":
    # Run simulations
    clean_key = run_clean(n_bits=100)
    stats = run_with_eve(n_bits=100, alert_threshold=0.11)

    # Show animated BB84 diagram (side-by-side clean vs Eve case)
    # If save=True → saves GIF in /keys folder
    animate_bb84(qber=stats["qber"], save=True)
