
#단일변수 x에 대해 가우시안 분포
#sigma^2 분산
#u 평균
#



from math import *
from matplotlib.pyplot import *
from random import *

u = 0 #평균
es = 1 #분산

es_ovr_n0 = 1

SNR = pow(10,es_ovr_n0/10)
sigma = sqrt(es/(2*SNR))

res = []

def gaussrand():
    a = 0.3989422804014327 #1/sqrt(2*pi)
    temp = uniform(0,1)
    temp = sigma * sqrt(2.0 * log(1.0 / (1.0-temp)))
    temp = u + temp * cos(2*pi*uniform(0,1))
    res.append(temp)






def AWGN(x):
    pass
for x in range(100):
    gaussrand()


plot(res)

show()


