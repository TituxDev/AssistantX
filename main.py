'''
Conceptual system test for user profile recognition
'''
from system.core.agent import Agent
from system.processes import markdown as mkd
from system import agents
from system import memory

from concurrent.futures import ThreadPoolExecutor
import json

chatter= Agent("llama3.1:latest")

with open(agents.path / "interest_profiler.md", 'r' , encoding="utf-8") as prompt:
    interest_profiler= Agent("llama3.1:latest", prompt.read())

with open(agents.path / "comunication_profiler.md", 'r' , encoding="utf-8") as prompt:
    comunication_profiler= Agent("llama3.1:latest", prompt.read())

with open(agents.path / "user_profiler.md", 'r' , encoding="utf-8") as prompt:
    user_profiler= Agent("llama3.1:latest", prompt.read())

try:
    with open(memory.path / "user profile.md" , "r", encoding="utf-8") as file:
        profile= mkd.extract(memory.path / "user profile.md")
except:
    profile= {}
        

with ThreadPoolExecutor(max_workers=2) as profilers:
    while (message:= input("\033[32mYou: ")) != "\\exit":
        profile_promt= mkd.construct(profile)
        response= chatter.chat(message, profile_promt)
        print(f"\033[36mchatter: {response}\033[0m")
        interests= profilers.submit(interest_profiler.call, str(chatter.history), profile_promt)
        comunication= profilers.submit(comunication_profiler.call, str(chatter.history), profile_promt)
        user_profile= {
            "interests" : interest_profiler.api(interests.result(), "filter response"),
            "comunication": comunication_profiler.api(comunication.result(), "filter response")
        }
        profile_update= json.loads(user_profiler.api(user_profiler.call(str(user_profile), profile_promt), "filter response"))
        for topic, subtopic in profile_update.items():
            if topic not in profile:
                profile[topic]= subtopic
            else:
                for st , text in subtopic.items():
                    profile[topic][st]= text

print(f"\033[0m")
with open(memory.path / "user_profile.md", "w", encoding="utf-8") as file:
    file.write(mkd.construct(profile))