import requests
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def query_llm(prompt: str, mode: str = "medium") -> str:
    try:
        # ☁️ CLOUD
        if mode == "cloud":
            r = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            return r.choices[0].message.content

        # 🧠 LOCAL MODEL MAPPING
        if mode == "low":
            model = "tinyllama"
        elif mode == "high":
            model = "mistral"
        else:
            model = "phi3.5"

        r = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            }
        )

        return r.json()["response"]

    except Exception as e:
        return f"[LLM ERROR] {e}"
