# -*- coding: utf-8 -*-
# @Time    : 2020/9/22 10:39
# @Author  : huangwei
# @File    : method3.py
# @Software: PyCharm
import cv2

from method2 import *


def get_code_contours(contours, hierarchy):
    ic = 0
    temp_contours = []

    for i in range(len(contours)):
        '''从所有的轮廓中找出为二维码定位块的轮廓放入temp_contours中'''
        temp_hierarchy = hierarchy[0][i]

        if temp_hierarchy[2] == -1:
            ic = 0
        else:
            ic += 1

        if ic >= 2:
            # 得到的是倒数第二层的轮廓，且图片最外层算一层
            sub_contour = contours[temp_hierarchy[2]]
            sub_area = cv2.contourArea(sub_contour)

            if sub_area < 200 and decide(sub_contour):
                area = cv2.contourArea(contours[i])

                if sub_area < area < 400 and decide(contours[i]):
                    up_contour = contours[temp_hierarchy[3]]
                    up_area = cv2.contourArea(up_contour)

                    if area < up_area < 800 and decide(up_contour):
                        temp_contours.append(up_contour)

    return temp_contours


def get_pointset(temp_contours):
    num_temp = len(temp_contours)
    pointSet = []

    for i in range(num_temp):
        '''给轮廓分组和找出对应位置'''
        sub_set = []

        if temp_contours[i] is not None:
            '''返回一个rect 对象，rect[0] 返回矩形的中心点，rect[1] 返回矩形的长和宽，rect[2] 返回矩形的旋转角度'''
            rect = cv2.minAreaRect(temp_contours[i])
            centerPoint = rect[0]
            rect_width = rect[1][0]
            # print("rect", rect_width)

            arr_length = []

            for j in range(num_temp):
                if temp_contours[j] is not None:
                    nextPoint = cv2.minAreaRect(temp_contours[j])[0]

                    point_length = cal_length(centerPoint, nextPoint)
                    # print("point length:", point_length)

                    # 二维码的大小
                    if rect_width * 2 < point_length < rect_width * 6:
                        arr_length.append(point_length)
                    else:
                        arr_length.append(0)
                else:
                    arr_length.append(0)

            # print("point:", arr_length)

            # 找出arr length相同的点
            for j in range(num_temp):
                if arr_length[j] != 0:
                    for k in range(j + 1, num_temp):
                        if arr_length[k] != 0:
                            tolerance = arr_length[j] * 0.2
                            delta = arr_length[j] - arr_length[k]

                            if abs(delta) < tolerance:
                                # 判断垂直
                                j_point = cv2.minAreaRect(temp_contours[j])[0]
                                k_point = cv2.minAreaRect(temp_contours[k])[0]

                                tan1 = get_tan(centerPoint, j_point)
                                tan2 = get_tan(centerPoint, k_point)

                                if abs(tan1) > 10 or abs(tan2) > 10:
                                    if abs(tan1) < 0.1 or abs(tan2) < 0.1:
                                        tan = 1
                                else:
                                    tan = abs(tan1 * tan2)

                                if abs(tan - 1) < 0.1:
                                    # 垂直判断朝向
                                    sub_set.append(centerPoint)

                                    # 求j点绕center点顺时针旋转90度后的点x 的坐标
                                    jx = centerPoint[0] - (j_point[1] - centerPoint[1])
                                    jy = centerPoint[1] + (j_point[0] - centerPoint[0])

                                    new_point = (jx, jy)

                                    new_length = cal_length(new_point, k_point)

                                    if new_length < tolerance:
                                        sub_set.append(j_point)
                                        sub_set.append(k_point)
                                    else:
                                        sub_set.append(k_point)
                                        sub_set.append(j_point)

                                    temp_contours[i] = None
                                    temp_contours[j] = None
                                    temp_contours[k] = None

            if sub_set:
                pointSet.append(sub_set)

    return pointSet


def get_point(filepath, classname):
    image = cv2.imread(filepath)

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if classname == 'train-ticket':
        # 返回的第一个参数为得到的阈值值
        _, threshold_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        # 返回的第一个参数为二值图
        # 第二个参数为list结构，列表中的每个元素 node 代表一个边沿信息，是一个(num, 1, 2)的三维向量
        # num 表示该条边沿里共有多少个像素点， 2 表示每个点的横纵坐标
        # 第三个参数为 (1, x, 4) 的数组，x表示共有多少个像素点， 4 表示 后、前、子、父轮廓的编号
        _, contours, hierarchy = cv2.findContours(threshold_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    elif classname == 'zeng-ticket':
        _, threshold_image = cv2.threshold(gray_image, 110, 255, cv2.THRESH_BINARY)
        _, contours, hierarchy = cv2.findContours(threshold_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    elif classname == 'sd-ticket':
        _, threshold_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        _, contours, hierarchy = cv2.findContours(threshold_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)



    # cv2.drawContours(image, contours, -1, (0, 255, 0), 1)
    # cv2.imshow("image", image)
    # cv2.waitKey(0)

    temp_contours = get_code_contours(contours, hierarchy)
    pointSet = get_pointset(temp_contours)

    return pointSet
