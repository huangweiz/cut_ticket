# -*- coding: utf-8 -*-
# @Time    : 2020/9/21 17:20
# @Author  : huangwei
# @File    : client.py
# @Software: PyCharm

import os
import socket
import struct
import sys

from method1 import *


def socket_client():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 6666))
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    print(s.recv(1024).decode("utf-8"))

    while 1:
        filepath = input('please input image path: ')

        if os.path.isfile(filepath):
            fileinfo_size = struct.calcsize('128sl')

            # 定义文件头信息，包含文件名和文件大小
            fhead = struct.pack(
                '128sl',
                os.path.basename(filepath).encode(),
                os.stat(filepath).st_size
            )

            print('client filepath: {0}'.format(filepath))
            s.send(fhead)

            fp = open(filepath, 'rb')
            while 1:
                data = fp.read(1024)
                if not data:
                    print('{0} file send over...'.format(filepath))
                    break
                s.send(data)

        output_message = s.recv(1024).decode("utf-8")
        print(output_message)

        param = output_message.split(' ')

        box_num = len(param) // 5

        for i in range(box_num):
            index = 0 + i * 5
            classname = param[index]
            # 根据class name 来调用相关的截图
            points = get_ticket_point(filepath, classname)

            # 数据转换，将List 中的 str类型转换为  int 类型
            io_param = list(map(int, param[1 + i * 5:5 + i * 5]))

            # 计算出两种方法得出的 发票的位置 符合的那个点集
            point = cal_iou(io_param, points)

            # 根据符合的点集裁剪出相应的发票
            get_image(filepath, point, classname, i)

    s.close()


if __name__ == '__main__':
    socket_client()
