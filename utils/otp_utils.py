import hashlib
import random
import json
import datetime
import pyotp
import socket
from IPy import IP


def get_client_ip(sign_up_ip, x_real_ip):
    if sign_up_ip:
        possible_ips = sign_up_ip.split(',')[:10]
        for sign_up_ip in possible_ips:
            sign_up_ip = sign_up_ip.strip()
            if ip_validator(sign_up_ip) and public_ip_check(sign_up_ip):
                return sign_up_ip
    return x_real_ip


def ip_validator(addr):
    try:
        socket.inet_aton(addr)
        return addr.count('.') == 3
    except socket.error:
        return False


def public_ip_check(addr):
    if IP(addr).iptype() == 'PUBLIC':
        return True
    return False


def get_random_otp():
    return pyotp.HOTP(pyotp.random_base32(), digits=4).at(0)
