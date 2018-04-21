# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 20:32:47 2018
本文是双孔隙土水曲线的拟合，文献参考是
Dexter AR, Czyż EA, Richard G, Reszkowska A. A user-friendly water retention
function that takes account of the textural and structural pore spaces in soil.
Geoderma. 2008;143(3):243-53.
@author: Fanxihui
"""
import xlrd
import numpy as np
from scipy.optimize import leastsq
import matplotlib.pyplot as plt

"""
需要修改的参数
"""
h_index=3                                      #输入吸力的列数
theta_index=4                                  #输入含水率的列数
filename='11.xlsx'                             #数据文件名

"""
导入数据
"""
workbook = xlrd.open_workbook(filename)
#print(workbook.sheet_names())                  #查看所有sheet
booksheet = workbook.sheet_by_index(0)          #用索引取第一个sheet
h = booksheet.col_values(h_index)
theta= booksheet.col_values(theta_index)
h = np.array(h)                                 #list转为np.array格式，便于后续计算
theta=np.array(theta)
"""
拟合参数
"""

def fun(p, h):
    """
    定义想要拟合的函数
    """
    c1,A1,h1,A2,h2 = p  #从参数p获得拟合的参数
    return c1+A1*np.exp(-h/h1)+A2*np.exp(-h/h2)

def err(p, h, theta):
    """
    定义误差函数
    """
    return fun(p,h) -theta

#定义初始值
p0 = [0.3,0.233,1000,0.1,100]

#xishu = leastsq(err, p0, args=(h,theta))
xishu,cov,infodict,mesg,ier = leastsq(err, p0, args=(h,theta),full_output=True)
#分别得到的是系数，
c1=xishu[0]
A1=xishu[1]
h1=xishu[2]
A2=xishu[3]
h2=xishu[4]
##求解拟合优度 R2
ss_err=(infodict['fvec']**2).sum()
ss_tot=((theta-theta.mean())**2).sum()
rsquared=1-(ss_err/ss_tot)

print ('Parameters=',xishu)
print('R2=',rsquared)

# xishu[0]，即为获得的参数
plt.figure(num='astronaut',figsize=(5,10)) # 两幅图
plt.subplot(2,1,1)                         #第一副图
plt.semilogx(h,theta,'o')
h=np.logspace(1,4,1000)

#plt.plot(np.log10(h),c1+A1*np.exp(-h/h1)+A2*np.exp(-h/h2))
plt.semilogx(h,c1+A1*np.exp(-h/h1)+A2*np.exp(-h/h2))

"""
孔隙分布
"""
k=np.linspace(0,0,999)
h=np.logspace(1,4,1000)                     #unit: hPa
r=4*7.29*0.01/h                             #unit:
for i in range(1,999):
    k[i]=-(fun(xishu,h[i])-fun(xishu,h[i-1]))/(np.log10(h[i])-np.log10(h[i-1]))
plt.subplot(2,1,2)                          #第二幅图
plt.semilogx(h[1:],k)
