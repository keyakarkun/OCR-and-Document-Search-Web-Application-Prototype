import numpy as np
import streamlit as st
import easyocr
import pytesseract
from PIL import Image
import re

def extract_text_from_image(image, language='en'):
    """Extracts text from an image using the selected OCR engine."""
    if language == 'en':
        reader = easyocr.Reader(['en'], gpu=False)
        text = reader.readtext(np.array(image), detail=0, paragraph=True) 
        extracted_text = ' '.join(text)
    else:  # Use pytesseract for Hindi
        extracted_text = pytesseract.image_to_string(image, lang='hin')
    return extracted_text

def highlight_search_terms(text, keywords):
    """Highlights the keywords in the extracted text."""
    if keywords:
        for keyword in keywords.split():
            text = re.sub(f"({keyword})", r'<span style="background-color: #FFFF00">\1</span>', text, flags=re.IGNORECASE)
    return text


st.title("OCR Image Text Extraction and Search")

# Language Selection
selected_language = st.radio("Select Language:", ("English", "Hindi"))
language_code = 'en' if selected_language == "English" else 'hi'

uploaded_image = st.file_uploader("Upload an image...", type=["jpg", "png", "jpeg"])

if uploaded_image is not None:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("Extract Text"):
        with st.spinner("Extracting text..."):
            extracted_text = extract_text_from_image(image, language_code)
            st.subheader("Extracted Text:")
            st.write(extracted_text)

        keywords = st.text_input("Enter keywords to search:")
        if st.button("Search"):
            highlighted_text = highlight_search_terms(extracted_text, keywords)
            st.subheader("Search Results:")
            st.markdown(highlighted_text, unsafe_allow_html=True) 