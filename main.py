import os
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow only your website to call this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://obilen.com", "https://www.obilen.com"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ChatIn(BaseModel):
    message: str

SYSTEM = """
You are Obilen — a super capable AI assistant.
Explain clearly, step by step.
If unsure, ask a short question.
"""

@app.post("/chat")
def chat(data: ChatIn):
    r = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": data.message},
        ],
    )
    return {"reply": r.choices[0].message.content}
