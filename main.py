'''
Conceptual system test for user profile recognition
'''
from system.core.agent import Agent
from system.processes import markdown as mkd
from system import agents

file= mkd.extract(agents.path / "void.md")
print(mkd.construct(file, "name"))

chatter= Agent("llama3.1:latest")

with open(agents.path / "user_profiler.md", 'r' , encoding="utf-8") as prompt:
    user_profiler= Agent("llama3.1:latest", prompt.read())

while (message:= input("You: ")) != "\\exit":
    response= chatter.chat(message)
    print(f"chatter: {response}")
    profile= user_profiler.call(str(chatter.history))
    with open("system/memory/user_profile.md", "w", encoding="utf-8") as user_profile:
        user_profile.write(f"---\n[PROFILE]\n{user_profiler.api(profile, "filter response",  "")}\n---")