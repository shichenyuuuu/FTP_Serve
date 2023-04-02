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


# 登录
def ftp_login(s, user, pwd):
    if DEBUG:
        user = user if user else 'test'
        pwd = pwd if pwd else '123456'
    # b表示字节串对象，字符串需要使用encode转换为字节串对象
    userParam = b"USER " + bytes(user.encode("utf-8")) + b"\n"  # 字节串序列，不是字符串
    pwdParam = b"PASS " + bytes(pwd.encode("utf-8")) + b"\n"

    s.send(userParam)
    response = s.recv(MAX_BYTES)
    if DEBUG:
        put_text(response) # 331 Password required for user
    s.send(pwdParam)
    res = s.recv(MAX_BYTES)
    if DEBUG:
        put_text(res)
    if str(res[:3].decode("utf-8")) == "230": # 230 Logged on
        put_text("登陆成功。", color="green")
        put_text("欢迎，{}".format(user), color="green")
        return True
    else:
        put_text("登陆失败，请重试。", color="red")
        raise "登陆失败，请重试。"

# 下载文件
def getFile(s, file, dstFile, pb):
    '''

    '''
    try:
        s.send(b"PASV\r\n")  # 被动模式

        response = s.recv(MAX_BYTES)
        if DEBUG:
            put_text(response, "noshow")
        while response.decode()[:3] != "227":
            response = s.recv(MAX_BYTES)
            if DEBUG:
                put_text(response, "noshow")
            put_text("回复：{}".format(response.decode("utf-8")[3:len(response)]), "noshow")

        data_response = re.search("\((.*?)\)", response.decode()).group(1)
        data_ip = ".".join(data_response.split(",")[0:4])
        data_port = int(data_response.split(',')[4]) * 256 + int(data_response.split(',')[5])

        # 获取服务器返回的数据端口，并建立连接
        r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        r.connect((data_ip, data_port))

        s.send(b"RETR " + bytes(file.encode("utf-8")) + b"\r\n")

        response = s.recv(MAX_BYTES)
        if DEBUG:
            put_text(response, "noshow")
        put_text("回复：{}".format(response.decode("utf-8")[3:len(response)]), "noshow")

        if response.decode()[:3] != "550":
            outputFile = str(dstFile)

            output_file = open(outputFile, "wb")
            put_text("这将花费一段时间", "noshow")
            while True:
                buffer = r.recv(1024)
                if buffer == b"":
                    break
                pb.updateProgress.emit(buffer)
                output_file.write(buffer)
            response = s.recv(MAX_BYTES)
            if DEBUG:
                put_text(response, "noshow")
            text = response.decode("utf-8")[4:len(response)]
            if text == "Transfer complete.\r\n":
                time.sleep(0.1)
                pb.setValues.emit()
            put_text("回复：{}".format(text), "noshow")
    except Exception as e:
        print(str(e))



# 上传文件
def uploadFile(s, srcfile, dstfile, pb):
    s.send(b"PASV\r\n")

    response = s.recv(MAX_BYTES)
    put_text(response, "noshow")
    while response.decode()[:3] != "227":
        response = s.recv(MAX_BYTES)
        if DEBUG:
            put_text(response, "noshow")
        put_text("回复：{}".format(response.decode("utf-8")[3:len(response)]), "noshow")

    data_response = re.search("\((.*?)\)", response.decode()).group(1)
    data_ip = ".".join(data_response.split(",")[0:4])
    data_port = int(data_response.split(',')[4]) * 256 + int(data_response.split(',')[5])

    r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    r.connect((data_ip, data_port))

    s.send(b"STOR " + bytes(dstfile.encode("utf-8")) + b"\r\n")

    # Open the file and send it to server
    output_file = open(srcfile, "rb")
    while True:
        buffer = output_file.read(MAX_BYTES)
        r.sendall(buffer)
        print(buffer)
        pb.updateProgress.emit(buffer)
        if buffer == b'':
            break
    put_text("文件已上传", "noshow")


# 删除文件
def deleteFile(s, file):
    s.send(b"PASV\r\n")

    response = s.recv(MAX_BYTES)
    if DEBUG:
        put_text(response)
    while response.decode()[:3] != "227":
        response = s.recv(MAX_BYTES)
        if DEBUG:
            put_text(response)
        put_text("回复：{}".format(response.decode("utf-8")[3:len(response)]), color="yellow")

    data_response = re.search("\((.*?)\)", response.decode()).group(1)
    data_ip = ".".join(data_response.split(",")[0:4])
    data_port = int(data_response.split(',')[4]) * 256 + int(data_response.split(',')[5])

    r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    r.connect((data_ip, data_port))

    s.send(b"DELE " + bytes(file.encode("utf-8")) + b"\r\n")
    put_text("文件已删除")

ftp_login(client("222.199.216.173", 21),"user","123456")
