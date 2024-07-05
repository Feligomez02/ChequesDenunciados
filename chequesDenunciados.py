import pandas as pd
import matplotlib.pyplot as plt

# Cargar los datos
data = pd.read_csv('cheques_denunciados.csv')

# Convertir la columna fechaProcesamiento a datetime
data['fechaProcesamiento'] = pd.to_datetime(data['fechaProcesamiento'])



# Convertir columnas a tipo string
data['denominacionEntidad'] = data['denominacionEntidad'].astype(str)
data['causal'] = data['causal'].astype(str)

# Convertir el nan de la columna causal a 'No denunciado'
data['causal'] = data['causal'].replace('nan', 'No denunciado')

# Mostrar información sobre el DataFrame
data.info()

# Función para obtener la cantidad de cheques denunciados por entidad
def cheques_por_entidad(data):
    # Filtrar solo los cheques denunciados
    denunciados = data[data['denunciado'] == True]
    print(denunciados)
    # Contar cheques por entidad
    return denunciados['denominacionEntidad'].value_counts()

# Obtener la cantidad de cheques denunciados por entidad
denunciados_por_entidad = cheques_por_entidad(data)
print(denunciados_por_entidad)

# Obtener la cantidad de cheques denunciados por causal
cheques_por_causal = data['causal'].value_counts()
print(cheques_por_causal)

# Graficar la cantidad de cheques denunciados por entidad
denunciados_por_entidad.plot(kind='bar')
plt.title('Cantidad de cheques denunciados por entidad')
plt.xlabel('Entidad')
plt.ylabel('Cantidad de cheques')
plt.xticks(fontsize=5)  # Ajustar el tamaño de las etiquetas del eje x
plt.show()

# Graficar la cantidad de cheques denunciados por causal
cheques_por_causal.plot(kind='pie', autopct='%1.1f%%')
plt.title('Cantidad de cheques denunciados por causal')
plt.show()

# Ratio de cheques denunciados por entidad
total_cheques_por_entidad = data['denominacionEntidad'].value_counts()

def ratio_cheques_por_entidad(data):
    denunciados = data[data['denunciado'] == True]
    denunciados_por_entidad = denunciados['denominacionEntidad'].value_counts()
    ratio = denunciados_por_entidad / total_cheques_por_entidad
    return ratio

# Obtener el ratio de cheques denunciados por entidad
ratio_cheques = ratio_cheques_por_entidad(data)
print(ratio_cheques)

# Graficar el ratio de cheques denunciados por entidad
ratio_cheques.plot(kind='bar')
plt.title('Ratio de cheques denunciados por entidad')
plt.xlabel('Entidad')
plt.ylabel('Ratio de cheques denunciados')
plt.xticks(fontsize=5)
plt.show()
