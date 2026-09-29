'''
Conceptual system test for user profile recognition
'''
from system.core.agent import Agent
from system.processes import markdown as mkd
from system import agents
from system import memory

from concurrent.futures import ThreadPoolExecutor

chatter= Agent("llama3.1:latest")

with open(agents.path / "interest_profiler.md", 'r' , encoding="utf-8") as prompt:
    interest_profiler= Agent("llama3.1:latest", prompt.read())

with open(agents.path / "comunication_profiler.md", 'r' , encoding="utf-8") as prompt:
    comunication_profiler= Agent("llama3.1:latest", prompt.read())

with open(agents.path / "user_profiler.md", 'r' , encoding="utf-8") as prompt:
    user_profiler= Agent("llama3.1:latest", prompt.read())

try:
    with open(memory.path / "user profile.md" , "r", encoding="utf-8") as file:
        profile_sumarized= file.read()
except:
    profile_sumarized= ""
        

with ThreadPoolExecutor(max_workers=2) as profilers:
    while (message:= input("\033[32mYou: ")) != "\\exit":
        response= chatter.chat(message, profile_sumarized)
        print(f"\033[36mchatter: {response}\033[0m")
        interests= profilers.submit(interest_profiler.call, str(chatter.history), profile_sumarized)
        comunication= profilers.submit(comunication_profiler.call, str(chatter.history), profile_sumarized)
        user_profile= {
            "interests" : interest_profiler.api(interests.result(), "filter response"),
            "comunication": comunication_profiler.api(comunication.result(), "filter response")
        }
        profile_sumarized= user_profiler.api(user_profiler.call(str(user_profile), profile_sumarized), "filter response")

with open(memory.path / "user_profile.md", "w", encoding="utf-8") as file:
    file.write(profile_sumarized)
