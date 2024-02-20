from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os 
from PIL import Image
import google.generativeai as genai
api_key = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=api_key)

## Function to load Gemini Pro Vision model

model = genai.GenerativeModel('gemini-pro-vision')

def get_gemini_response(input,image,prompt):
    response = model.generate_content([input, image[0], prompt])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        #read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        return FileNotFoundError("No file uploaded. Please upload a file.")
        
    


##initialize our streamlit app
st.set_page_config(page_title="MultiLanguage Invoice Extractor")
st.header ("MultiLanguage Invoice Extractor")


input=st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an image of the invoice...", type=["jpg","png","jpeg"], key="image")
image=""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)

submit = st.button("Tell me about the invoice")

input_prompt = """
You are expert in understanding invoices. We will upload an image as invoices and you will have to answer any questions based on the uploaded image of invoice.
"""

# if submit btn is clicked

if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt,image_data,input)
    st.subheader("The response is :")
    st.write(response)
    
