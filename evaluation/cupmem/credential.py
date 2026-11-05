"""Deliver credentials over SSH stdin to a private socket inside the allocation.

No credential files, command-line secrets, Slurm exported secrets, or login-node
Python are used. Both receiver and delivery helper execute on the compute node.
"""
import json
import os
from pathlib import Path
import resource
import socket
import struct
import sys


def socket_path(job):
    if not str(job).isdigit():
        raise ValueError("Invalid job ID")
    return Path("/tmp") / ("cupmem-" + str(os.getuid()) + "-" + str(job)) / "credential.sock"


def receive(job, timeout=180):
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    path = socket_path(job)
    path.parent.mkdir(mode=0o700)  # Existing path is an error, never reuse.
    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        server.bind(str(path))
        os.chmod(path, 0o600)
        server.listen(1)
        server.settimeout(timeout)
        print("credential_receiver_ready", str(job), flush=True)
        connection, _ = server.accept()
        with connection:
            connection.settimeout(10)
            _, uid, _ = struct.unpack("3i", connection.getsockopt(socket.SOL_SOCKET, socket.SO_PEERCRED, 12))
            if uid != os.getuid():
                raise PermissionError("Credential peer UID mismatch")
            pieces = []
            while True:
                piece = connection.recv(1024)
                if not piece:
                    break
                pieces.append(piece)
                if sum(map(len, pieces)) > 8192:
                    raise ValueError("Credential payload too large")
            data = json.loads(b"".join(pieces))
            if set(data) != {"api_key"} or not isinstance(data["api_key"], str) or not data["api_key"]:
                raise ValueError("Invalid credential payload")
            return data["api_key"]
    finally:
        server.close()
        if path.exists():
            path.unlink()
        path.parent.rmdir()


def deliver(job):
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    raw = sys.stdin.buffer.read(8193)
    if not raw or len(raw) > 8192:
        raise ValueError("Invalid credential payload size")
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
        client.connect(str(socket_path(job)))
        client.sendall(raw)
        client.shutdown(socket.SHUT_WR)
    print("credential_delivered", str(job), flush=True)


if __name__ == "__main__":
    deliver(sys.argv[1])
