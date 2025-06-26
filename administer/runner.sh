#!/bin/bash
set -e

if [[ -z "$1" ]]; then
  echo "❌ Error: You must provide an argument: 'beat' or 'celery'"
  exit 1
fi

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

wait_for_port("cf_lib_web", 80)
END

case "$1" in
  beat)
    celery -A library_system beat -l info
    ;;
  celery)
    celery -A library_system worker -l info
    ;;
  *)
    echo "❌ Invalid argument: '$1'. Use 'beat' or 'celery'"
    exit 1
    ;;
esac
