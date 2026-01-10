#!/usr/bin/env python3

import socket
import time
import os

# ---------- CONFIG ----------
CSV_FILE = "/home/duckweed2/DW2_LOG.csv"
HOST = "0.0.0.0"
PORT = 6000
SLEEP_TIME = 0.2
# ---------------------------


def wait_for_csv_data():
    """
    Wait until the CSV exists AND has at least one data row
    """
    print("[DW_SERVER] Waiting for DW2_LOG.csv to contain data...")
    while True:
        if os.path.exists(CSV_FILE):
            with open(CSV_FILE, "r") as f:
                lines = f.readlines()
                if len(lines) > 1:  # header + at least one row
                    print("[DW_SERVER] CSV ready")
                    return
        time.sleep(0.5)


def main():
    wait_for_csv_data()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Allow restart without "Address already in use"
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind((HOST, PORT))
    sock.listen(1)

    print(f"[DW_SERVER] Listening on {HOST}:{PORT}")
    print("[DW_SERVER] Waiting for client...")

    conn, addr = sock.accept()
    print(f"[DW_SERVER] Client connected from {addr}")

    try:
        with open(CSV_FILE, "r") as f:
            f.readline()  # skip header

            while True:
                line = f.readline()
                if line:
                    conn.sendall(line.encode("utf-8"))
                else:
                    time.sleep(SLEEP_TIME)

    except (BrokenPipeError, ConnectionResetError):
        print("[DW_SERVER] Client disconnected")

    except KeyboardInterrupt:
        print("\n[DW_SERVER] Shutting down")

    finally:
        conn.close()
        sock.close()


if __name__ == "__main__":
    main()
