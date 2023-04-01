import netifaces
import socket
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED

'''局域网扫描'''


class Scanner:
    ip_list = []
    all_task = []

    @staticmethod
    def scan_tools_v1(host):
        """
        通过输入的IP地址判断服务器的控制端口是否开启
        """
        port = 21
        sk = socket.socket()
        sk.settimeout(0.1)  # 套接字超时时间为0.1秒
        conn_result = sk.connect_ex((host, port)) # 如果连接成功，则返回0；如果连接失败，则返回一个错误码
        if conn_result == 0:
            print('服务器{}的{}端口已开放'.format(host, port))
            Scanner.ip_list.append(host)
        sk.close()

    @staticmethod
    def get_gateways():
        return netifaces.gateways()['default'][netifaces.AF_INET][0] # 获取本机的网关

    @staticmethod
    def run():
        prefix = Scanner.get_gateways() # 先获取网关
        hosts = [prefix[:-1] + str(host) for host in range(1, 255)] # 获取形如222.199.216.XXX的IP
        executor = ThreadPoolExecutor(max_workers=16) # 同时执行16个线程
        Scanner.all_task = [executor.submit(Scanner.scan_tools_v1, (host)) for host in hosts]
        wait(Scanner.all_task, return_when=ALL_COMPLETED)

    @staticmethod
    def get_progress():
        total = len(Scanner.all_task)
        finish = 0
        for ele in Scanner.all_task:
            if ele.done():
                finish += 1
        return 100 if finish == total else int(finish / total)


if __name__ == '__main__':
    Scanner.run()
