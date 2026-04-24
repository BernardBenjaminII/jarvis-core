from src.services.llm_service import query_llm
from src.services.tools import run_tool
from src.services.system_service import run_command
from src.memory import save_interaction, get_recent_context
from src.services.network_guardian import handle_network_guardian


# 🧠 PROMPT BUILDER
def build_prompt(question, context):
    return f"""
You are JARVIS, an advanced AI assistant.

Recent Context:
{context}

User Query:
{question}

Response:
""".strip()


# 🛡️ SAFE COMMAND WHITELIST
ALLOWED_COMMANDS = [
    "ls", "pwd", "whoami", "cat",
    "ifconfig", "ip a", "ip route",
    "ping", "netstat", "ss",
    "ps", "top",
    "nmap", "iwconfig", "iw dev"
]


# 🖥️ Detect direct shell commands
def is_shell_command(question: str):
    q = question.strip()
    return any(q.startswith(cmd) for cmd in ALLOWED_COMMANDS)


# 🧠 Detect Kali / network intent
def is_kali_task(question: str):
    q = question.lower()

    kali_keywords = [
        "scan network", "scan", "nmap",
        "check internet", "internet status",
        "ping", "latency",
        "open ports", "ports",
        "network devices", "devices",
        "wifi", "monitor mode",
        "interface", "interfaces",
        "ip address"
    ]

    return any(k in q for k in kali_keywords)


# 🛠️ Kali command translator (NL → command)
def handle_kali_command(question: str):
    q = question.lower()

    if "scan network" in q or "nmap" in q:
        return run_command("nmap -sn 192.168.1.0/24")

    if "check internet" in q or "internet status" in q:
        return run_command("ping -c 3 1.1.1.1")

    if "ip address" in q:
        return run_command("ip a")

    if "interfaces" in q:
        return run_command("ip a")

    if "routes" in q:
        return run_command("ip route")

    if "open ports" in q:
        return run_command("nmap -sT localhost")

    return "[KALI] No matching command found."


# 🧠 Tool detection (non-shell utilities)
def should_use_tool(question: str):
    q = question.lower()

    tool_keywords = [
        "time", "date",
        "status", "cpu", "memory", "disk",
        "process", "kill",
        "read file", "search file"
    ]

    return any(k in q for k in tool_keywords)


# 🚀 MAIN BRAIN
def process_query(question, mode="local"):
    try:
        context = get_recent_context()

        # 🖥️ SYSTEM COMMAND
        if is_shell_command(question):
            result = run_command(question)
            save_interaction(question, result)
            return f"[JARVIS: system]\n{result}"

        # 🛡️ NETWORK GUARDIAN
        if "network" in question.lower() or "scan" in question.lower():
            result = handle_network_guardian(question)
            save_interaction(question, result)
            return f"[JARVIS: network-guardian]\n{result}"

        # 🛠️ TOOL
        if should_use_tool(question):
            result = run_tool(question)
            save_interaction(question, result)
            return f"[JARVIS: tool]\n{result}"

        # 🤖 LLM
        response = query_llm(build_prompt(question, context), mode)
        save_interaction(question, response)
        return response

    except Exception as e:
        return f"[BRAIN ERROR] {str(e)}"
def is_network_guardian_task(question: str):
    q = question.lower()

    keywords = [
        "network guardian",
        "network status",
        "full network check",
        "quick network",
        "internet check",
        "check internet",
        "fix dns",
        "repair dns",
        "restart network",
        "restart networkmanager",
        "stop docker",
        "start docker",
        "reset docker network",
        "docker safe reset",
        "routes",
        "interfaces"
    ]

    return any(k in q for k in keywords)
