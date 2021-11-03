# TFY41xx Fysikk vaaren 2021.
#
# Programmet tar utgangspunkt i hoeyden til de 8 festepunktene.
# Deretter beregnes baneformen y(x) ved hjelp av 7 tredjegradspolynomer, 
# et for hvert intervall mellom to festepunkter, slik at baade banen y, 
# dens stigningstall y' = dy/dx og dens andrederiverte
# y'' = d2y/dx2 er kontinuerlige i de 6 indre festepunktene.
# I tillegg velges null krumning (andrederivert) 
# i banens to ytterste festepunkter (med bc_type='natural' nedenfor).
# Dette gir i alt 28 ligninger som fastlegger de 28 koeffisientene
# i de i alt 7 tredjegradspolynomene.

# De ulike banene er satt opp med tanke paa at kula skal 
# (1) fullfoere hele banen selv om den taper noe mekanisk energi underveis;
# (2) rulle rent, uten aa gli ("slure").

# Vi importerer noedvendige biblioteker:
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import CubicSpline
import data_util

# Horisontal avstand mellom festepunktene er 0.200 m
h = 0.200
xfast=np.asarray([0,h,2*h,3*h,4*h,5*h,6*h,7*h])


# Vi begrenser starthøyden (og samtidig den maksimale høyden) til
# å ligge mellom 250 og 300 mm
ymax = 300
# yfast: tabell med 8 heltall mellom 50 og 300 (mm); representerer
# høyden i de 8 festepunktene
yfast=np.asarray(np.random.randint(50, ymax, size=8))
#konverter fra m til mm
yfast =yfast/1000
# inttan: tabell med 7 verdier for (yfast[n+1]-yfast[n])/h (n=0..7); dvs
# banens stigningstall beregnet med utgangspunkt i de 8 festepunktene.
inttan = np.diff(yfast)/h
attempts=1
# while-løkken sjekker om en eller flere av de 3 betingelsene ovenfor
# ikke er tilfredsstilt; i så fall velges nye festepunkter inntil
# de 3 betingelsene er oppfylt
while (yfast[0] < yfast[1]*1.04 or
       yfast[0] < yfast[2]*1.08 or
       yfast[0] < yfast[3]*1.12 or
       yfast[0] < yfast[4]*1.16 or
       yfast[0] < yfast[5]*1.20 or
       yfast[0] < yfast[6]*1.24 or
       yfast[0] < yfast[7]*1.28 or
       yfast[0] < 0.250 or
       np.max(np.abs(inttan)) > 0.4 or
       inttan[0] > -0.2):
          yfast=np.asarray(np.random.randint(0, ymax, size=8))
          
          #konverter fra m til mm
          yfast =yfast/1000
          
          inttan = np.diff(yfast)/h
          attempts=attempts+1
          

yfast = np.array([
    0.274, 
    0.153, 
    0.092, 
    0.141, 
    0.141, 
    0.162, 
    0.128, 
    0.060])

# Omregning fra mm til m:
# xfast = xfast/1000
# yfast = yfast/1000

# Når programmet her har avsluttet while-løkka, betyr det at
# tallverdiene i tabellen yfast vil resultere i en tilfredsstillende bane. 

#Programmet beregner deretter de 7 tredjegradspolynomene, et
#for hvert intervall mellom to nabofestepunkter.


#Med scipy.interpolate-funksjonen CubicSpline:
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
pi = 3.15169264
M = 0.031
r = 0.011

def t_x(Nx, v_x):
    time = 0
    times = np.array([0])
    for i in range(1,Nx):
        delta_t = (2*dx)/(v_x[i-1] + v_x[i])
        time = time + delta_t
        times = np.append(times, [time])
    return times

# def x_t(Nx, v_x):
#     time = 0
#     times = np.array([0])
#     for i in range(1,Nx):
#         delta_t = (2*dx)/(v_x[i-1] + v_x[i])
#         time = time + delta_t
#         times = np.append(times, [time])
#     x_t_list = []
#     for xt in range(0,Nx):
#         x = 0
#         for ii in range(0, len(times)):
#             t = times[ii]
#             if t >= times[xt]:
#                 x_t_list.append(ii)
#                 break
#     return x_t_list


K = np.asarray( d2y/(((1 + dy**2)**(3/2))) )
v_x = np.asarray( np.sqrt((2*g*(y[0] - y))/(1+c)) )
a = np.square(v_x)*K
angle = np.arctan(dy)
angle_deg = np.arctan(dy) * 180/3.14
N = M*(g * np.cos(angle) + a)
my = 0.14
f = (2*M*g*np.sin(angle))/7
# f = np.arange(0, my*np.abs(N))
f_N = np.abs(f/N)
# for i in range(0, 1400):
#     if i > 590 and i < 612:
#         print("itteration : " , i)
#         print("   f/N : ", f_N[i], "   N : ", N[i], "   f : ", f[i], "   dy: ", dy[i])

# Bruker 'Lab1/Python lab1/Raw_data_exp\\Eksp5_t_x_y_v.txt'
comp_t_array, comp_x_array, comp_y_array, comp_v_array = data_util.get_array_from_files("Lab1/Python lab1/Raw_data_exp", 4, 1401, 0.03)

#Eksempel: Plotter banens form y(x)
baneform = plt.figure('y(x)',figsize=(12,6))
plt.plot(x,y,xfast,yfast,'*')
plt.plot(comp_x_array, comp_y_array, xfast,yfast,'r*')
plt.title('Banens form')
plt.xlabel('$x$ (m)',fontsize=20)
plt.ylabel('$y(x)$ (m)',fontsize=20)
plt.ylim(0.0,0.40)
plt.grid()
plt.show()
#Figurer kan lagres i det formatet du foretrekker:
#baneform.savefig("baneform.pdf", bbox_inches='tight')
#baneform.savefig("baneform.png", bbox_inches='tight')
#baneform.savefig("baneform.eps", bbox_inches='tight')
comp_x_array_mod = comp_x_array + 0.04
comp_v_array_mod = np.insert(comp_v_array, 0, comp_v_array[0])
comp_x_array_mod = np.insert(comp_x_array_mod, 0, 0)
comp_v_array_mod = np.insert(comp_v_array_mod, 0, 0)
comp_x_array_mod = np.insert(comp_x_array_mod, 0, 0)
v_x_plt = plt.figure('',figsize=(12,6))
plt.plot(x,v_x)
plt.plot(comp_x_array_mod, comp_v_array_mod)
plt.title('')
plt.xlabel('$x$ m',fontsize=20)
plt.ylabel('$v(x)$ m/S',fontsize=20)
plt.grid()
plt.show()

angle_plt = plt.figure('B(x)',figsize=(12,6))
plt.plot(x,angle_deg)
plt.title('B')
plt.xlabel('$x$ (m)',fontsize=20)
plt.ylabel('$B(grader)$',fontsize=20)
plt.grid()
plt.show()

N_plt = plt.figure('N(x)',figsize=(12,6))
plt.plot(x,N)
plt.title('Normalkraft')
plt.xlabel('$x$ (m)',fontsize=20)
plt.ylabel('$F(Newton)$',fontsize=20)
plt.grid()
plt.show()

N_plt = plt.figure('N(x)/Mg',figsize=(12,6))
plt.plot(x,(N/(M*g)))
plt.title('Normalkraft')
plt.xlabel('$x$ (m)',fontsize=20)
plt.ylabel('$F(Newton)$',fontsize=20)
plt.grid()
plt.show()

K_plt = plt.figure('K(x)',figsize=(12,6))
plt.plot(x,K)
plt.title('Krumning')
plt.xlabel('$x$ (m)',fontsize=20)
plt.ylabel('$y(x)$ (m)',fontsize=20)
plt.grid()
plt.show()

f_N_plt = plt.figure('f/N',figsize=(12,6))
plt.plot(x,f_N)
plt.title('f/N')
plt.xlabel('$x$ (m)',fontsize=20)
plt.ylabel('$|f/N|$ (m)',fontsize=20)
plt.grid()
plt.show()

v_t_plt = plt.figure('v(t)',figsize=(12,6))
plt.plot(t_x(Nx, v_x),v_x)
plt.title('v(t)')
plt.xlabel('$t$ (m)',fontsize=20)
plt.ylabel('$|v(t)|$ (m)',fontsize=20)
plt.grid()
plt.show()

t_x_plt = plt.figure('',figsize=(12,6))
plt.plot(t_x(Nx, v_x), x)
plt.plot(comp_t_array, comp_x_array)
plt.title('')
plt.xlabel('$t$ (s)',fontsize=20)
plt.ylabel('$|x|$ (m)',fontsize=20)
plt.grid()
plt.show()


print('Antall forsøk',attempts)
print('Festepunkthøyder (m)',yfast)
print('Banens høyeste punkt (m)',np.max(y))

print('NB: SKRIV NED festepunkthøydene når du/dere er fornøyd med banen.')
print('Eller kjør programmet på nytt inntil en attraktiv baneform vises.')