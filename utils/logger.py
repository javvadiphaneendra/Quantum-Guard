# utils/logger.py
import os
from datetime import datetime

class Logger:
    def __init__(self, logfile="logs.txt"):
        self.logfile = logfile

    def log(self, message):
        from datetime import datetime
        log_message = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}"
        print(log_message)
        with open(self.logfile, "a", encoding="utf-8") as f:   # ✅ added encoding
            f.write(log_message + "\n")
