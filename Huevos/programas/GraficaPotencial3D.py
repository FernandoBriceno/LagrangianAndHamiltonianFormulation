import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Definir las constantes
m = 1
g = 9.8
L = 1
E=5

# Crear un rango de valores de X y Y
x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)

# Crear una cuadrícula de valores de X y Y
X, Y = np.meshgrid(x, y)

# Calcular los valores correspondientes de Z
Z = m * g * (L * np.cos(Y) + np.sin(X))

# Limitar los valores de Z a un máximo de Zcorte
Zlimite = np.clip(Z, None, E)

# Crear la figura y los ejes
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Graficar la superficie
ax.plot_surface(X, Y, Zlimite, cmap='Blues')

# Agregar el plano Z = 5
Z_plano_5 = np.full((100, 100), E)
ax.plot_surface(X, Y, Z_plano_5, alpha=0.5, color='green')

# Agregar etiquetas a los ejes
ax.set_xlabel('x')
ax.set_ylabel('A')
ax.set_zlabel('U')

# Agregar la leyenda
ax.text(-5, -5, 30, r'$U(x,A) = m \times g \times (L \times cos(A) + sin(x))$')

# Crear la gráfica de corte
Zcorte = E
levels = [Zcorte]
contours = ax.contour(X, Y, Z, levels=levels, colors='red')

# Cambiar el color de la curva de corte a rojo
for contour in contours.collections:
    contour.set_color('red')

# Mostrar la gráfica
plt.show()

