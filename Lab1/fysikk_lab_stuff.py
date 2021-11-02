import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import CubicSpline

# Horisontal avstand mellom festepunktene er 0.200 m
h = 0.200
xfast=np.asarray([0,h,2*h,3*h,4*h,5*h,6*h,7*h])
yfast = np.asarray([0.297,0.225,0.146,0.224,0.226,0.153,0.152,0.175])

cs = CubicSpline(xfast, yfast, bc_type='natural')

xmin = 0.000
xmax = 1.401
dx = 0.001

x = np.arange(xmin, xmax, dx)   

#funksjonen arange returnerer verdier paa det "halvaapne" intervallet
#[xmin,xmax), dvs slik at xmin er med mens xmax ikke er med. Her blir
#dermed x[0]=xmin=0.000, x[1]=xmin+1*dx=0.001, ..., x[1400]=xmax-dx=1.400, 
#dvs x blir en tabell med 1401 elementer
Nx = len(x)
y = cs(x)       #y=tabell med 1401 verdier for y(x)
dy = cs(x,1)    #dy=tabell med 1401 verdier for y'(x)
d2y = cs(x,2)   #d2y=tabell med 1401 verdier for y''(x)

g = 9.81
c = 2/5

b = np.arctan(dy)

v_x = np.sqrt(2*g*(y[0]-y)/(1+c))

v_x_horison = np.cos(b)*v_x

a_sentripetal = (v_x*d2y) / (1+dy**2)**(3/2)

fN_abs = np.abs((c*g*np.sin(b))/((1+c)*g*np.cos(b)+a_sentripetal))

fN = ((c*g*np.sin(b))/((1+c)*g*np.cos(b)+a_sentripetal))

def vx_n(n):
    return (1/2)*(v_x[n-1]+v_x[n])  # vx er tabell over x-komponent av hastighet

def deltaT(n):
    return (dx)/vx_n(n)  # dx er 0.001



#calculates time
tn = np.array([0], dtype=float)
sum = 0
for i in range(1, Nx):
    sum += deltaT(i)
    np.append(tn, sum)

#reading data from tracker file

x_track = np.asarray([])
y_track = np.asarray([])
v_track = np.asarray([])
t_track = np.asarray([])

#file = open('1.txt', 'r')

"""
lines = file.readlines()
for i in range(2,len(lines)):
    data = lines[i].split(',')
    np.append(t_track, float((data[0]))
    np.append(x_track, float(data[1]))
    np.append(y_track, data[2])
    np.append(v_track, data[3])
"""

data = np.loadtxt("Lab1\Python lab1\Raw_data_exp\Eksp4_t_x_y_v.txt", float, delimiter=';', usecols=[0, 1, 2, 3], skiprows=2)
for dataline in data:

        np.append(t_track, dataline[0])
        np.append(t_track, dataline[1])
        np.append(t_track, dataline[2])
        np.append(t_track, dataline[3])

#average end speed
v_end = np.asarray([1.262, 1.251, 1.203, 1.249, 1.243, 1.201,1.263, 1.233 ])
v_end_mean = v_end.mean()

#standardavik
standardavvik = np.sqrt(np.mean((v_end-v_end_mean)**2))

#standardfeil
standardavvik / np.sqrt(len(v_end))

#plotting
fig, axs = plt.subplots(4, figsize=(6,12))
fig.suptitle('Report')

#banens form
#teoretisk
axs[0].plot(x, y, xfast, yfast, '*')
axs[0].set_xlabel("x(m)", fontsize=20)
axs[0].set_ylabel("y(m)", fontsize=20)
axs[0].set_title("Banens form")
axs[0].grid()
axs[0].set_ylim(0.0, 0.40)
axs[0].plot(x_track, y_track)


#eksperimentell


#
axs[1].plot(x,b)
axs[1].set_xlabel("x(m)", fontsize=20)
axs[1].set_ylabel("b(rad)", fontsize=20)
axs[1].set_title("banens helling")
axs[1].grid()


#fart x-komponent av x
#teoretisk
axs[2].plot(x, v_x)
axs[2].set_xlabel("x(m)", fontsize=20)
axs[2].set_ylabel("v(x) (m/s)", fontsize=20)
axs[2].set_title("kulens fart")
axs[2].grid()

#eksperimentell


axs[3].plot(x, fN_abs)
axs[3].set_xlabel("x(m)", fontsize=20)
axs[3].set_ylabel("|f/N|", fontsize=20)
axs[3].set_title("friksjonskoeffisient")
axs[3].grid()

#hastighet av tid



plt.grid()
plt.show()
