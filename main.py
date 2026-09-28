'''
Conceptual system test for user profile recognition
'''
from system.core.agent import Agent
from system.agents import agents

print(agents)
chatter= Agent("gemini-3.1-flash-lite")

with open("user/agents/user_profiler.md", 'r' , encoding="utf-8") as prompt:
    user_profiler= Agent("gemini-3.1-flash-lite", prompt.read())

while (message:= input("You: ")) != "\\exit":
    response= chatter.chat(message)
    print(f"chatter: {response}")
    profile= user_profiler.call(str(chatter.history))
    with open("system/memory/user_profile.md", "w", encoding="utf-8") as user_profile:
        user_profile.write(f"---\n[PROFILE]\n{user_profiler.api(profile, "filter response",  "")}\n---")