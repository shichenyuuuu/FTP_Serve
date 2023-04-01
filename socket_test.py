import re
import socket
import time
from logger import put_text

DEBUG = True
MAX_BYTES = 1024


def client(hostName, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket.AF_INET表示使用ipv4；SOCK_STREAM表示使用TCP协议
    ip_address = socket.gethostbyname(hostName if hostName else '192.168.43.197')
    s.connect((ip_address, port))  # 建立连接

    response = s.recv(MAX_BYTES)  # 接收响应
    if DEBUG:
        put_text(response.decode())
    if response.decode()[:3] != "220":
        put_text("连接失败，请重试。", color="red")
        raise "连接失败，请重试。"
    put_text("连接到服务器成功。", color="green")
    return s

client("222.199.216.173",21)
