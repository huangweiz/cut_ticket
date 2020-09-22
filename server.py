# -*- coding: utf-8 -*-
# @Time    : 2020/9/21 17:06
# @Author  : huangwei
# @File    : server.py
# @Software: PyCharm

import os
import socket
import struct
import threading
import sys
import cv2
from input import YoloTest

# 运行模型
init = YoloTest()


def socket_service():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 防止socket server重启后端口被占用（socket.error: [Errno 98] Address already in use）
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('127.0.0.1', 6666))
        s.listen(10)
    except socket.error as msg:
        print(msg)
        sys.exit(1)

    print('Waiting connection...')

    while 1:
        conn, addr = s.accept()
        t = threading.Thread(target=deal_data, args=(conn, addr))
        t.start()


def deal_data(conn, addr):
    print('Accept new connection from {0}'.format(addr))
    conn.send('Hi, Welcome to the server!'.encode("utf-8"))

    while 1:
        fileinfo_size = struct.calcsize('128sl')
        buf = conn.recv(fileinfo_size)
        if buf:
            filename, filesize = struct.unpack('128sl', buf)
            fn = filename.strip(b"\x00").decode("utf-8")
            new_filename = os.path.join('./', 'new_' + fn)
            print(new_filename, filesize)
            print('file new name is {0}, filesize if {1}'.format(new_filename, filesize))

            recvd_size = 0  # 定义已接收文件的大小
            fp = open(new_filename, 'wb')
            print('start receiving...')

            while not recvd_size == filesize:
                if filesize - recvd_size > 1024:
                    data = conn.recv(1024)
                    recvd_size += len(data)
                else:
                    data = conn.recv(filesize - recvd_size)
                    recvd_size = filesize
                fp.write(data)

            fp.close()
            image = cv2.imread(new_filename)
            infos = init.evaluate(image)

            # 将infos 中的 name 读出来
            info_arr = infos.split(' ')

            print('end receive...')
        conn.send(infos.encode("utf-8"))

    conn.close()


if __name__ == '__main__':
    socket_service()
