import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


c=20

g=9.81 #Aceleración de gravedad
m=1   #Masa de los huevos
L=1    #Longitud del péndulo
h=0.01 #El paso del tiempo
ti=0    #tiempo inicial
tf=1 #tiempo final
A0=-3#-np.pi-4 #Valor inicial del ángulo (-4 radianes a partir del punto más bajo)
A01=-4.2
A02=-5
A03=-5.5
A04=-6.2
Ap0=0   #Valor inicial de la velocidad angular


def runProgram(m,L,h,ti,tf,A0,Ap0):
    def F1(t,y,Y):
        return Y 

    def F2(t,y,Y):
        f2= (g*np.sin(y)-c**2*np.cos(c*t)*np.sin(c*t)+g*np.cos(c*t)+L*Y**2*(np.sin(y)+np.cos(c*t)*np.cos(y)) )/(L*(1+(np.cos(y)-np.cos(c*t)*np.sin(y))))
        #print(round(t,3),round(y,3),round((1+(np.cos(y)-np.cos(c*t)*np.sin(y))),3))
        return f2 #f2

    def rungeKuta4(f1,f2,a,b,y0,yp0,h):
        
        N=int((b-a)/h)
        t=np.arange(a, b+h, h, dtype=float)
        
        t[0]=a
        y=np.zeros(N+1)
        y[0]=y0
        Y=np.zeros(N+1)
        Y[0]=yp0
        
        for i in range(0,N):
            k1=h*f1(t[i],y[i],Y[i])
            k01=h*f2(t[i],y[i],Y[i])
        
            k2=h*f1(t[i]+(h/2),y[i]+(k1/2),Y[i]+(k01/2))
            k02=h*f2(t[i]+(h/2),y[i]+(k1/2),Y[i]+(k01/2))
        
            k3=h*f1(t[i]+(h/2),y[i]+(k2/2),Y[i]+(k02/2))
            k03=h*f2(t[i]+(h/2),y[i]+(k2/2),Y[i]+(k02/2))
        
            k4=h*f1(t[i]+h,y[i]+k3,Y[i]+k03)
            k04=h*f2(t[i]+h,y[i]+k3,Y[i]+k03)
        
            y[i+1]=y[i]+(k1+2*k2+2*k3+k4)/6
            Y[i+1]=Y[i]+(k01+2*k02+2*k03+k04)/6
        return t, y, Y  
      
    t,A,W = rungeKuta4(F1,F2,ti,tf,A0,Ap0,h)
    t,A1,W1 = rungeKuta4(F1,F2,ti,tf,A01,Ap0,h)
    t,A2,W2 = rungeKuta4(F1,F2,ti,tf,A02,Ap0,h)
    t,A3,W3 = rungeKuta4(F1,F2,ti,tf,A03,Ap0,h)
    

    x = c*t + L*np.sin(A) #x[]
    y = L*np.cos(A)+np.sin(c*t) #y[]
    #***********************************
    x1 = c*t + L*np.sin(A1) #x[]
    y1 = L*np.cos(A1)+np.sin(c*t) #y[]
    #***********************************
    x2 = c*t + L*np.sin(A2) #x[]
    y2 = L*np.cos(A2)+np.sin(c*t) #y[]
    #***********************************
    x3 = c*t + L*np.sin(A3) #x[]
    y3 = L*np.cos(A3)+np.sin(c*t) #y[]
    #***********************************
    x4 = c*t + L*np.sin(A3) #x[]
    y4= L*np.cos(A3)+np.sin(c*t) #y[]

    
    #*******GRAFICANDO*******************

    fig = plt.figure()
    ax=fig.gca()

    def recta(i): #pinta la cuerda
        xpend=[c*t[i], x[i]]
        ypend=[L*np.sin(c*t[i]),y[i]]
        plt.plot(xpend,ypend, 'm')
    def recta1(i): #pinta la cuerda
        xpend=[c*t[i], x1[i]]
        ypend=[L*np.sin(c*t[i]),y1[i]]
        plt.plot(xpend,ypend, 'm')
    def recta2(i): #pinta la cuerda
        xpend=[c*t[i], x2[i]]
        ypend=[L*np.sin(c*t[i]),y2[i]]
        plt.plot(xpend,ypend, 'm')
    def recta3(i): #pinta la cuerda
        xpend=[c*t[i], x3[i]]
        ypend=[L*np.sin(c*t[i]),y3[i]]
        plt.plot(xpend,ypend, 'm')
    def recta4(i): #pinta la cuerda
        xpend=[c*t[i], x4[i]]
        ypend=[L*np.sin(c*t[i]),y4[i]]
        plt.plot(xpend,ypend, 'm')


    def actualizar(i) :
        
        ax.clear()
        recta(i)
        recta1(i)
        recta2(i)
        recta3(i)
        recta4(i)
        #plot trayectorias manubrio
        plt.plot(c*t[:i],L*np.sin(c*t[:i]), 'k--')

        #plot trayectorias centro de masa
        plt.plot(x[:i+1],y[:i+1], 'y')
        #1***********************
        plt.plot(x1[:i+1],y1[:i+1], 'c')
        #2***********************
        plt.plot(x2[:i+1],y2[:i+1], 'b')
        #3***********************
        plt.plot(x3[:i+1],y3[:i+1], 'g')
        #3***********************
        plt.plot(x4[:i+1],y4[:i+1], 'r')
        
        
        #plot las masas
        plt.plot(x[i],y[i], 'mo',markersize=15) #plt si sigue fija
        plt.plot(x1[i],y1[i], 'mo',markersize=15)
        plt.plot(x2[i],y2[i], 'mo',markersize=15)
        plt.plot(x3[i],y3[i], 'mo',markersize=15)
        plt.plot(x4[i],y4[i], 'mo',markersize=15)
        



        plt.title(str(round(t[i],3))+" [s]") #tiempo en segundos
        
        #limites del recuadro
        lim=5
        plt.xlim(0,12)
        plt.ylim(-3,3)
    ani = animation.FuncAnimation(fig, actualizar, range(len(t)))
    fig
    plt.show()

runProgram(m,L,h,ti,tf,A0,Ap0)