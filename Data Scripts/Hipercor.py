import requests
import mysql.connector
from bs4 import BeautifulSoup

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
url = 'https://www.hipercor.es/supermercado/buscar/?term=queso&search=text'

###############################################
# NO PERMITE HACER PETICIONES GET A LA PÁGINA #
###############################################

# Realizar la solicitud GET a la página web
response = requests.get(url)
if response.status_code != 200:
    print(f"Error al acceder a la página: {response.status_code}")
else:
    print("Entre")
    # Analizar el contenido HTML de la página web
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Encontrar todos los productos en la página
    products = soup.find_all('div', class_='grid-item   product_tile _retro _hipercor  dataholder js-product')
    
    # Lista para almacenar la información de los productos
    product_list = []

    for product in products:
        # Extraer el nombre del producto
        name_tag = product.find('a', class_='link event js-product-link')
        name = name_tag.text.strip() if name_tag else 'N/A'
   
        # Extraer el precio del producto
        price_tag = product.find('strong', class_='base__Price-sc-1mnb0pd-29 sc-ieebsP iDLLj eyJUgq')
        price = price_tag.text.strip() if price_tag else 'N/A'

        # Extraer el peso del producto
        weight_tag = product.find('span', class_='text__Text-sc-6l1yjp-0 base__SizeText-sc-1mnb0pd-38 fop__SizeText-sc-sgv9y1-4 bhymDA iImbUZ jrvLpU')
        weight = weight_tag.text.strip() if weight_tag else 'N/A'

        # Extraer el precio por kilo del producto
        price_per_kilo_tag = product.find('span', class_='_text_f6lbl_1 _text--m_f6lbl_23 standard-promotion__PromotionIntentText-sc-1vpsrpe-2 fop__PricePerText-sc-sgv9y1-5 jVJmKC eNYENy')
        price_per_kilo = price_per_kilo_tag.text.strip() if price_per_kilo_tag else 'N/A'
        
        # Extraer la URL de la imagen del producto
        image_tag = product.find('img', class_='fop__Image-sc-sgv9y1-2 daCdrp')
        image_url = image_tag['src'] if image_tag else 'N/A'

        product_info = {
            'name': name,
            'price': price,
            'weight': weight,
            'price_per_kilo': price_per_kilo,
            'image_url': image_url
        }
        product_list.append(product_info)

    # Mostrar la información de los productos
    for product in product_list:
        print(f"Nombre: {product['name']}")
        print(f"Precio: {product['price']}")
        print(f"Peso: {product['weight']}")
        print(f"Precio por kilo: {product['price_per_kilo']}")
        print(f"URL de la imagen: {product['image_url']}")
        print('-' * 30)
