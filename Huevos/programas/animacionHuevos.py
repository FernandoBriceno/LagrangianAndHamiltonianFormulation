import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


c=20 #velocidad en ’x’
g=9.81 #Aceleracin de gravedad
m=1 #Masa de los huevos
L=1 #Longitud del pndulo
h=0.01 #El paso del tiempo
ti=0 #tiempo inicial
tf=0.5 #tiempo final
A0=1.5 #Valor inicial del ngulo (-4 radianes a partir del punto ms bajo)
Ap0=0 #Valor inicial de la velocidad angular


def runProgram(m,L,h,ti,tf,A0,Ap0):
    def F1(t,y,Y):
        return Y 

    def F2(t,y,Y):
        f2= (g*np.sin(y)-c**2*np.cos(c*t)*np.sin(c*t)+g*np.cos(c*t)+L*Y**2*(np.sin(y)+np.cos(c*t)*np.cos(y)) )/(L*(1+(np.cos(y)-np.cos(c*t)*np.sin(y))))
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


    x = c*t + L*np.sin(A) #x[]
    y = L*np.cos(A)+np.sin(c*t) #y[]

    
    #*******GRAFICANDO*******************

    fig = plt.figure()
    ax=fig.gca()

    def recta(i): #pinta la cuerda
        xpend=[c*t[i], x[i]]
        ypend=[L*np.sin(c*t[i]),y[i]]
        plt.plot(xpend,ypend, 'g')



    def actualizar(i) :
        
        ax.clear()
        recta(i)

        #plot trayectorias manubrio
        plt.plot(c*t[:i],L*np.sin(c*t[:i]), 'k--')

        #plot trayectorias centro de masa
        plt.plot(x[:i+1],y[:i+1], 'r')

        
        #plot las masas
        plt.plot(x[i],y[i], 'mo',markersize=15) #plt si sigue fija


        plt.title(str(round(t[i],3))+" [s]") #tiempo en segundos
        
        #limites del recuadro
        lim=5
        plt.xlim(0,6.5)
        plt.ylim(-2,2)
    ani = animation.FuncAnimation(fig, actualizar, range(len(t)))
    fig
    plt.show()

runProgram(m,L,h,ti,tf,A0,Ap0)