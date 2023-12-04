import textract

# Ruta del archivo PDF correcta
pdf_path = './data/data/ACCOUNTANT/10554236.pdf'

print("Script iniciado...")

print("Ruta del PDF:", pdf_path)

# Extraer el texto del PDF
try:
    text = textract.process(pdf_path).decode('utf-8')
except Exception as e:
    error_message = str(e)
    text = None
    print("Error:", error_message)

if text:
    print("Texto extraído con éxito.")
    print("Primeros 500 caracteres del texto:")
    print(text[:500])
else:
    print(f"Error al extraer texto: {error_message}")