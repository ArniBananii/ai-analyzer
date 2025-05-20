
from pathlib import Path
import os
from dotenv import load_dotenv
import openai

try:
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OpenAI API key must be set via environment variable.")
except ValueError as e:
    print(f"Error: {e}")

def ask_openai(prompt: str) -> str:
    system_prompt_path = Path("model_context.txt")
    with system_prompt_path.open("r", encoding="utf-8") as f:
        system_prompt = f.read()
    if not system_prompt_path.exists():
        raise FileNotFoundError(f"System prompt file not found: {system_prompt}")
    response = openai.chat.completions.create(
        model="gpt-4.1",
        messages=[
                {"role": "system", "content": system_prompt_path},
                {"role": "user", "content": prompt}
            ],
        temperature=0.7,
    )
    return response.choices[0].message["content"]