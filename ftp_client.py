# 封装ftp客户端操作
import socket, sys, re
from logger import put_text
import time

DEBUG = True
MAX_BYTES = 1024 #最大字节

logs = ""


def client(hostName, port):   #连接服务器

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #创建对象，选择ipv4与ftp
    ip_address = socket.gethostbyname(hostName if hostName else '222.199.216.32')#得到ip
    s.connect((ip_address, port))#socket中的connect函数用于建立与远程主机的连接
#recv函数是Socket库中的一个接收数据的函数，用于从已连接的套接字中接收数据。其主要作用是等待和接收数据，直到接收到指定的字节数或者遇到指定的结束标志。
    response = s.recv(MAX_BYTES)#接收的最大长度
    if DEBUG:#如果有错误代码
        put_text(response)
    if response.decode()[:3] != "220":#解码，220代表连接就绪
        put_text("连接失败，请重试。", color="red")
        raise ("连接失败，请重试。")
    put_text("连接到服务器成功。", color="green")
    return s


def ftp_login(s, user, pwd):
    if DEBUG:
        user=user if user else 'test'
        pwd =pwd if pwd else '123456'
    userParam = b"USER " + bytes(user.encode("utf-8")) + b"\n"#用户参数，转为2进制
    pwdParam = b"PASS " + bytes(pwd.encode("utf-8")) + b"\n"

    s.send(userParam)
    response = s.recv(MAX_BYTES)#从已连接的套接字中接收数据
    if DEBUG:
        put_text(response)

    s.send(pwdParam)
    res = s.recv(MAX_BYTES)#接受回复
    if DEBUG:
        put_text(res)

    if str(res[:3].decode("utf-8")) == "230":#230为登录因特网
        put_text("登陆成功。", color="green")
        put_text("欢迎，{}".format(user), color="green")
        return True
    else:
        put_text("登陆失败，请重试。", color="red")
        raise ("登陆失败，请重试。")


def listDir(s):
    s.send(b"PASV\r\n")
    response = s.recv(MAX_BYTES)
    put_text(response)
    while response.decode()[:3] != "227":
        response = s.recv(MAX_BYTES)
        if DEBUG:
            put_text(response)

    data_response = re.findall('\((.*\))', response.decode())[0].split(")")[0]
    data_port = int(data_response.split(',')[4]) * 256 + int(data_response.split(',')[5])
    data_ip = ".".join(data_response.split(",")[0:4])

    r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    r.connect((data_ip, data_port))

    s.send(b"LIST *\r\n")
    data = b""
    while True:
        buffer = r.recv(MAX_BYTES)
        if buffer == b"":
            break
        data += buffer
    put_text(" Perms    Links Owner    Group        Size Date         Name")
    put_text(data.decode("utf-8"))
    all_info = data.decode("utf-8")
    files = all_info.split("\r\n")
    sources = []
    for i in files:
        file = i[56: len(files[0])]
        if file:
            sources.append(file)

    r.close()
    return all_info


def changeWorkingDir(s, directory):
    s.send(b"CWD " + bytes(directory.encode("utf-8")) + b"\r\n")

    response = s.recv(MAX_BYTES)
    put_text(response)
    while response.decode()[:3] != "250":
        if response.decode()[:3] == "550":
            break
        response = s.recv(MAX_BYTES)
        if DEBUG:
            put_text(response)
        put_text("回复：{}".format(response.decode("utf-8")[3:len(response)]), color="yellow")


def makeDir(s, directory):
    s.send(b"MKD " + bytes(directory.encode("utf-8")) + b"\r\n")
    put_text("输入指令 {}".format(str(b"MKD " + bytes(directory.encode("utf-8")) + b"\r\n")), color="blue")
    response = s.recv(MAX_BYTES)
    if DEBUG:
        put_text(response)
    while response.decode()[:3] != "257":
        if response.decode()[:3] == "550":
            break
        response = s.recv(MAX_BYTES)
        if DEBUG:
            put_text(response)
        put_text("回复：{}".format(response.decode("utf-8")[3:len(response)]), color="yellow")


def removeDir(s, directory):
    s.send(b"RMD " + bytes(directory.encode("utf-8")) + b"\r\n")
    put_text("输入指令 {}".format(str(b"RMD " + bytes(directory.encode("utf-8")) + b"\r\n")), color="blue")
    response = s.recv(MAX_BYTES)
    if DEBUG:
        put_text(response)
    while response.decode()[:3] != "250":
        if response.decode()[:3] == "550":
            break
        response = s.recv(MAX_BYTES)
        if DEBUG:
            put_text(response)
        put_text("回复：{}".format(response.decode("utf-8")[3:len(response)]), color="yellow")


def getFile(s, file, dstFile, pb):
    try:
        s.send(b"PASV\r\n")

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


def getPwd(s):
    s.send(b"PWD\r\n")
    response = s.recv(MAX_BYTES)
    put_text(response)
    if response.decode()[:3] != "550":
        response = s.recv(MAX_BYTES)
        if DEBUG:
            put_text(response)
        text = str(response.decode("utf-8")[4:len(response)])
        work = text.split(" ", 2)
        pwd = work[0].replace('"', '')
        put_text("回复：{}".format(pwd), color="yellow")
        return True, pwd[:-2]
    else:
        return False, "/"


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
