import requests
import os
from openai import OpenAI


# 🔍 Check if Ollama is running
def is_ollama_available():
    try:
        requests.get("http://localhost:11434/api/tags", timeout=2)
        return True
    except:
        return False


# 🧠 Local LLM (Ollama)
def query_local(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        },
        timeout=60
    )

    data = response.json()
    print("[DEBUG] Ollama raw response:", data)  # 👈 keep this for now

    # ✅ Normal case
    if "response" in data:
        return data["response"], "mistral/local"

    # ⚠️ Chat-style fallback
    if "message" in data and "content" in data["message"]:
        return data["message"]["content"], "mistral/local"

    # ❌ Error case
    if "error" in data:
        raise Exception(data["error"])

    raise Exception(f"Unknown Ollama response format: {data}")

# ☁️ Cloud LLM (OpenAI)
def query_cloud(prompt):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content, "openai/cloud"


# 🚀 MAIN ENTRY
def query_llm(prompt, mode="auto"):

    if mode == "auto":
        if is_ollama_available():
            try:
                response, tag = query_local(prompt)
                return f"[JARVIS: {tag}]\n{response}"
            except Exception as e:
                print(f"[LLM] Local failed: {e}")

        try:
            response, tag = query_cloud(prompt)
            return f"[JARVIS: {tag}]\n{response}"
        except Exception as e:
            return f"[LLM ERROR] Cloud failed: {str(e)}"

    if mode == "local":
        try:
            response, tag = query_local(prompt)
            return f"[JARVIS: {tag}]\n{response}"
        except Exception as e:
            return f"[LLM ERROR] Local failed: {str(e)}"

    if mode == "cloud":
        try:
            response, tag = query_cloud(prompt)
            return f"[JARVIS: {tag}]\n{response}"
        except Exception as e:
            return f"[LLM ERROR] Cloud failed: {str(e)}"

    return "[LLM ERROR] Invalid mode"
