
#단일변수 x에 대해 가우시안 분포
#sigma^2 분산
#u 평균
#



from math import *
#from matplotlib.pyplot import *

sigma = 1 # 분산(sigma**2)
u = 1

def AWGN(x):
    return (1/sqrt((sigma**2)*2*pi)*(exp(-(((x-u)**2)/2*(sigma**2)))))           # (1/sigma*sqrt(2*pi))*exp(-((x-u)**2/2*sigma))                  



