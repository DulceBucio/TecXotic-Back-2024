# Gráfica 3D pero no es la q sirve para el copiloto, se puede hacer con Three.js pero ta bn dificil ;(

import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Creando el DataFrame
data = {
    "Day": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    "Receiver_1": [3, 3, 0, 0, 1, 1, 1, 1, 3, 2, 0, 2, 3, 2, 0],
    "Receiver_2": [4, 3, 8, 8, 13, 10, 8, 4, 3, 1, 2, 1, 0, 1, 2],
    "Receiver_3": [3, 2, 5, 6, 3, 2, 3, 3, 2, 2, 3, 2, 1, 0, 1]
}
df = pd.DataFrame(data)

# Preparando datos para el gráfico
X = df["Day"].values
Z = df.values[:, 1:].T  # Transponemos para tener cada receiver como una fila

# Gráfico
fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(111, projection='3d')

# Configurando ejes
ax.set_xlabel('Día')
ax.set_ylabel('Receiver')
ax.set_zlabel('Valor')
ax.set_title('Valores de Receiver por Día en Barras')

# Colores para cada receiver
colors = ['r', 'g', 'b']

# Graficando en barras
for i, receiver in enumerate(Z, start=1):
    for j, val in enumerate(receiver):
        ax.bar3d(X[j]-0.25, i, 0, 0.5, 0.1, val, color=colors[i-1], shade=True)

plt.show()
