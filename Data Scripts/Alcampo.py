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

# Inserta el supermercado "Alcampo" en la zona "Madrid"
insert_supermarket_query = """
INSERT INTO supermarket (Name, Zone) VALUES (%s, %s)
"""


supermarket_data = ("Alcampo", "Madrid")
cursor.execute(insert_supermarket_query, supermarket_data)

# Obtiene el ID del supermercado insertado
supermarket_id = cursor.lastrowid



# URL de la página web
url = 'https://www.compraonline.alcampo.es/categories/frescos/quesos/OCQuesos'

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
        # Extraer el nombre del producto (remover el peso del nombre)
        name_tag = product.find('h3', class_='_text_f6lbl_1 _text--m_f6lbl_23')
        name_text = name_tag.text.strip() if name_tag else 'N/A'
        name_match = re.match(r'(.*?)(\d+(?:,\d+)?\s?(g|kg))$', name_text)
        name = name_match.group(1).strip() if name_match else name_text

        # Extraer el precio del producto
        price_tag = product.find('span', class_='_text_f6lbl_1 _text--m_f6lbl_23 sc-1fkdssq-0 eVdlkb')
        price_text = price_tag.text.strip() if price_tag else 'N/A'
        price = float(price_text.replace('€', '').replace(',', '.').strip()) if '€' in price_text else 0.0

        # Extraer el peso del producto
        weight_tag = product.find('span', class_='_text_f6lbl_1 _text--m_f6lbl_23 sc-1sjeki5-0 bUHwDh')
        weight_text = weight_tag.text.strip() if weight_tag else 'N/A'
        weight_match = re.search(r'(\d+(?:,\d+)?)\s?(g|kg)', weight_text)
        if weight_match:
            weight_value = float(weight_match.group(1).replace(',', '.'))
            weight_unit = weight_match.group(2)
            if weight_unit == 'g':
                weight_value /= 1000  # Convertir gramos a kilogramos
        else:
            weight_value = 0.0

        # Extraer el precio por kilo del producto
        price_per_kilo_tag = product.find('span', class_='_text_f6lbl_1 _text--m_f6lbl_23 sc-1vpsrpe-2 sc-bnzhts-0 eySopN jIzHwa')
        price_per_kilo_text = price_per_kilo_tag.text.strip() if price_per_kilo_tag else 'N/A'
        price_per_kilo_match = re.search(r'\((\d+,\d+)\s?€\s?por\s?kilogramo\)', price_per_kilo_text)
        price_per_kilo = float(price_per_kilo_match.group(1).replace(',', '.')) if price_per_kilo_match else 0.0
        
        # Extraer la URL de la imagen del producto
        image_tag = product.find('img', class_='image__StyledLazyLoadImage-sc-wislgi-0 foQxui')
        image_url = image_tag['srcset'] if image_tag else 'N/A'

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
        print(f"Precio: {product['price']} ")
        print(f"Peso: {product['weight']}")
        print(f"Precio por kilo: {product['price_per_kilo']}")
        print(f"URL de la imagen: {product['image_url']}")
        print('-' * 30)

# Cierra la conexión
cursor.close()
conn.close()

print("Datos insertados correctamente.")
