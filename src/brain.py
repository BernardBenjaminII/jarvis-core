from src.services.llm_service import query_llm
from src.services.tools import run_tool
from src.memory import save_interaction, get_recent_context


def build_prompt(question, context):
    return f"""
You are JARVIS, an advanced AI assistant.

Recent Context:
{context}

User Query:
{question}

Response:
""".strip()


def should_use_tool(question: str):
    q = question.lower()

    tool_keywords = [
        "time", "date",
        "status", "cpu", "memory", "disk",
        "ip", "network", "scan", "ping",
        "find", "search", "read",
        "run", "execute",
        "process", "kill"
    ]

    return any(k in q for k in tool_keywords)


def process_query(question, mode="local"):
    try:
        # 🧠 Memory
        context = get_recent_context()

        # 🛠️ Tool routing
        if should_use_tool(question):
            result = run_tool(question)
            save_interaction(question, result)
            return f"[JARVIS: tool]\n{result}"

        # 🤖 LLM
        full_prompt = build_prompt(question, context)
        response = query_llm(full_prompt, "local")

        save_interaction(question, response)
        return response

    except Exception as e:
        return f"[BRAIN ERROR] {str(e)}"
