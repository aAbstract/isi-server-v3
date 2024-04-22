import os
import socket
import colorama
import subprocess


def print_err_log(msg: str):
    err_tag = f"{colorama.Fore.RED}[ERROR]{colorama.Style.RESET_ALL}"
    print(f"{err_tag}: {msg}")


def is_port_open(host: str, port: int) -> bool:
    try:
        _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _socket.settimeout(2)
        _socket.connect((host, port))
        return True
    except:
        return False
    finally:
        _socket.close()
