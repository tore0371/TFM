import requests
import mysql.connector
from bs4 import BeautifulSoup

########################################################################################################
# No se tiene imágenes, el peso en algunos productos va en la descripción, no se tiene precio por kilo #
########################################################################################################

# Datos almacenados en Base de datos


# Configuración de la base de datos
config = {
    'user': 'salva',
    'password': 'Cerverus1',
    'host': 'localhost',
    'database': 'tfm'
}

# Conexión a la base de datos
conn = mysql.connector.connect(**config)
cursor = conn.cursor()

print("\n")
print("Conexión a la base de datos realizada con éxito")
print("\n")

# Crear la entrada del supermercado
supermarket_name = 'La casa de los quesos'
supermarket_location = 'Madrid'

insert_supermarket_query = """
INSERT INTO supermarket (Name, Zone)
VALUES (%s, %s)
"""


cursor.execute(insert_supermarket_query, (supermarket_name, supermarket_location))



# Obtener el ID autogenerado del supermercado
supermarket_id = cursor.lastrowid


# URL de la página web
url = 'https://lacasadelosquesos.com/tienda/'

# Realizar la solicitud GET a la página web
response = requests.get(url)
if response.status_code != 200:
    print(f"Error al acceder a la página: {response.status_code}")
else:
    # Analizar el contenido HTML de la página web
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Encontrar todos los productos en la página
    products = soup.find_all('div', class_='product-small box')
    
    for product in products:
        # Extraer el nombre del producto
        name_tag = product.find('a', class_='woocommerce-LoopProduct-link woocommerce-loop-product__link')
        name = name_tag.text.strip() if name_tag else 'N/A'
   
        # Extraer el precio del producto
        price_tag = product.find('span', class_='woocommerce-Price-amount amount')
        price_text = price_tag.text.strip() if price_tag else '0.00'
        try:
            price = float(price_text.replace('€', '').replace(',', '.').strip())
        except ValueError:
            price = 0.00

        # Inserción en la base de datos
        insert_product_query = """
        INSERT INTO supermarket_data (SupermarketID, ProductName, Price, Weight, KGPrice, ImageURL)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        
        cursor.execute(insert_product_query, (supermarket_id, name, price, 0.00, 0.00, 'N/A'))
        
        

    # Confirmar los cambios en la base de datos
    conn.commit()

    # Mostrar la información de los productos
    for product in products:
        name_tag = product.find('a', class_='woocommerce-LoopProduct-link woocommerce-loop-product__link')
        name = name_tag.text.strip() if name_tag else 'N/A'
   
        price_tag = product.find('span', class_='woocommerce-Price-amount amount')
        price_text = price_tag.text.strip() if price_tag else '0.00'
        try:
            price = float(price_text.replace('€', '').replace(',', '.').strip())
        except ValueError:
            price = 0.00

        print(f"Nombre: {name}")
        print(f"Precio: {price:.2f} €")
        print('-' * 30)

# Cerrar la conexión a la base de datos
cursor.close()
conn.close()
