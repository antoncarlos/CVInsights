import streamlit as st
import boto3
import langid
import spacy
 
# Configuración de AWS
s3 = boto3.client('s3')
textract = boto3.client('textract')
translate = boto3.client('translate')
 
# Configuración del bucket de S3
S3_BUCKET = 'tu-bucket-s3'
S3_OUTPUT_FOLDER = 'cv-input'
S3_OUTPUT_TRANSLATED_FOLDER = 'cv-translated'
 
# Configuración del modelo spaCy para inglés
nlp = spacy.load("en_core_web_sm")
 
def upload_to_s3(file):
    # Subir archivo al bucket de S3
    s3.upload_fileobj(file, S3_BUCKET, f'{S3_OUTPUT_FOLDER}/{file.name}')
 
def nlp_filter(text):
    # Ejemplo de filtrado de "hard skills" utilizando spaCy
    doc = nlp(text)
 
    hard_skills = ["python", "machine learning", "data analysis"]
    # Filtrar CVs que contengan al menos una "hard skill"
    for token in doc:
        if token.text.lower() in hard_skills:
            return True
 
    return False
 
def calculate_profile_score(profile, requirements):
    score = 0
 
    # Verificar cada requisito y otorgar puntos
    if profile['experience'] > 3:
        score += requirements['experience_priority']
 
    if 'SQL' in profile['technologies']:
        score += requirements['sql_priority']
 
    if profile['english_level'] == 'C1' or profile['english_level'] == 'C2':
        score += requirements['english_priority']
 
    if profile['degree'] == 'MSc in IT':
        score += requirements['degree_priority']
 
    return score
 
def get_recommended_profiles(profiles, requirements):
    recommended_profiles = []
 
    for profile in profiles:
        score = calculate_profile_score(profile, requirements)
 
        # Definir un umbral para la puntuación de recomendación
        if score >= requirements['threshold']:
            recommended_profiles.append({'profile': profile, 'score': score})
 
    # Ordenar perfiles por puntuación descendente
    recommended_profiles.sort(key=lambda x: x['score'], reverse=True)
 
    return recommended_profiles
 
def main():
    st.title('Carga de CVs y Recomendaciones')
 
    uploaded_file = st.file_uploader("Seleccione un archivo PDF", type=["pdf"])
 
    if uploaded_file is not None:
        # Subir el archivo a S3 cuando se selecciona
        upload_to_s3(uploaded_file)
        st.success('Archivo cargado con éxito.')
 
        # Obtener el texto del PDF con Textract
        response = textract.start_document_text_detection(
            DocumentLocation={'S3Object': {'Bucket': S3_BUCKET, 'Name': f'{S3_OUTPUT_FOLDER}/{uploaded_file.name}'}}
        )
 
        # Esperar a que Textract complete el trabajo
        job_id = response['JobId']
        result = None
        while result == None or result['JobStatus'] == 'IN_PROGRESS':
            result = textract.get_document_text_detection(JobId=job_id)
 
        # Extraer texto
        text = result['Blocks'][0]['Text']
 
        # Detectar el idioma del texto
        lang, _ = langid.classify(text)
 
        # Traducir solo si el idioma no es español
        if lang != 'es':
            # Traducir texto al español
            translation = translate.translate_text(Text=text, SourceLanguageCode=lang, TargetLanguageCode='es')
            translated_text = translation['TranslatedText']
 
            # Filtrar por "hard skills"
            if nlp_filter(translated_text):
                # Lógica del sistema recomendador
                requirements = {
                    'experience_priority': 1,
                    'sql_priority': 2,
                    'english_priority': 3,
                    'degree_priority': 4,
                    'threshold': 8
                }
 
                profiles = [
                    {'experience': 4, 'technologies': ['SQL', 'Python'], 'english_level': 'C1', 'degree': 'MSc in IT'},
                    {'experience': 2, 'technologies': ['Java', 'C++'], 'english_level': 'B2', 'degree': 'BSc in CS'},
                    # Agrega más perfiles según sea necesario
                ]
 
                recommended_profiles = get_recommended_profiles(profiles, requirements)
 
                # Mostrar perfiles recomendados
                st.title('Perfiles Recomendados')
                for rec_profile in recommended_profiles:
                    st.write(f"Perfil: {rec_profile['profile']}, Puntuación: {rec_profile['score']}")
            else:
                st.warning('El CV no cumple con los requisitos de hard skills.')
        else:
            # No es necesario traducir, simplemente almacenar el texto original
            st.info('El CV está en español, no se requiere traducción.')
 
if __name__ == '__main__':
    main()