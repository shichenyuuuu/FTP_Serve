# 局域网p2p文件传输程序
## 主要实现功能
1. 友好的UI界面
2. 局域网扫描
3. 断点重续传输
4. 做种
## docker
docker run -d -v D:\test:/home/vsftpd -p 20:20 -p 21:21 -p 21100-21110:21100-21110 -e FTP_USER=test -e FTP_PASS=123456 -e PASV_ADDRESS=192.168.43.197 -e PASV_MIN_PORT=21100 -e PASV_MAX_PORT=21110 --name vsftpd --restart=always fauria/vsftpd