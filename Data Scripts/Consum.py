import requests
import mysql.connector
from bs4 import BeautifulSoup


#########################################################
# No permite hacer peticiones ya que hay que activar JS #
#########################################################

# Configuración de la base de datos
config = {
    'user': 'salva',
    'password': 'Cerverus1',
    'host': 'localhost',
    'database': 'tfm'
}

# Conexion a la base de datos
conn = mysql.connector.connect(**config)
cursor = conn.cursor()

print("\n")
print("Conexión a la base de datos realizada con exito")
print("\n")


# URL de la página web
url = 'https://tienda.consum.es/es/s/queso%20?orderById=13&page=1'

# Realizar la solicitud GET a la página web
response = requests.get(url)
if response.status_code != 200:
    print(f"Error al acceder a la página: {response.status_code}")
else:
    # Analizar el contenido HTML de la página web
    soup = BeautifulSoup(response.text, 'html.parser')
    
   