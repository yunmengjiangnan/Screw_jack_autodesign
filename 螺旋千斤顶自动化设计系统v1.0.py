# -*- coding = utf-8 -*-
# @Time : 2021/12/3 20:15
# @Author : xzh
# @File : 螺旋千斤顶自动化设计系统v1.0.py
# @Software: PyCharm

import math
from math import ceil, pi

# 螺纹的牙型
# #选用矩形螺纹，采用内径对中，配合选H8/h8，在计算强度时不考虑螺纹的径向间隙。

# 螺杆的材料
# #选用45钢

# 螺杆的直径与自锁验算
# #输入设计原始数据
F = 20  # 最大起重量（KN）
H = 150  # 最大起升高度（mm）
print()
F = int(input('请输入最大起重量（KN）: '))
H = int(input('请输入最大起升高度（mm）: '))
sigma_s = 353  # 45号钢屈服极限（MPa）
S = 3  # 安全系数
alpha = 0  # (°)
mu = 0.10  # (0.08 ~ 0.10)
n = 1  # 螺纹条数
# #录入国家标准推荐螺距与直径
P_list = (2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 40, 48)
P_and_d_first_list = {
    '2': (10, 12, 16, 20, 26),
    '3': (10, 12, 32, 40, 50, 60),
    '4': (16, 20, 80),
    '5': (26, 100),
    '6': (32, 40, 120),
    '8': (50, 60),
    '10': (32, 40, 80, 200),
    '12': (50, 60, 100, 250, 320, 400),
    '16': (80, 120, 160, 500)
}

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
            # d = 28
            d1 = d - P
            # 自锁验算
            rho_ = math.atan(mu / math.cos(alpha / 2)) * 180 / pi
            d2 = (d1 + d) / 2
            phi = math.atan((n * P) / (pi * d2)) * 180 / pi
            if phi <= rho_ - 1:
                print('最大起重量F = ', F, 'KN')
                print('最大升起高度H = ', H, 'mm')
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
T = F * d2 / 2 * math.tan((phi + rho_) * pi / 180)
sigma = (4 * F * pow(10, 9)) / (pi * pow(d1, 2))
tau = T / (0.2 * pow(d1, 3)) * pow(10, 9)
sigma_v = pow(pow(sigma, 2) + 3 * pow(tau, 2), 0.5) * pow(10, -6)
if sigma_v < sigma_agree:
    print('σγ =', sigma_v, ' < [σ]，强度符合强度要求')
else:
    print('还未集成强度校核至螺距，直径选择！！！')

# 螺母的设计与计算
print('###############螺母设计###############\n'
      '材料：锡青铜   牌号：ZCuSn10Pb1')
# #螺纹圈数
p_ = 25
Z_min = F * pow(10, 3) / (pi * d2 * h * p_)
Z = ceil(Z_min)
Z_ = Z + 1.5
H_ = Z_ * P
a = H_ / 3
D_min = 1.6 * d
D = ceil(D_min)
D1_min = 1.3 * D
D1 = ceil(D1_min)
print('螺纹圈数Z = ', Z)
print('实际螺纹圈数Z\' = ', Z_)
print('螺母高H\' = ', H_, 'mm')
print('a = ', a, 'mm')
print('D = ', D, 'mm')
print('D1 = ', D1, 'mm')
print(
    '圆柱面配合采用 H8 / n7,\n'
    '螺母下端和底座孔上端均加工出倒角，倒角尺寸为C2。\n'
    '同时安置紧定螺钉防止螺母转动，紧定螺钉选用 GB/T65 的开槽圆头螺钉。\n')

# 螺杆稳定性计算
print('############螺杆稳定性计算############\n')
nju = 2
l = H + H_ / 2 + 1.5 * d
i = d1 / 4
Lambda = nju * l / i
Fcr = 480 * pi * d1 * d1 / 4 / (1 + 0.0002 * Lambda * Lambda) / 1000
Ssc = Fcr / F
Ss = (2.5, 4)
if Ss[0] < Ssc:
    print('螺杆稳定性合格。')
else:
    print('螺杆稳定性不合格，请检查数据！！！！！！！')

# 托杯的设计与计算
print('###############托杯设计###############\n'
      '材料：选用 Q235 碳钢,模锻制造。')
delta = 10
D2 = ceil(0.6 * d)
D3 = ceil(2.4 * d)
p_ = 20
D4 = ceil(pow((4 * F * 1000) / (pi * p_) + pow(D2, 2), 0.5))
print('δ = ', delta)
print('托杯高 = ', 1.6 * d)
print('D2 = ', D2, 'mm')
print('D3 = ', D3, 'mm')
print('D4 = ', D4, 'mm')

# 手柄的设计与计算
print('###############手柄设计###############\n'
      '材料：Q235 碳钢')
# #手柄长度
mu = 0.06
M1 = F * math.tan((phi + rho_) * pi / 180) * (d2 / 2)
M2 = 0.25 * (D2 + D4) * mu * F
K = 200
Lp = (M1 + M2) / K * 1000
Lw = Lp + (0.5 * D4) + 100
H1 = H + 20  # 提前计算底座参量用于确定千斤顶的最小高度
HH_min = H1 + H_ + 1.5 * P + 1.5 * d + 1.6 * d  # 千斤顶的最小高度
if Lw < HH_min:
    print('Lw 不超过千斤顶的最小高度，所以手柄实际长度为: ', Lw)
else:
    Lw_new = round(Lw % HH_min)
    Ht = Lw - Lw_new  # 套筒长度
    print('Lw 不应超过千斤顶的最小高度，所以将手柄实际长度改为: ', Lw_new,
          '另外加套筒，套筒长 ', Ht)
# #手柄直径
sigma_b = 120
dp = pow((K * Lp) / (0.1 * sigma_b), 1 / 3)
dk = dp + 0.5
print('M1 = ', M1)
print('M2 = ', M2)
print('Lw = ', Lw)
print('dp = ', dp)
print('dk = ', dk)
print('固定螺钉选用GB/T68——2000 M8×20开槽沉头螺钉')

# 底座的设计与计算
print('###############底座设计###############\n')
print('（1）材料：HT100 铸铁 \n（2）尺寸设计：见图 5，取壁厚δ = 10mm，锥度按照1: 5 设计。')
D5 = D + 6
D6 = D5 + (H1 / 5)
sigma_p = 2.5
D7 = pow((4 * F * 1000) / (pi * sigma_p) + pow(D6, 2), 0.5)
D8 = D1
print('D5 = ', D5)
print('D6 = ', D6)
print('[σ]p = ', sigma_p)
print('D7 = ', D7)
print('D8 = ', D8)
# 千斤顶的效率
eta = (F * P) / (2 * pi * (M1 + M2))
if eta < 0.3:
    print('η = ', eta, '<0.3\n因此， 设计效率符合要求。')
else:
    print('η = ', eta, '我也没办法了，你效率太高了，手算吧╮(─▽─)╭')
