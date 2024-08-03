import requests
import mysql.connector
from bs4 import BeautifulSoup


###################################################
# Error 403 al hacer la petición, acceso denegado #
###################################################


print("\n")
print("Conexión a la base de datos realizada con exito")
print("\n")


# URL de la página web
url = 'https://www.dia.es/search?q=QUESO'

# Realizar la solicitud GET a la página web
response = requests.get(url)
if response.status_code != 200:

    print("Enlace que se intenta acceder: " + url)
    print(f"Error al acceder a la página: {response.status_code}")
else:
    print ("Petición realizada con éxito")



