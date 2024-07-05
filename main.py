import requests
import random
import urllib3
import pandas as pd

# Suprimir solo la advertencia InsecureRequestWarning de urllib3 necesaria para pruebas
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Endpoints para los cheques denunciados y entidades
URL_ENTIDADES = 'https://api.bcra.gob.ar/cheques/v1.0/entidades'
URL_DENUNCIADOS = 'https://api.bcra.gob.ar/cheques/v1.0/denunciados'

# Cargar el DataFrame existente de cheques denunciados
try:
    df_existente = pd.read_csv('cheques_denunciados.csv')
except FileNotFoundError:
    # Si el archivo no existe, inicializar un DataFrame vacío con las columnas adecuadas
    df_existente = pd.DataFrame(columns=['denunciado', 'fechaProcesamiento', 'denominacionEntidad', 'sucursal', 'numeroCuenta', 'causal'])

def get_json(url):
    """
    Hace una solicitud GET y transforma la respuesta en un objeto JSON.
    """
    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()  # Lanza un error para códigos de estado no exitosos
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud: {e}")
        return None
    except ValueError:
        print(f"No se pudo parsear la respuesta JSON de {url}")
        return None

def fetch_entidades():
    """
    Obtiene datos del endpoint de entidades.
    """
    data = get_json(URL_ENTIDADES)
    if data is None or 'status' in data and data['status'] != 200:
        print(f"Error: {data}")
        exit()
    return data.get('results', [])

def fetch_denunciados(codigoEntidad, unique_identifier):
    """
    Obtiene datos del endpoint de denunciados para una entidad y un identificador dados.
    """
    denunciados_url = f"{URL_DENUNCIADOS}/{codigoEntidad}/{unique_identifier}"
    data_denunciados = get_json(denunciados_url)
    if data_denunciados is None:
        print(f"Error: No se devolvió datos para la URL {denunciados_url}")
        return None
    if 'status' in data_denunciados and data_denunciados['status'] != 200:
        print(f"Error: {data_denunciados} para la URL {denunciados_url}")
        return None
    return data_denunciados.get('results', {})

def agregar_a_df(df, cheque, denominacionEntidad):
    """
    Agrega un cheque a un DataFrame utilizando pd.concat.
    """
    if isinstance(cheque, dict):
        cheque_df = pd.DataFrame([{
            'denunciado': cheque.get('denunciado', None),
            'fechaProcesamiento': cheque.get('fechaProcesamiento', None),
            'denominacionEntidad': denominacionEntidad,
            'sucursal': cheque.get('detalle', {}).get('sucursal', None),
            'numeroCuenta': cheque.get('detalle', {}).get('numeroCuenta', None),
            'causal': cheque.get('detalle', {}).get('causal', None)
        }])
        return pd.concat([df, cheque_df], ignore_index=True)
    else:
        print(f"Formato inesperado del cheque: {cheque}")
        return df

def main():
    """
    Función principal para obtener y procesar datos de la API.
    """
    global df_existente  # Asegura que se esté utilizando la variable global df_existente

    # Obtener entidades y construir el diccionario
    entidades = fetch_entidades()
    entidad_dict = {banco['codigoEntidad']: banco['denominacion'] for banco in entidades}

    # Iterar sobre cada entidad
    for banco in entidades:
        print(banco['denominacion'])
        codigoEntidad = banco['codigoEntidad']
        denominacionEntidad = entidad_dict.get(codigoEntidad, 'Desconocido')

        # Intentar varias veces con identificadores aleatorios
        for _ in range(200):  # Ajustar el rango para más intentos si es necesario
            unique_identifier = str(random.randint(0, 1000000))
            results = fetch_denunciados(codigoEntidad, unique_identifier)

            if results is None:
                continue

            # Agregar los detalles de cada cheque al DataFrame
            if isinstance(results, dict):
                df_existente = agregar_a_df(df_existente, results, denominacionEntidad)

    # Mostrar los primeros 5 registros
    print(df_existente.head())
    print(df_existente.shape)

    # Guardar el DataFrame actualizado en el archivo CSV, sobrescribiendo el archivo existente
    df_existente.to_csv('cheques_denunciados.csv', index=False)

if __name__ == "__main__":
    main()
