import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def gpt_generate_dalle_prompt(title, style, color, theme):
    """
    Uses GPT-4 to craft a high-quality DALL·E 3 prompt with detailed anatomical and artistic guidance.
    """
    system_prompt = (
        "You are an expert visual prompt engineer for DALL·E 3. "
        "Given the name of a yoga pose, your job is to create a highly detailed and stylistically consistent image prompt "
        "for a female figure performing that pose. "
        "Never interpret the name literally — always treat it as a physical posture, not as scenery or object. "
        "Include visual specifics such as posture, limb position, orientation, body alignment, and energy/focus of the pose. "
        "Use the sytle given by the user and follow that strictly."
    )

    user_prompt = f"""
Pose Title: {title}
Style: {style}
Background Color: {color}
Theme: {theme}

IMPORTANT:
- Treat the title as a YOGA POSE — not a literal object or scene.
- Include key visual aspects of the yoga pose: body orientation, position, limb alignment, tension or relaxation.
- Always describe the posture clearly and accurately.
- Ignore misleading words like “dog” or “mountain” and other similar words unless they're relevant to body shape.
- Focus on illustrating a figure doing that yoga pose, centered and cleanly styled.
- Include the background color and stylistic tone.
- DO NOT include text or literal animals/objects.
- Also add clear instruction for the background color and style. which the user provided.
- Do not invent any posture details. If you're unsure, stick to general descriptors
- Do not add extra finger or eye movements unless explicitly required.
- Only use standard yoga descriptions from verified anatomy sources.
- Also add explicit instruction not to add any kind of other deatils like trees, animals, mountain, other objects.


NOW: Generate a high quality prompt for the new pose according to the Pose Title.
"""

    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.4
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[ERROR] GPT prompt generation failed: {e}")
        return None

def generate_image_url(prompt):
    """
    Uses OpenAI's DALL·E 3 (via GPT) to generate an image and return its URL.
    """
    try:
        response = openai.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
            response_format="url"
        )
        return response.data[0].url
    except Exception as e:
        print(f"[ERROR] Image generation failed: {e}")
        return None

def download_image(image_url, save_path):
    import requests
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        return True
    else:
        print("Failed to download image.")
        return False



#for testing

if __name__ == "__main__":
    title = "Mountain Pose"
    style = "Create flat-vector yoga pose illustrations featuring a single female figure in teal and charcoal sportswear, drawn with uniform line weight, no gradients, a limited teal-orange palette."
    color = "#ADD8E6"
    theme = "Yoga poses for infographic"

    print("🎯 Generating prompt using GPT-4...")
    prompt = gpt_generate_dalle_prompt(title, style, color, theme)
    print("\n📝 Final Prompt:\n", prompt)

    if prompt:
        print("\n Generating image...")
        image_url = generate_image_url(prompt)
        print("✅ Image URL:\n", image_url)

        if image_url:
            filename = f"{title.replace(' ', '_').lower()}.png"
            if download_image(image_url, filename):
                print(f" Image downloaded to {filename}")
            else:
                print(" Failed to download image.")
