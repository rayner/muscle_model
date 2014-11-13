#!/usr/bin/python

# Program for simulating full model with coupling

import sys
import numpy as np
import matplotlib.pyplot as plt
from decimal import *
sys.path += '.'
from x_inf import *

getcontext().prec = 28 # decimal precision

# Importing data
f = open('../../MatlabSupport/Main_Version/data/input.csv')
data = f.read().splitlines()

# Model parameters

Cmem = Decimal(data[0])
gKS = Decimal(data[1]) * Cmem
gKF = Decimal(data[2]) * Cmem
gCa = Decimal(data[3]) * Cmem
gL = Decimal(data[4]) * Cmem
VKS = Decimal(data[5])
VKF = Decimal(data[6])
VCa = Decimal(data[7])
VL = Decimal('10e-3'); # Decimal(data[8]);
Vhalf_n = Decimal(data[9])
Vhalf_p = Decimal(data[10])
Vhalf_q = Decimal(data[11])
Vhalf_e = Decimal(data[12])
Vhalf_f = Decimal(data[13])
Cahalf_h = Decimal(data[14]) * Decimal('1e-9')
k_n = Decimal(data[15])
k_p = Decimal(data[16])
k_q = Decimal(data[17])
k_e = Decimal(data[18])
k_f = Decimal(data[19])
k_h = Decimal(data[20]) * Decimal('1e-9')
T_n = Decimal(data[21])
T_p = Decimal(data[22])
T_q = Decimal(data[23])
T_e = Decimal(data[24])
T_f = Decimal(data[25])
T_Ca = Decimal(data[26])
alphaCa = Decimal(data[27])
thiCa = Decimal('6.1e-6') / (T_Ca * gCa)

# Simulation Parameters
deltat = Decimal('0.01e-3')
duration = Decimal('0.03')                 #*********************      Duration    Duration   ***************
numpoints = int(round(duration/deltat))
numtests = 11
xaxis = [round(x * Decimal('1e3'), 2) for x in np.arange(deltat, duration+deltat, deltat)]

# Input parameters
onset = int(round(Decimal('0.002')/deltat))
offset = int(round(Decimal('0.022')/deltat))

# Variable Declaration
V = list()
I_j = list()
I_mem = list()
Ca = list()
n = list()
p = list()
q = list()
e = list()
f = list()
h = list()

for i in range(0,numtests):
    V.append(list())
    I_mem.append(list())
    Ca.append(list())
    n.append(Decimal('0'))
    p.append(Decimal('0'))
    q.append(Decimal('0'))
    e.append(Decimal('0'))
    f.append(Decimal('0'))
    h.append(Decimal('0'))
    I_j.append(Decimal('0'))
    for j in range(0,numpoints):
        V[i].append(Decimal('0'))
        I_mem[i].append(Decimal('0'))
        Ca[i].append(Decimal('0'))
I_j.append(Decimal('0'))

# Input initialization
for i in range(0,numtests):
    for j in range(0,numpoints):
        V[i][j] = Decimal('-70e-3')

Vstim = Decimal('40e-3')
for i in range(0,numtests):
    for j in range(onset-1,offset):
        V[i][j] = Vstim
    Vstim = Vstim - Decimal('10e-3')

# Variable initialization
for j in range(0,numtests):
    Ca[j][0] = Decimal('0')
    n[j] = x_inf(V[j][0], Vhalf_n, k_n)
    p[j] = x_inf(V[j][0], Vhalf_p, k_p)
    q[j] = x_inf(V[j][0], Vhalf_q, k_q)
    e[j] = x_inf(V[j][0], Vhalf_e, k_e)
    f[j] = x_inf(V[j][0], Vhalf_f, k_f)

# Start of simulation
for j in range(0,numtests):
    for i in range(1,numpoints):
        dn = (x_inf(V[j][i-1], Vhalf_n, k_n) - n[j])/T_n
        n[j] = n[j] + dn*deltat
        dp = (x_inf(V[j][i-1], Vhalf_p, k_p) - p[j])/T_p
        p[j] = p[j] + dp*deltat
        dq = (x_inf(V[j][i-1], Vhalf_q, k_q) - q[j])/T_q
        q[j] = q[j] + dq*deltat
        de = (x_inf(V[j][i-1], Vhalf_e, k_e) - e[j])/T_e
        e[j] = e[j] + de*deltat
        df = (x_inf(V[j][i-1], Vhalf_f, k_f) - f[j])/T_f
        f[j] = f[j] + df*deltat
        h[j] = x_inf(Ca[j][i-1], Cahalf_h, k_h)
        # H_rec[i] = h[j]
        IKS = gKS * n[j] * (V[j][i-1] - VKS)
        IKF = gKF * p[j]**4 * q[j] * (V[j][i-1] - VKF)
        ICa = gCa * e[j]**2 * f[j] * (1 + (h[j] - 1) * alphaCa) * (V[j][i-1] - VCa)
        IL = gL * (V[j][i-1] - VL)

        dCa = -(Ca[j][i-1]/T_Ca + thiCa*ICa)
        Ca[j][i] = Ca[j][i-1] + dCa*deltat

        I_mem[j][i] = (IKS + IKF + ICa)

    plt.plot(xaxis, [x * Decimal('1e9') for x in I_mem[j]])

plt.ylabel('Imem (nA)')
plt.xlabel('Time (ms)')
plt.show()
