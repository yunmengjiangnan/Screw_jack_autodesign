# -*- coding = utf-8 -*-
# @Time : 2021/12/3 20:15
# @Author : xzh
# @File : 螺旋千斤顶自动化设计系统v1.0.py
# @Software: PyCharm

import math
from math import pi

# 螺纹的牙型
# #选用矩形螺纹，采用内径对中，配合选H8/h8，在计算强度时不考虑螺纹的径向间隙。

# 螺杆的材料
# #选用45钢

# 螺杆的直径与自锁验算
# #输入设计原始数据
F = 20  # 最大起重量（KN）
H = 150  # 最大起升高度（mm）
sigma_s = 353  # 45号钢屈服极限（MPa）
S = 3  # 安全系数
alpha = 0  # (°)
mu = 0.10  # (0.08 ~ 0.10)
n = 1  # 螺纹条数
# #录入国家标准推荐螺距与直径
P_list = (2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 40, 48)
P_and_d_first_list = {'2': (10, 12, 16, 20, 26),
                      '3': (10, 12, 32, 40, 50, 60),
                      '4': (16, 20, 80),
                      '5': (26, 100),
                      '6': (32, 40, 120),
                      '8': (50, 60),
                      '10': (32, 40, 80, 200),
                      '12': (50, 60, 100, 250, 320, 400),
                      '16': (80, 120, 160, 500)}

# #变量初始化
phi = 0
rho_ = 0
number_of_attempts = 0

# #计算过程
sigma_agree = round(sigma_s / S)  # 求许用应力sigma
d1_min = pow((4 * 1.3 * F * 1000) / (pi * sigma_agree), 0.5)  # 求螺纹内经最小值d1_min
P_float = d1_min / 4
# P = math.ceil(P_float)
for P in P_list:
    if P > P_float:
        h = P / 2
        d_float = d1_min + P
        for d in P_and_d_first_list[str(P)]:
            d1 = d - P
            # 自锁验算
            rho_ = math.atan(mu / math.cos(alpha / 2)) * 180 / pi
            d2 = (d1 + d) / 2
            phi = math.atan((n * P) / (pi * d2)) * 180 / pi
            if phi <= rho_ - 1:
                print('最大起重量F = ', F, 'KN')
                print('最大升起高度H = ', 'mm')
                print('###############螺杆设计###############')
                print('螺距P = ', P, 'mm')
                print('螺纹的工作高度h = ', h, 'mm')
                print('螺纹大径d = ', d, 'mm')
                print('螺纹内径d1 = ', d1, 'mm')
                print('螺纹中径d2 = ', d2, 'mm')
                print('螺纹中径升角Ψ = ', phi, '°')
                break
        break
    else:
        pass

# 螺杆结构
print('退刀槽尺寸为：', 1.5 * P, '× Φ', d1 - 0.5)
print('d0 = ', d + 5, 'mm')
print('挡圈厚度：8mm')
print('螺钉直径为：', 0.25 * d, 'mm')

# 强度校核
T = F * d2 / 2 * math.tan(phi + rho_)
sigma = (4 * F) / (pi * pow(d1, 2))
tau = T / (0.2 * pow(d1, 3))
sigma_v = pow(pow(sigma, 2) + 3 * pow(tau, 2), 0.5)
if sigma_v < sigma_agree:
    print('σγ =', sigma_v, ' < [σ]，强度符合强度要求')
else:
    print('还未集成强度校核至螺距，直径选择！！！')

# 螺母的设计与计算
print('###############螺母设计###############\n'
      '材料：锡青铜   牌号：ZCuSn10Pb1')

