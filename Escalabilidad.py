#!/usr/bin/env python
# coding: utf-8

# # W5 - Escalabilidad
# 
# * Oscar Juárez - 17315
# * Computación paralela y distribuida
# * Fecha: 11/02/2021
# 
# Programa interactivo de python que permite analizar si un programa es escalable, tomando en cuenta su Speedup, Eficiencia y un dominio creciente.

# **Funciones útiles a lo largo del programa**

# In[1]:


from math import log
import plotly.express as px
import pandas as pd


def SpeedupLineal(Ts, Tp):
    return Ts/Tp


def Eficiencia(n, p):
    return n/(n+p)


def TParalelo(n, p):
    return n/p + log(p)


def ObtenerDatos(p):
    for n in range(10, 330, 10):
        tparalelo = TParalelo(n, p)
        speedup = SpeedupLineal(n, tparalelo)
        yield speedup, Eficiencia(speedup, p)


# **Generación de los datos**

# In[2]:


dicc = {}
dicc['Dominio'] = [val for val in range(10, 330 ,10)]
for n in [1, 2, 4, 8, 16, 32]:
    data = list(ObtenerDatos(n))
    dicc[f'S{n}'] = [i[0] for i in data]
    dicc[f'E{n}'] = [i[1] for i in data]

df = pd.DataFrame(dicc)


# ## Speedup de cada núcleo en el dominio

# In[3]:


fig = px.line(df, x='Dominio', y=['S1','S2', 'S4', 'S8','S16', 'S32'],
             labels={
                 'value': 'Speedup',
                 'variable': 'Núcleos'
             },
             title='Speedup de Cada Núcleo por Dominio')
fig.show()


# ### Comentario del gráfico
# 
# En el gráfico del speedup se puede observar que este aumenta de manera logarítmica, proporcional a la cantidad de nucleos. Se denota una mejora en la ejecución del programa con diferentes tareas y se le saca el mejor provecho con una alta cantidad de núcleos.

# ## Eficiencia de cada núcleo en el dominio

# In[4]:


fig = px.line(df, x='Dominio', y=['E1','E2', 'E4', 'E8','E16', 'E32'],
             labels={
                 'value': 'Eficiencia',
                 'variable': 'Núcleos'
             },
             title='Eficiencia de Cada Núcleo por Dominio')
fig.show()


# ### Comentario del gráfico
# 
# La eficiencia de cada núcleo también depende de la cantidad de tareas que tengamos. Es decir, para un dominio muy bajo, la eficiencia de múchos núcleos será baja. Sin embargo, a medida que los núcleos y las tareas aumentan, la eficiencia de cada núcleo mejorará hasta llegar a su punto de rendimiento máximo.

# ## Proponemos un valor k
# 
# Se repetirá el procedimiento, esta vez proponiendo un valor de k de 2.5 (factor de crecimiento para los procesadores). Se tomará como base 16 núcleos.

# **Generación de los datos**

# In[5]:


k = 2.5
p = 32

dicc = {}
data = list(ObtenerDatos(p*k))
dicc['Dominio'] = [val for val in range(10,330,10)]
dicc['Eficiencia'] = [i[1] for i in data]

df = pd.DataFrame(dicc)


# **Se grafica nuevamente la eficiencia**

# In[6]:


fig = px.line(df, x='Dominio', y='Eficiencia',
             labels={'value': 'Eficiencia'},
             title='Eficiencia de 32 Núcleos por Dominio, con un Factor k de Crecimiento')
fig.show()


# ## ¿El programa es Escalable?

# El programa es **levemente escalable**, puesto que las unidades de procesamiento deberan de ser aumentadas a medida que se aumenta el tamaño del problema. De lo contrario, estaríamos perdiendo mucha eficiencia conforme más procesadores sean utilizados. Además, el gráfico se comporta de una forma muy similar con este nuevo factor de crecimiento, por lo que se entiende que a lo largo del tiempo la eficiencia se mantiene.
