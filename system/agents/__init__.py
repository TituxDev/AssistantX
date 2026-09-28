from pathlib import Path

agents_dir = Path(__file__).resolve().parent

agents = {}

for path in agents_dir.glob("*.md"):
    agent = {"rol": None, "propouse": None}
    section = None

    with path.open("r", encoding="utf-8") as file:
        for line in file:
            header = line.strip()

            if header.startswith("## "):
                section = header[3:].lower()

                if section not in agent:
                    section = None
                else:
                    agent[section] = ""

                continue

            if section:
                agent[section] += line

    agents[path.stem] = agent