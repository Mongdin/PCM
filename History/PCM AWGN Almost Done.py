'''
Mongdin
19/11/01 AWGN 추가
'''

from math import *
from matplotlib.pyplot import *
from random import uniform as randnum

#설정
periods = 2 # sin 신호의 길이를 주기단위로 표시 radi(max) = 2*pi*periods
sampling = 32 # 한 주기당 샘플링할 표본 갯수
quantbit = 4
extend = 8 
u = 0                       #평균
es = 1                      #분산
es_ovr_n0 = 20
######################노이즈, 변복조방식,수신기 설정
AWGN_EN = False
ASK_EN = False
INTEG_RECEIVER = False

SNR = pow(10,es_ovr_n0/10)
sigma = sqrt(es/(2*SNR))

def AWGN():
    a = 0.3989422804014327 #1/sqrt(2*pi)
    temp = randnum(0,1)
    temp = sigma * sqrt(2.0 * log(1.0 / (1.0-temp)))
    temp = u + temp * cos(2*pi*randnum(0,1))
    return temp


quantizing = 2**quantbit # 양자화 근사치 갯수(3비트)
total_samples = periods*sampling
sampled = []
quantized = []
quantized_level = []
codebit = []
coded = []
pcm = []
pcm_ex = []
integ = []
picked = []
decoded = []
ASK = []
CHANNEL = []
#######################################################################
#표본화
for x in range(total_samples):
    radi = round((x/sampling)*2,3) # radi*pi = 실제 radian 실수값 ->radi를 읽기편함
    value = round(sin(radi*pi),3) # sin 함수 사용시 radi에 pi를 곱해서 사용해야함
    sampled.append(value) # 배열의 맨 뒤에 값 추가





sigmax = max(sampled) # 샘플된 값들중 가장 큰 값
sigmin = min(sampled) # 샘플된 값들중 가장 작은 값
level = (sigmax-sigmin)/quantizing # 양자화 레벨
quanq = level/2 # 양자화 레벨사이 중간값으로 근사화하기위함



#양자화
for x in range(total_samples):
    doma = sampled[x] # 샘플된 신호를 도마위에올림
    if doma==0:
            quantized.append(0)
            quantized_level.append(quantizing//2)
    else:
        for n in range(quantizing//2): # 양수부분만의 양자화레벨만큼 반복
            if level*n<abs(doma)<=level*(n+1): # 양자화 레벨 구간 판단
                if doma<0:
                    quantized.append(round(-(level*n)-quanq,3)) # 음수일때 소숫점 3째자리까지 근사화
                    quantized_level.append((quantizing//2)-n)
                else: 
                    quantized.append(round((level*n)+quanq,3)) # 양수일때 소숫점 3째자리까지 근사화
                    quantized_level.append(n+(quantizing//2))
                


#coded배열 0으로 초기화
coded = [[0]*quantbit for i in range(len(quantized_level))]
        
#부호화
for x in range(len(quantized_level)):
    doma = quantized_level[x]
    for n in list(reversed(range(quantbit))):
        #print(doma,n,doma//(2**n))
        if doma//(2**n)==1:
            
            coded[x][n] = 1
            doma = doma % (2**n)
            
        else:
            coded[x][n]=0

#pcm신호 파형만들기위함(lsb->msb순서로 전송)
for x in range(len(coded)):
    for n in range(len(coded[x])):
        pcm.append(coded[x][n])
#pcm 신호 늘리기
for x in pcm:
    for n in range(extend):
        pcm_ex.append(x)


#변조
## ASK                자체적으로 배열을 늘림
if ASK_EN:
    for x in pcm:
        for n in range(1,extend+1):
            ASK.append(x * sin(((2 * pi)/extend)*n))
    CHANNEL = ASK  # 전송



else:
    CHANNEL = pcm_ex
subplot(234)
plot(CHANNEL)
title('CHANNEL')
grid(True)



    
#######################################################
#                        송신                         #
#######################################################

## <channel>
pcm = []
#AWGN Enable시 잡음 추가
if AWGN_EN:
    for x in range(len(CHANNEL)):
        CHANNEL[x] += AWGN()

## </channel>

#######################################################
#                        수신                         #
#######################################################





#ASK 복조
if ASK_EN:
    maxmax = max(CHANNEL)
    for x in range(0,len(CHANNEL),extend):
        if max(CHANNEL[x:x+extend]) > maxmax:
            pcm.append(1)
        else:
            pcm.append(0)
    subplot(235)
    plot(pcm)
    title('ASK DEMOD')
    grid(True)

else:
    for x in range(extend-1,len(integ),extend):
        if CHANNEL[x]<(max(CHANNEL)/2):
            pcm.append(0)
        else:
            pcm.append(1)
    subplot(235)
    plot(pcm)
    title('PCM RECEIVE')
    grid(True)
#적분수신기
if INTEG_RECEIVER:
    doma = 0
    pcm = []
    for x in range(len(CHANNEL)):
        if x%extend == 0:
            doma = 0
        else:
            doma += CHANNEL[x]
        integ.append(doma) # 적분
    
    #비트판별 (적분된것 판별시점(최대일때))
    for x in range(extend-1,len(integ),extend):
        if integ[x]<(max(integ)/2):
            pcm.append(0)
        else:
            pcm.append(1)
    subplot(235)
    plot(integ)
    title('INTEGRAL')
    grid(True)
                   
#디코더(파형복원)
for x in range(0,len(pcm),quantbit):
       buffer = 0
       for n in range(quantbit):
            buffer += (pcm[x+n])*(2**n)
       if buffer<(quantizing//2):
            buffer = -(((quantizing//2)-buffer)*level)
       else:
            buffer = ((buffer-(quantizing//2)))*level
       decoded.append(buffer)

#print(max(integ)/2)

subplot(231)
title('Sampled')
grid(True)
plot(sampled)

subplot(232)
plot(quantized)
title('Quantized')
grid(True)

subplot(233)
plot(quantized_level)
title('Quantized level')
grid(True)






subplot(236)
plot(decoded)
title('Decoded')
grid(True)

print("%d개의 주기,  주기당 %d개의 샘플, 총 %d개의 샘플, %d개의 양자화 레벨, %d개의 펄스"%(periods,sampling,total_samples,quantizing,len(pcm_ex)))
             
show()
