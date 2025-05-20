import os
import openai
from dotenv import load_dotenv
import requests
from PIL import Image
from io import BytesIO
from langchain.prompts import PromptTemplate

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Prompt template
prompt_template = PromptTemplate(
    input_variables=["title", "style", "color", "theme"],
    template="""
Create a {style}. The yoga pose that the figure should be doing is "{title}".
Use a {color} background. The design should visually align with the overall theme: "{theme}".

Make sure the character is the central focus, properly executing the specified yoga pose. Avoid including any literal interpretations of the pose name (e.g., no mountains for "Mountain Pose").


"""

)

# Input
title = "Mountain Pose"
style = "Create flat-vector yoga pose illustrations featuring a single female figure in teal and charcoal sportswear, drawn with uniform line weight, no gradients, a limited teal-orange palette."
color = "#ADD8E6"
theme = "Yoga poses for an infographic"

# Generate prompt
prompt = prompt_template.format(title=title, style=style, color=color, theme=theme)
print("Generated Prompt:\n", prompt)

# Call OpenAI API
response = openai.images.generate(
    model="dall-e-3",
    prompt=prompt,
    size="1024x1024",
    quality="standard",
    n=1,
    response_format="url"
)
image_url = response.data[0].url
print("Generated Image URL:\n", image_url)

# Download and show image
res = requests.get(image_url)
img = Image.open(BytesIO(res.content))
img.show()
