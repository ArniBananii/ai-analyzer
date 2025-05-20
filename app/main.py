import json
from fastapi import FastAPI, Request 
from dotenv import load_dotenv
import httpx
import os
from ai_client import ask_openai


load_dotenv()
print(os.environ)

app = FastAPI()

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

@app.post("/analyze")
async def analyze(request: Request):
    try:
        data = await request.json()
        print("Received data:", data)
        ai_summary = ask_openai(json.dumps(data, indent=2))
        await send_to_discord(ai_summary)
        return {"message": "Analysis sent to Discord"}
    except Exception as e:
        return {"error": str(e)}



async def send_to_discord(message: str):
    if not DISCORD_WEBHOOK_URL:
        print("Missing Discord webhook URL")
        return
    async with httpx.AsyncClient() as client:
        await client.post(DISCORD_WEBHOOK_URL, json={"content": message})