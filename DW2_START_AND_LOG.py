#!/usr/bin/env python3

import socket
import os
import subprocess
import time

# ---------- CONFIG ----------
DUCKWEED2_USER = "duckweed2"
DUCKWEED2_IP = "192.168.50.2"
REMOTE_DIR = "/home/duckweed2"

PORT = 6000
OUTPUT_FILE = os.path.expanduser("~/DW2_LOG.csv")
# ----------------------------


def start_remote_processes():
    """
    SSH into duckweed2 and start DW_SERVER.py and DW_MAIN.py
    """
    cmd = (
        f'ssh {DUCKWEED2_USER}@{DUCKWEED2_IP} '
        f'"cd {REMOTE_DIR} && '
        f'python3 DW_SERVER.py & '
        f'python3 DW_MAIN.py &"'
    )

    print("[DW2] Starting remote sensor + server...")
    subprocess.run(cmd, shell=True, check=True)
    print("[DW2] Remote processes started")


def start_csv_receiver():
    """
    Connect to duckweed2 and save incoming CSV stream
    """
    if not os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "w") as f:
            f.write(
                "MONTH,DAY,YR,HR,MIN,SEC,"
                "TEMP,HUMID,CO2PPM,R,G,B,NIR,THERM1,THERM2\n"
            )

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("[DW2] Connecting to CSV stream...")
    sock.connect((DUCKWEED2_IP, PORT))
    print("[DW2] Connected, logging data")

    with open(OUTPUT_FILE, "a") as out:
        while True:
            data = sock.recv(4096)
            if not data:
                break

            line = data.decode("utf-8")
            out.write(line)
            out.flush()

            print(line.strip())


def main():
    start_remote_processes()
    time.sleep(2)   # give server time to bind
    start_csv_receiver()


if __name__ == "__main__":
    main()
#name it DW2_START_AND_LOG.py

