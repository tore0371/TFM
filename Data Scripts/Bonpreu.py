import requests
import mysql.connector
from bs4 import BeautifulSoup
import re

# Script completado, falta imágenes
# Datos insertados en la BASE DE DATOS


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

# Inserta el supermercado "Bon Preu" en la zona "Barcelona"
insert_supermarket_query = """
INSERT INTO supermarket (Name, Zone) VALUES (%s, %s)
"""
supermarket_data = ("Bon Preu", "Barcelona")
cursor.execute(insert_supermarket_query, supermarket_data)

# Obtiene el ID del supermercado insertado
supermarket_id = cursor.lastrowid

# URL de la página web
url = 'https://www.compraonline.bonpreuesclat.cat/products/search?q=Queso'

# Realizar la solicitud GET a la página web
response = requests.get(url)
if response.status_code != 200:
    print(f"Error al acceder a la página: {response.status_code}")
else:
    # Analizar el contenido HTML de la página web
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Encontrar todos los productos en la página
    products = soup.find_all('div', class_='product-card-container')
    
    # Lista para almacenar la información de los productos
    product_list = []

    for product in products:
        # Extraer el nombre del producto
        name_tag = product.find('h3', class_='_text_f6lbl_1 _text--m_f6lbl_23')
        name = name_tag.text.strip() if name_tag else 'N/A'
   
        # Extraer el precio del producto
        price_tag = product.find('span', class_='_text_f6lbl_1 _text--m_f6lbl_23 sc-1fkdssq-0 eVdlkb')
        price = price_tag.text.strip() if price_tag else 'N/A'

        # Extraer el peso del producto
        weight_tag = product.find('span', class_='_text_f6lbl_1 _text--m_f6lbl_23 sc-1sjeki5-0 bUHwDh')
        weight = weight_tag.text.strip() if weight_tag else 'N/A'

        # Extraer el precio por kilo del producto
        price_per_kilo_tag = product.find('span', class_='_text_f6lbl_1 _text--m_f6lbl_23 sc-1vpsrpe-2 sc-bnzhts-0 exvQSw jIzHwa')
        price_per_kilo = price_per_kilo_tag.text.strip() if price_per_kilo_tag else 'N/A'
        
        # Extraer la URL de la imagen del producto
        image_tag = product.find('img', class_='image__StyledLazyLoadImage-sc-wislgi-0 foQxui')
        image_url = image_tag['srcset'] if image_tag else 'N/A'

        # Limpiar los datos extraídos
        price_value = float(price.replace('€', '').replace(',', '.').strip()) if price != 'N/A' else 0.0
        weight_value = float(weight.replace('kg', '').replace(',', '.').strip()) if weight != 'N/A' else 0.0
        price_per_kilo_clean = re.sub(r'[^\d.,]', '', price_per_kilo.replace(',', '.')).strip()
        kg_price_value = float(price_per_kilo_clean) if price_per_kilo_clean else 0.0

        product_info = {
            'name': name,
            'price': price_value,
            'weight': weight_value,
            'price_per_kilo': kg_price_value,
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
        print(f"Precio: {product['price']} €")
        print(f"Peso: {product['weight']} kg")
        print(f"Precio por kilo: ({product['price_per_kilo']} € per quilo)")
        print(f"URL de la imagen: {product['image_url']}")
        print('-' * 30)

# Cierra la conexión
cursor.close()
conn.close()

print("Datos insertados correctamente.")
