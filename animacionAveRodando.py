import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

z=3  #Grado de aceleración del limpiavidrios
a=0.3   #Radio de gordura del ave
g=10
M=0.2   #Masa del limpiavidrios
m=0.3   #Masa del ave
L=4    #Longitud del limpiavidrios
A0=0    #Ángulo inicial
tlim = np.pi/(2*z)  #El tiempo en el que la velocidad angular comienza a disminuir
h=0.01 #El paso del tiempo
ti=0    #tiempo inicial
tf=5  #tiempo final
r0=3    #Valor inicial de la coordenada r
rp0=0   #Valor inicial de la coordenada r'


def runProgram(z,a,g,M,m,L,A0,tlim,h,ti,tf,r0,rp0):
    def angulo(z,t):
        return (np.pi/4)*(1-np.cos(z*t)) + A0
    def W(z,t):
        return (np.pi/4)*np.sin(z*t)*z
    def ALFA(z,t):
        return (np.pi/4)*np.cos(z*t)*z*z
    def vx_vy(t,R,Rp,w,A):
        vx=Rp*np.cos(A)-R*np.sin(A)*w-a*np.cos(A)*w
        vy=Rp*np.sin(A)+R*np.cos(A)*w-a*np.sin(A)*w
        return vx, vy    
    def valoresI(t0,R,Rp,th,z):#No SE USA
        w=W(z,t0)
        v0x,v0y = vx_vy(t0,R,Rp,z)
        x0=R*np.cos(th)-a*np.sin(th)#x[]
        y0=R*np.sin(th)+a*np.cos(th)#[]
        return x0,y0,v0x,v0y
    def xf(t,x0,v0x):
        return x0+v0x*t
    def yf(t,y0,v0y):
        return y0+v0y*t-(1/2)*g*t**2
    def F1(t,y,Y):
        return Y 

    def F2(t,y,Y):
        A=(7*M*(L**2))/(12*m)+(a**2)
        B=(M*L)/(2*m)
        x=angulo(z,t)
        w=W(z,t)
        #alfa=ALFA(z,t)
        f2= 2*a*g*(a*np.sin(x)-(B+y)*np.cos(x)) - 4*a*y*Y*w + 2*(A+(y**2))*(y*(w**2)-g*np.sin(x))/(3*(A+(y**2))-2*(a**2))
        #f2= (g*((a+1)*np.sin(x)-(B+y)*np.cos(x)) - 2*y*Y*w + (A+a+(y**2))*(alfa)-y*w**2)/(a-(3/2))
        
        return f2 #f2

    def rungeKuta4(f1,f2,a,b,y0,yp0,h):
        #N=(b-a)//h
        N=int((b-a)/h)
        t=np.arange(a, b+h, h, dtype=float)
        #t=np.zeros(N+1)
        t[0]=a
        y=np.zeros(N+1)
        y[0]=y0
        Y=np.zeros(N+1)
        Y[0]=yp0
        
        for i in range(0,N):
            #t[i+1]
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
    t,r,rp = rungeKuta4(F1,F2,ti,tf,r0,rp0,h)

    theta=angulo(z,t) #Th[]
    x=r*np.cos(theta)-a*np.sin(theta) #x[]
    y=r*np.sin(theta)+a*np.cos(theta) #y[]
    w = W(z,t) #w[]

    #posiciones de la cabeza antes de soltarse
    def x_y_cabeza(a,ri,rf,x,y,alfa0):
        alfa= -(1/a)*(rf-ri)
        xc=x-a*np.sin(alfa)
        yc=y+a*np.cos(alfa)
        return xc,yc, alfa
    #posiciones de la cabeza después de soltarse
    def x_y_cabeza2(a,vr0,x2,y2,t,alfa0):
        alfa= alfa0-(vr0/a)*t
        xc2=x2-a*np.sin(alfa)
        yc2=y2+a*np.cos(alfa)
        return xc2,yc2

    xc,yc, alfa=x_y_cabeza(a,r0,r,x,y,0)

    def Vx_Vy(x,y,h): #velocidades en x e y
        vx=np.zeros(len(x))
        vy=np.zeros(len(x))
        for i in range(0, len(x)):
            if i==0:
                vx[i]=0
                vy[i]=0
            else:
                vx[i]=(x[i]-x[i-1])/h
                vy[i]=(y[i]-y[i-1])/h
        return vx, vy
    vx , vy = Vx_Vy(x,y,h)

    def vr(r,h): #velocida r'
        vr=np.zeros(len(r))
        for i in range(0, len(r)):
            if i==0:
                vr[i]=0
            else:
                vr[i]=(r[i]-r[i-1])/h
        return vr
    vr=vr(r,h)


    x2,y2=np.zeros(len(t)),np.zeros(len(t))
    xc2,yc2=np.zeros(len(t)),np.zeros(len(t))
    for i in range(0,len(t)): #nuevos valores para la posición, cuando se despega del limpiavidrios
        if t[i] < tlim and r[i]<=L and r[i]>=0 :
            x2[i]=x[i]
            y2[i]=y[i]

            xc2[i],yc2[i]= xc[i],yc[i]

            #condiciones iniciales despues de soltarse
            t0=t[i+1]
            x0,y0 = x[i+1] , y[i+1]
            v0x,v0y = vx[i+1] , vy[i+1]

            alfa0 = alfa[i+1]
            vr0 = vr[i+1]

        else:
            T=t[i]-t0 #inicia en T=0
            x2[i]=xf(T,x0,v0x)
            y2[i]=yf(T,y0,v0y)
            xc2[i],yc2[i]=x_y_cabeza2(a,vr0,x2[i],y2[i],T,alfa0) #Rellena las posiciones de la cabeza

    #*******GRAFICANDO*******************

    fig = plt.figure()
    ax=fig.gca()


    def recta(i): #pinta el limpia parabrisas
        l=L
        th=angulo(z,t[i])
        x=[0,l*np.cos(th)]
        y=[0,l*np.sin(th)]
        plt.plot(x,y, 'k')

    def recta2(i): #pinta el limpia parabrisas largo punteado
        l=2*L
        th=angulo(z,t[i])
        x=[-l*np.cos(th),l*np.cos(th)]
        y=[-l*np.sin(th),l*np.sin(th)]
        plt.plot(x,y, 'y--')

    def rectaVelx(i): #vector velocidad en x
        velx1=[x[i],x[i]+(vx[i-1]/10)]
        velx2=[y[i],y[i]]
        return velx1,velx2
    def rectaVely(i): #vector velocidad en y
        vely1=[x[i],x[i]]
        vely2=[y[i],y[i]+(vy[i-1]/10)]
        return vely1,vely2
    def ventana(L): #pinta la ventana
        h1=[[-(L+0.5),L+0.5],[L+0.5,L+0.5]]
        h2=[[-(L+0.5),L+0.5],[0,0]]
        vpunto=[[0,0],[0,L+0.5]]
        v1=[[-(L+0.5),-(L+0.5)],[0,L+0.5]]
        v2=[[L+0.5,L+0.5],[0,L+0.5]]
        color= 'c'

        plt.plot(h1[0],h1[1], color)
        plt.plot(h2[0],h2[1], color)
        plt.plot(vpunto[0],vpunto[1], color+'--')
        plt.plot(v1[0],v1[1], color)
        plt.plot(v2[0],v2[1], color)
    def velocidades(i): #pinta los vectores velocidades vx y vy
        velx1,velx2=rectaVelx(i)
        vely1,vely2=rectaVely(i)
        color='w'
        plt.plot(velx1,velx2, color)
        plt.plot(vely1,vely2, color)
        
    def actualizar(i) :
        
        ax.clear()

        ventana(L)
        velocidades(i)
        recta2(i)
        recta(i)
        

        #plot trayectorias centro de masa
        plt.plot(x2[:i+1],y2[:i+1], 'b')
        plt.plot(x[:i+1],y[:i+1], 'r')
        
        
        #plot trayectorias de la cabeza
        plt.plot(xc2[:i+1],yc2[:i+1], 'b--') #la cabeza del ave si se suelta
        plt.plot(xc[:i+1],yc[:i+1], 'r--') #la cabeza del ave si no se suelta
        

        #plot las masas

        plt.plot(x[i],y[i], 'mo',markersize=20) #plt si sigue fija
        plt.plot(x2[i],y2[i], 'mo',markersize=20) #plt si se suelta enalgún momento

        plt.plot(xc2[i],yc2[i], 'bo',markersize=5) #la cabeza del ave si se suelta
        plt.plot(xc[i],yc[i], 'ro',markersize=5) #la cabeza del ave si no se suelta
        
        plt.title(str(round(t[i],3))+" [s]") #tiempo en segundos
        
        #limites del recuadro
        lim=5
        plt.xlim(-8,L+1)
        plt.ylim(-4,L+1)
    ani = animation.FuncAnimation(fig, actualizar, range(len(t)))
    fig
    plt.show()

runProgram(z,a,g,M,m,L,A0,tlim,h,ti,tf,r0,rp0)