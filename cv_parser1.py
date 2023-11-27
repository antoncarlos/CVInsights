import docx2txt
import nltk
import re

#
# Descarga los recursos necesarios para nltk
nltk.download('punkt')
nltk.download('stopwords')

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

# Función para extraer educación
def extract_education(text):
    # Aquí debes implementar la lógica para extraer información sobre la educación.
    # Puedes usar expresiones regulares o procesamiento de texto para buscar patrones relevantes.
    # Por ejemplo, buscar palabras clave como "educación", "título", "universidad", etc.

    # Ejemplo de expresión regular para buscar títulos académicos:
    education_pattern = r"(?i)(?:estudi(o|os)|graduad(o|os)|maestr(o|os)|doctor(ado|ados)|ingenier(o|os))(?:\s\w+)?\s(?:en\s)?\w+"
    education_matches = re.findall(education_pattern, text)
    
    return education_matches

# Función para extraer experiencia profesional
def extract_experience(text):
    # Aquí debes implementar la lógica para extraer información sobre la experiencia profesional.
    # Puedes usar expresiones regulares o procesamiento de texto para buscar patrones relevantes.
    # Por ejemplo, buscar palabras clave como "experiencia", "trabajo", "cargo", "empresa", etc.

    # Ejemplo de expresión regular para buscar información sobre la experiencia laboral:
    experience_pattern = r"(?i)experiencia(?:\s\w+)?\s(?:laboral|profesional)?\s.*?(?=(?:educación|idiomas|certificaciones|skills|$))"
    experience_matches = re.findall(experience_pattern, text, re.DOTALL)
    
    return experience_matches

# Función para extraer idiomas
def extract_languages(text):
    # Aquí debes implementar la lógica para extraer información sobre los idiomas.
    # Puedes usar expresiones regulares o procesamiento de texto para buscar patrones relevantes.
    # Por ejemplo, buscar palabras clave como "idiomas", "inglés", "español", etc.

    # Ejemplo de expresión regular para buscar información sobre idiomas:
    languages_pattern = r"(?i)idiomas?\s.*?(?=(?:educación|experiencia|certificaciones|skills|$))"
    languages_matches = re.findall(languages_pattern, text, re.DOTALL)
    
    return languages_matches

# Función para extraer certificaciones
def extract_certifications(text):
    # Aquí debes implementar la lógica para extraer información sobre las certificaciones.
    # Puedes usar expresiones regulares o procesamiento de texto para buscar patrones relevantes.
    # Por ejemplo, buscar palabras clave como "certificaciones", "certificado", "curso", etc.

    # Ejemplo de expresión regular para buscar información sobre certificaciones:
    certifications_pattern = r"(?i)certificaciones?\s.*?(?=(?:educación|experiencia|idiomas|skills|$))"
    certifications_matches = re.findall(certifications_pattern, text, re.DOTALL)
    
    return certifications_matches

# Función para extraer skills/habilidades
def extract_skills(text):
    # Aquí debes implementar la lógica para extraer información sobre las habilidades o skills.
    # Puedes usar expresiones regulares o procesamiento de texto para buscar patrones relevantes.
    # Por ejemplo, buscar palabras clave como "habilidades", "skills", "conocimientos", etc.

    # Ejemplo de expresión regular para buscar información sobre skills:
    skills_pattern = r"(?i)skills?\s.*?(?=(?:educación|experiencia|idiomas|certificaciones|$))"
    skills_matches = re.findall(skills_pattern, text, re.DOTALL)
    
    return skills_matches

# Ruta al archivo de CV en formato docx
cv_file_path = 'cv_APA.docx'

# Utiliza docx2txt para extraer texto del archivo docx
cv_text = docx2txt.process(cv_file_path)

# Extraer información
education_info = extract_education(cv_text)
experience_info = extract_experience(cv_text)
languages_info = extract_languages(cv_text)
certifications_info = extract_certifications(cv_text)
skills_info = extract_skills(cv_text)

# Imprimir la información extraída
print("Educación:")
for item in education_info:
    print(item)

print("\nExperiencia Profesional:")
for item in experience_info:
    print(item)

print("\nIdiomas:")
for item in languages_info:
    print(item)

print("\nCertificaciones:")
for item in certifications_info:
    print(item)

print("\nSkills/Habilidades:")
for item in skills_info:
    print(item)
