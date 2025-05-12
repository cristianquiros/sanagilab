from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import openai
import os

app = FastAPI()

# Clave API de OpenAI desde variable de entorno
openai.api_key = os.getenv("OPENAI_API_KEY")

# Configuración CORS para permitir desde tu dominio
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://sanagilab.com"],  # O usa ["*"] temporalmente
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        user_message = data.get("message", "")
        if not user_message:
            return {"error": "Mensaje vacío"}

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        reply = response.choices[0].message.content.strip()
        return {"reply": reply}
    except Exception as e:
        return {"error": str(e)}
