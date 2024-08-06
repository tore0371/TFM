import requests
import mysql.connector
from bs4 import BeautifulSoup
import re

# Scrtipt ccompleto
# Datos insertados en la base de datos

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

# Inserta el supermercado "Eroski" en la zona "Madrid"
insert_supermarket_query = """
INSERT INTO supermarket (Name, Zone) VALUES (%s, %s)
"""


supermarket_data = ("Eroski", "Madrid")
cursor.execute(insert_supermarket_query, supermarket_data)

# Obtiene el ID del supermercado insertado
supermarket_id = cursor.lastrowid



# URL de la página web
url = 'https://supermercado.eroski.es/es/search/results/?q=queso&suggestionsFilter=false'

# Realizar la solicitud GET a la página web
response = requests.get(url)
if response.status_code != 200:
    print(f"Error al acceder a la página: {response.status_code}")
else:
    # Analizar el contenido HTML de la página web
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Encontrar todos los productos en la página
    products = soup.find_all('div', class_='col col-xs-12 col-sm-12 col-md-12 col-lg-12 product-item big-item')
    
    # Lista para almacenar la información de los productos
    product_list = []

    for product in products:
        # Extraer el nombre del producto
        name_tag = product.find('h2', class_='product-title')
        name = name_tag.text.strip() if name_tag else 'N/A'
   
        # Extraer el precio del producto
        price_tag = product.find('span', class_='price-now')
        price_text = price_tag.text.strip() if price_tag else 'N/A'
        price = float(price_text.replace('Ahora ', '').replace('€', '').replace(',', '.').strip()) if '€' in price_text else 0.0

        # Extraer el peso del producto
        weight_match = re.search(r'(\d+(?:,\d+)?)\s?(g|kg)', name)
        if weight_match:
            weight_value = float(weight_match.group(1).replace(',', '.'))
            weight_unit = weight_match.group(2)
            if weight_unit == 'g':
                weight_value /= 1000  # Convertir gramos a kilogramos
        else:
            weight_value = 0.0

        price_per_kilo_tag = product.find('span', class_='price-product')
        price_per_kilo_text = price_per_kilo_tag.text.strip() if price_per_kilo_tag else 'N/A'

        # Ajustar la expresión regular para capturar precios con formato como "16,13 €"
        price_per_kilo_match = re.search(r'(\d+(?:,\d+)?)\s?€', price_per_kilo_text)
        if price_per_kilo_match:
            price_per_kilo = float(price_per_kilo_match.group(1).replace(',', '.'))
        else:
            price_per_kilo = 0.0
        
        # Extraer la URL de la imagen del producto
        image_tag = product.find('img', class_='product-img')
        image_url = image_tag['data-bigimage'] if image_tag else 'N/A'

        product_info = {
            'name': name,
            'price': price,
            'weight': weight_value,
            'price_per_kilo': price_per_kilo,
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
        print(f"Precio: {product['price']}")
        print(f"Peso: {product['weight']}")
        print(f"Precio por kilo: {product['price_per_kilo']}")
        print(f"URL de la imagen: {product['image_url']}")
        print('-' * 30)

# Cierra la conexión
cursor.close()
conn.close()

print("Datos insertados correctamente.")
