import streamlit as st
from PIL import Image
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part

project_id = "hello-app-403419"
location = "us-central1"
vertexai.init(project = project_id, location = location)

def get_model_repsonse(input, image, prompt):
    model = GenerativeModel("gemini-pro-vision")
    response = model.generate_content([input, image[0], prompt])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        # Read the file into bytes
        image_bytes = uploaded_file.getvalue()
        image_parts = [
                Part.from_data(image_bytes, mime_type = uploaded_file.type)
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
st.set_page_config(page_title = "Energy Calculator")

st.header("Energy Calculator")
input = st.text_input("Input Prompt: ", placeholder = 'Enter additional information about your food', key = "input")
uploaded_file = st.file_uploader("Select  an image:", type = ["jpg", "jpeg", "png"])
image = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption = "Your image was successfully uploaded!", use_column_width = True)
submit = st.button("Compute")

input_prompt = "Identify the food items present in the image and calculate the total number of calories and brekadown of macronutrients in each food item present in the picture"

if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_model_repsonse(input, image_data, input_prompt)
    st.subheader("The Response is")
    st.write(response)