import requests
import mysql.connector
from bs4 import BeautifulSoup
import re

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

print("\nConexión a la base de datos realizada con éxito\n")

# Inserta el supermercado "Bonarea" en la zona "Barcelona"
insert_supermarket_query = """
INSERT INTO supermarket (Name, Zone) VALUES (%s, %s)
"""
supermarket_data = ("Bonarea", "Barcelona")
cursor.execute(insert_supermarket_query, supermarket_data)

# Obtiene el ID del supermercado insertado
supermarket_id = cursor.lastrowid

# URL de la página web
url = 'https://www.bonarea-online.com/es/shop/find?searchWords=queso'
# Realizar la solicitud GET a la página web
response = requests.get(url)
if response.status_code != 200:
    print(f"Error al acceder a la página: {response.status_code}")
else:
    # Analizar el contenido HTML de la página web
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Encontrar todos los productos en la página
    products = soup.find_all('div', class_='block-product block-product-shopping none')
    
    # Lista para almacenar la información de los productos
    product_list = []

    for product in products:
        # Extraer el nombre del producto (remover el peso del nombre)
        name_tag = product.find('div', class_='text')
        if name_tag:
            name_text = name_tag.text.strip()
            # Usar regex para separar el nombre del peso
            name_match = re.match(r'(.*?)(\d+(?:,\d+)?\s?g|kg)?$', name_text)
            name = name_match.group(1).strip() if name_match else 'N/A'
        else:
            name = 'N/A'

        # Extraer el precio del producto
        price_tag = product.find('div', class_='price')
        price_text = price_tag.text.strip() if price_tag else 'N/A'

        # Extraer el peso del producto
        weight_tag = product.find('div', class_='weight')
        weight_text = weight_tag.text.strip() if weight_tag else 'N/A'

        # Extraer la URL de la imagen del producto
        image_tag = product.find('img', class_='img-fluid lazyload')
        image_url = image_tag['data-src'] if image_tag else 'N/A'

        # Limpiar los datos extraídos
        # Separar el precio unitario y el precio por kilo
        price_match = re.search(r'(\d+,\d+)\s€/u\.\s\((\d+,\d+)\s€/kg\)', price_text)
        if price_match:
            unit_price = float(price_match.group(1).replace(',', '.'))
            kg_price = float(price_match.group(2).replace(',', '.'))
        else:
            unit_price = kg_price = 0.0

        # Convertir el peso a kilogramos
        weight_match = re.search(r'aprox\.\s(\d+(?:,\d+)?)\s?(g|kg)?', weight_text)
        if weight_match:
            weight_value = float(weight_match.group(1).replace(',', '.'))
            weight_unit = weight_match.group(2)
            if weight_unit == 'g':
                weight_value /= 1000  # Convertir gramos a kilogramos
        else:
            weight_value = 0.0

        product_info = {
            'name': name,
            'price': unit_price,
            'weight': weight_value,
            'price_per_kilo': kg_price,
            'image_url': image_url
        }
        product_list.append(product_info)

    # Inserta datos en la tabla supermarket_data
    insert_product_query = """
    INSERT INTO supermarket_data (SupermarketID, ProductName, Price, Weight, KGPrice, ImageURL) 
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    for product in product_list:
        product_data = (supermarket_id, product['name'], product['price'], product['weight'], product['price_per_kilo'], product['image_url'])
        cursor.execute(insert_product_query, product_data)

    # Confirma las inserciones
    conn.commit()

    # Mostrar la información de los productos
    for product in product_list:
        print(f"Nombre: {product['name']}")
        print(f"Precio: {product['price']} €/u.")
        print(f"Peso: aprox. {product['weight']} kg")
        print(f"Precio por kilo: {product['price_per_kilo']} €/kg")
        print(f"URL de la imagen: {product['image_url']}")
        print('-' * 30)

# Cierra la conexión
cursor.close()
conn.close()

print("Datos insertados correctamente.")
