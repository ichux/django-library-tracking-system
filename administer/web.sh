#!/bin/bash
set -e

python3 <<END
import socket
import time


def wait_for_port(host, port, timeout=1):
    print(f"⏳ Waiting for {host}:{port} to become available...")
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            try:
                sock.connect((host, port))
                print(f"✅ Connected to {host}:{port}")
                return
            except (socket.timeout, ConnectionRefusedError):
                time.sleep(1)


wait_for_port("cf_lib_redis", 6379)
wait_for_port("cf_lib_db", 5432)
END

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:80
