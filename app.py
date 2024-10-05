### Calorie Tracker
from dotenv import load_dotenv

load_dotenv() ## loading all the environment variables

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load Google Gemini Pro Vision API And get response

def get_gemini_response(image, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([image[0], prompt])
    return response.text

def input_image_setup(uploaded_file):
    # Checking if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
## Initializing Streamlit app

st.set_page_config(page_title="Calorie Tracker App")

st.markdown("""
            <style>
            .stApp {
                background-color: #143130;
             }
            </style>
            """, unsafe_allow_html=True)

st.header("Calorie Tracker App")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Tell me the total calories")

input_prompt = """
You are an expert nutritionist. Please analyze the food items in the image
and calculate the total calories, also provide the details of each food item with calorie intake
in the following format:

1. Item 1 - number of calories
2. Item 2 - number of calories
----
----
Finally, mention whether the food is healthy or not.\n
If the food is unhealthy, give suggestions to add or remove food items to make it an overall healthy meal.
"""

## If submit button is clicked

if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(image_data, input_prompt)
    st.subheader("The Response is")
    st.write(response)
