import numpy as np
import matplotlib.pyplot as plt

def time(t0,tf,dt):
    N=int((tf-t0)/dt)
    t=np.arange(t0, tf+dt, dt, dtype=float)
    return t

def theta(t,z):
    theta=np.zeros(len(t))
    for i in range (0,len(t)):
        theta[i] = (np.pi/4)*(1-np.cos(z*t[i]))
    return theta

def w(t,z):
    w=np.zeros(len(t))
    for i in range (0,len(t)):
        w[i] = (np.pi/4)*(np.sin(z*t[i]))
    return w

def alfa(t,z):
    alfa=np.zeros(len(t))
    for i in range (0,len(t)):
        alfa[i] = (np.pi/4)*(np.cos(z*t[i]))
    return alfa
z=5
tf=2.5
t=time(0,tf,0.01)
theta=theta(t,z)
w=w(t,z)
alfa=alfa(t,z)

#for i in range(0,len(t)):
 #   print(t[i],theta[i],w[i],alfa)


plt.plot(t,theta, label="θ") 
plt.plot(t,w, label="θ'") 
plt.plot(t,alfa, label="θ''") 
plt.xlabel('tiempo [s]')
plt.xlim(0,tf)
plt.legend()


plt.show()