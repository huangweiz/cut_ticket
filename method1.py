# -*- coding: utf-8 -*-
# @Time    : 2020/9/21 17:21
# @Author  : huangwei
# @File    : method1.py
# @Software: PyCharm
import operator
import numpy as np
from method3 import *


def get_ticket_point(filepath, classname):
    pointSet = get_point(filepath, classname)

    goal_points = []

    for points in pointSet:
        if points[0] is not None:
            '''根据二维码三个顶点求发票的四个顶点'''
            if classname == "train-ticket":
                rect_point = train_rect_points(points)
            elif classname == "zeng-ticket":
                rect_point = canyin_rect_points(points)
            goal_points.append(rect_point)

    return goal_points


def cal_iou(param, points):
    """
    这里可以调节两种方法得到的 点集之后  根据什么来判断 比较符合的点集
    1. 两个面积比在一定范围
    2. 中心点距离最小的一个且距离小于某个值
    :param param:
    :param points:
    :return:
    """
    p_x = (param[0] + param[2]) / 2
    p_y = (param[1] + param[3]) / 2
    p_w = param[2] - param[0]
    p_h = param[3] - param[1]

    p_center = (p_x, p_y)
    p_area = p_w * p_h

    all_distance = []

    for point in points:
        c_w = cal_length(point[0], point[1])
        c_h = cal_length(point[0], point[2])

        c_center = get_center(point)
        distance = cal_length(p_center, c_center)

        c_area = c_w * c_h
        ratio = p_area / c_area
        if 0.5 < ratio < 2:
            all_distance.append(distance)

    min_index, min_distance = min(enumerate(all_distance), key=operator.itemgetter(1))

    if min_distance < (p_w + p_h) / 2:
        return points[min_index]


def get_image(filepath, point, classname, i):
    image = cv2.imread(filepath)

    print(filepath)

    box = np.array([point[0], point[1], point[3], point[2]], dtype="float32")

    w, h = int(cal_length(point[0], point[1])), int(cal_length(point[0], point[2]))

    dst_rect = np.array([
        [0, 0],
        [w + 1, 0],
        [w + 1, h + 1],
        [0, h + 1]
    ], dtype="float32")

    # print("box:\n", box)
    # print("dst:\n", dst_rect)

    m = cv2.getPerspectiveTransform(box, dst_rect)

    print("w:", w, h)

    warp_image = cv2.warpPerspective(image, m, (w, h))

    """
    
    根据传入的文件名进行命名
    
    
    """
    new_path = "./output/%s%d.png" % (classname, i)
    print(new_path)
    cv2.imwrite(new_path, warp_image, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])

    cv2.waitKey(0)
