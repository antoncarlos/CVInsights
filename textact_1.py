import boto3

# Configura las credenciales de AWS (asegúrate de configurarlas previamente)
aws_access_key_id = 'ASIAWXHXR6QILVE2D4RY'
aws_secret_access_key = 'w8pLzOpxWadBw43cyirVwncYh/VIkbHUQe+LTCGS'
aws_session_token = 'FwoGZXIvYXdzEE0aDKMivTjQlg7ODe68FCLSAXElSfYKoNzIYgmaHcirZzvahx7hoKuGh4/IsWFp5MVlJSoNeCrJG4h1RSHTcWcsnuXfTVCs7CMDqTXNjoJfK7Av1g3vcIBcHj9M2uOMe5iqyFzX+59sFaQPk5+srAGFHBP8depNYPrLcMy/xK2WF/UO7HKx3OgdlJOILHpqIHQdG/fGPpGc1fvrKollMKkVjwZxOhI/7DoHenj0U40Y3Fc4rV4CejOv3jxFlKFOpRKKYyM8K/XJcT0UKF2qOAuDsVzBUa4CoQtPKpJJCrZMx1WpDyiIvo6rBjItufCMYptlrTO7KZ1YbRiu4gySn/3Mdb4prhIpdbSLHi7FwLZh/Z0ThqwGhbYl'
region_name = 'us-east-1'

# Crea un cliente de Textract con aws_session_token
textract_client = boto3.client('textract', 
                               aws_access_key_id=aws_access_key_id, 
                               aws_secret_access_key=aws_secret_access_key, 
                               aws_session_token=aws_session_token, 
                               region_name=region_name)

# Especifica el nombre del archivo de tu CV en el directorio actual
file_name = './data/data/ACCOUNTANT/10554236.pdf'  # Cambia el nombre del archivo según corresponda

# Lee el contenido del archivo
with open(file_name, 'rb') as file:
    document_bytes = file.read()

# Llama a Textract para analizar el documento
response = textract_client.analyze_document(
    Document={
        'Bytes': document_bytes
    },
    FeatureTypes=['FORMS']
)

# Procesa la respuesta para extraer la información
for item in response['Blocks']:
    if item['BlockType'] == 'LINE':
        print(item['Text'])
