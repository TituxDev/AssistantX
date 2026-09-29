'''
Conceptual system test for user profile recognition
'''
from system.core.agent import Agent
from system.processes import markdown as mkd
from system import agents
from concurrent.futures import ThreadPoolExecutor

chatter= Agent("llama3.1:latest")

with open(agents.path / "interest_profiler.md", 'r' , encoding="utf-8") as prompt:
    interest_profiler= Agent("llama3.1:latest", prompt.read())

with open(agents.path / "comunication_profiler.md", 'r' , encoding="utf-8") as prompt:
    comunication_profiler= Agent("llama3.1:latest", prompt.read())

with ThreadPoolExecutor(max_workers=2) as profilers:
    while (message:= input("You: ")) != "\\exit":
        response= chatter.chat(message)
        print(f"chatter: {response}")
        interests= profilers.submit(interest_profiler.call, str(chatter.history))
        comunication= profilers.submit(comunication_profiler.call, str(chatter.history))
        interests= interests.result()
        comunication= comunication.result()
        print(f"---\n[INTERESTS]\n{interest_profiler.api(interests, "filter response",  "")}\n---")
        print(f"---\n[COMUNICATION]\n{comunication_profiler.api(comunication, "filter response",  "")}\n---")
