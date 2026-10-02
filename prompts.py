from system.core.agent import Agent
from system import agents

with open(agents.path / "needs_interpreter.md", "r", encoding="utf-8") as file:
    interpreter= Agent("gemini-3.1-flash-lite", file.read())

print(interpreter.api(interpreter.call("I need to find a good restaurant in New York City. Can you help me with that?"), "filter response"))