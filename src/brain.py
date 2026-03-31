from src.llm_client import ask_llm

def process_query(query: str, mode: str = "full") -> str:
    query = query.lower()

    if mode == "light":
        return "[LIGHT MODE] Limited response."

    if "status" in query:
        return "All systems operational."

    if "hello" in query:
        return "J.A.R.V.I.S. online."

    # fallback to LLM
    return ask_llm(query)
