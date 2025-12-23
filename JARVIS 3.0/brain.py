from google import genai

client = genai.Client()

def format_bold(text):
    if "**" not in text:
        return text

    parts = text.split("**")
    formatted = ""

    for i, part in enumerate(parts):
        if i % 2 == 1:
            formatted += f"\033[1m{part}\033[0m"  # Terminal bold
        else:
            formatted += part

    return formatted


def generate_response1(prompt):
    # Force short explanations
    if "explain" in prompt.lower() or "what is" in prompt.lower():
        prompt += " in 2 or 3 lines"

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
def generate_response2(prompt):
    # Force short explanations
    prompt += f" explain in brief with one or two line what a {prompt.lower()} is "

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return format_bold(response.text)
