from pathlib import Path
from system.processes.markdown import extract 

path= Path(__file__).resolve().parent
agents = {}

for p in path.glob("*.md"):
    agents[p.stem]= next(iter(extract(p).values()))["role"]