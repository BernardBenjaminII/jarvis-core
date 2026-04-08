from src.services.llm_service import query_llm
from src.services.tools import run_tool
from src.memory import save_interaction, get_recent_context

def build_prompt(question):
    return f"""
You are JARVIS, an advanced AI assistant.

User Query:
{question}

Response:
""".strip()


def process_query(question, mode="local"):
    full_prompt = build_prompt(question)

    try:
        response = query_llm(full_prompt, mode)
        return response

    except Exception:
        response = query_llm(full_prompt, "cloud")
        return response

def select_mode(question: str) -> str:
    q = question.lower()

    # 🔧 Tool-type / simple
    if len(q) < 30:
        return "low"

    # ⚡ Simple factual
    if any(x in q for x in ["what is", "who is", "when", "where"]):
        return "medium"

    # 🧠 Complex reasoning
    if any(x in q for x in ["design", "architecture", "explain deeply", "analyze"]):
        return "high"

    # ☁️ Very complex or vague → cloud
    if len(q) > 200:
        return "cloud"

    return "medium"
