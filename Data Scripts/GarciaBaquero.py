import requests
import mysql.connector
from bs4 import BeautifulSoup

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
supermarket_name = 'García Baquero'
supermarket_location = 'Toro'

insert_supermarket_query = """
INSERT INTO supermarket (Name, Zone)
VALUES (%s, %s)
"""


cursor.execute(insert_supermarket_query, (supermarket_name, supermarket_location))

# Obtener el ID autogenerado del supermercado
supermarket_id = cursor.lastrowid


# URL de la página web
url = 'https://tienda.garciabaquero.com/es/'

# Realizar la solicitud GET a la página web
response = requests.get(url)
if response.status_code != 200:
    print(f"Error al acceder a la página: {response.status_code}")
else:
    # Analizar el contenido HTML de la página web
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Encontrar todos los productos en la página
    products = soup.find_all('div', class_='product-miniature-container')
    
    for product in products:
        # Extraer el nombre del producto
        name_tag = product.find('h1', class_='product-title')
        name = name_tag.text.strip() if name_tag else 'N/A'
   
        # Extraer el precio del producto
        price_tag = product.find('span', class_='price')
        price_text = price_tag.text.strip() if price_tag else '0.00'
        try:
            price = float(price_text.replace('€', '').replace(',', '.').strip())
        except ValueError:
            price = 0.00

        # Extraer el peso del producto (valor predeterminado a 0)
        weight = 0.00
        
        # Extraer el precio por kilo del producto (valor predeterminado a 0)
        kg_price = 0.00
        
        # Extraer la URL de la imagen del producto
        image_tag = product.find('a', class_='product-thumbnail-link')
        img_url = 'N/A'
        if image_tag:
            img = image_tag.find('img')
            if img and 'data-full-size-image-url' in img.attrs:
                img_url = img['data-full-size-image-url']

        # Insertar los datos del producto en la base de datos
        insert_product_query = """
        INSERT INTO supermarket_data (SupermarketID, ProductName, Price, Weight, KGPrice, ImageURL)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        
        cursor.execute(insert_product_query, (supermarket_id, name, price, weight, kg_price, img_url))
        
    # Confirmar los cambios en la base de datos
    conn.commit()

    # Mostrar la información de los productos
    for product in products:
        name_tag = product.find('h1', class_='product-title')
        name = name_tag.text.strip() if name_tag else 'N/A'
   
        price_tag = product.find('span', class_='price')
        price_text = price_tag.text.strip() if price_tag else '0.00'
        try:
            price = float(price_text.replace('€', '').replace(',', '.').strip())
        except ValueError:
            price = 0.00

        # Extraer la URL de la imagen del producto
        image_tag = product.find('a', class_='product-thumbnail-link')
        img_url = 'N/A'
        if image_tag:
            img = image_tag.find('img')
            if img and 'data-full-size-image-url' in img.attrs:
                img_url = img['data-full-size-image-url']

        print(f"Nombre: {name}")
        print(f"Precio: {price:.2f} €")
        print(f"Peso: {weight:.2f} kg")
        print(f"Precio por kilo: {kg_price:.2f} €")
        print(f"URL de la imagen: {img_url}")
        print('-' * 30)

# Cerrar la conexión a la base de datos
cursor.close()
conn.close()
