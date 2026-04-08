import datetime

def run_tool(command: str) -> str:
    command = command.lower()

    if "time" in command:
        return f"Current time: {datetime.datetime.now()}"

    if "date" in command:
        return f"Today's date: {datetime.date.today()}"

    if "who are you" in command:
        return "I am JARVIS, your personal assistant."

    return None
