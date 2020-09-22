# -*- coding: utf-8 -*-
# @Time    : 2020/9/21 17:23
# @Author  : huangwei
# @File    : method2.py
# @Software: PyCharm

import cv2
import math


def decide(contour):
    """判断外接矩形长宽比例是否符合"""

    rect = cv2.minAreaRect(contour)
    width, height = rect[1]
    ratio = width / height

    if 0.5 < ratio < 2:
        return True
    else:
        return False


def cal_length(centerPoint, nextPoint):
    temp_x = centerPoint[0] - nextPoint[0]
    temp_y = centerPoint[1] - nextPoint[1]

    length = math.sqrt((temp_x ** 2) + (temp_y ** 2))

    return length


def get_tan(point1, point2):
    tan_x = point1[0] - point2[0]
    tan_y = point1[1] - point2[1]

    if tan_x == 0:
        tan = 10000
    else:
        tan = tan_y / tan_x

    return tan


def train_rect_points(points):
    right_y = (points[1][1] - points[0][1]) * 1.6 + points[0][1]
    right_x = (points[1][0] - points[0][0]) * 1.6 + points[0][0]

    left_y = (points[0][1] - points[1][1]) * 7 + points[1][1]
    left_x = (points[0][0] - points[1][0]) * 7 + points[1][0]

    up_y = (points[0][1] - points[2][1]) * 4 + points[2][1]
    up_x = (points[0][0] - points[2][0]) * 4 + points[2][0]

    down_y = (points[2][1] - points[0][1]) * 1.7 + points[0][1]
    down_x = (points[2][0] - points[0][0]) * 1.7 + points[0][0]

    if up_x - down_x == 0:
        x1 = left_x
        y1 = up_y

        x2 = right_x
        y2 = up_y

        x3 = left_x
        y3 = down_y

        x4 = right_x
        y4 = down_y

    elif right_x - left_x == 0:
        x1 = up_x
        y1 = left_y

        x2 = up_x
        y2 = right_y

        x3 = down_x
        y3 = left_y

        x4 = down_x
        y4 = right_y
    else:
        k1 = (up_y - down_y) / (up_x - down_x)
        k2 = (right_y - left_y) / (right_x - left_x)

        x1 = (k1 * left_x - left_y - k2 * up_x + up_y) / (k1 - k2)
        y1 = k1 * (x1 - left_x) + left_y

        x2 = (k1 * right_x - right_y - k2 * up_x + up_y) / (k1 - k2)
        y2 = k1 * (x2 - right_x) + right_y

        x3 = (k1 * left_x - left_y - k2 * down_x + down_y) / (k1 - k2)
        y3 = k1 * (x3 - left_x) + left_y

        x4 = (k1 * right_x - right_y - k2 * down_x + down_y) / (k1 - k2)
        y4 = k1 * (x4 - right_x) + right_y

    point1 = (int(x1), int(y1))
    point2 = (int(x2), int(y2))
    point3 = (int(x3), int(y3))
    point4 = (int(x4), int(y4))

    new_point = [point1, point2, point3, point4]

    return new_point


def canyin_rect_points(points):
    right_y = (points[0][1] - points[2][1]) * 6.5 + points[2][1]
    right_x = (points[0][0] - points[2][0]) * 6.5 + points[2][0]

    left_y = (points[2][1] - points[0][1]) * 2.5 + points[0][1]
    left_x = (points[2][0] - points[0][0]) * 2.5 + points[0][0]

    up_y = (points[0][1] - points[1][1]) * 17 + points[1][1]
    up_x = (points[0][0] - points[1][0]) * 17 + points[1][0]

    down_y = (points[1][1] - points[0][1]) * 2 + points[0][1]
    down_x = (points[1][0] - points[0][0]) * 2 + points[0][0]

    if up_x - down_x == 0:
        x1 = left_x
        y1 = up_y

        x2 = right_x
        y2 = up_y

        x3 = left_x
        y3 = down_y

        x4 = right_x
        y4 = down_y

    elif right_x - left_x == 0:
        x1 = up_x
        y1 = left_y

        x2 = up_x
        y2 = right_y

        x3 = down_x
        y3 = left_y

        x4 = down_x
        y4 = right_y
    else:
        k1 = (up_y - down_y) / (up_x - down_x)
        k2 = (right_y - left_y) / (right_x - left_x)

        x1 = (k1 * left_x - left_y - k2 * up_x + up_y) / (k1 - k2)
        y1 = k1 * (x1 - left_x) + left_y

        x2 = (k1 * right_x - right_y - k2 * up_x + up_y) / (k1 - k2)
        y2 = k1 * (x2 - right_x) + right_y

        x3 = (k1 * left_x - left_y - k2 * down_x + down_y) / (k1 - k2)
        y3 = k1 * (x3 - left_x) + left_y

        x4 = (k1 * right_x - right_y - k2 * down_x + down_y) / (k1 - k2)
        y4 = k1 * (x4 - right_x) + right_y

    point1 = (int(x1), int(y1))
    point2 = (int(x2), int(y2))
    point3 = (int(x3), int(y3))
    point4 = (int(x4), int(y4))

    new_point = [point1, point2, point3, point4]

    return new_point


def get_center(point):
    c_x = (point[0][0] + point[1][0] + point[2][0] + point[3][0]) / 4
    c_y = (point[0][1] + point[1][1] + point[2][1] + point[3][1]) / 4
    center_point = (c_x, c_y)
    return center_point


def get_angle(point):
    d_x = point[0][0] - point[1][0]
    d_y = point[0][1] - point[1][1]

    if d_x == 0:
        if d_y > 0:
            roll_angle = -90
        else:
            roll_angle = 90
    else:
        roll_angle = math.degrees(math.atan(d_y / d_x))
        if d_x > 0:
            roll_angle += 180

    return roll_angle
