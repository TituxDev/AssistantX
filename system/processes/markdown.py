from pathlib import Path

def extract(path: Path, *args: str)->dict:
    result= {}
    section = None

    with path.open("r", encoding="utf-8") as file:
        for line in file:
            header= line.strip()
            if header.startswith("## "):
                if section:
                    result[section]= result[section].strip()
                section= header[3:].lower()
                if section in args or not args:
                    result[section]= ""
                else:
                    section= None
                continue
            if section:
                result[section]+= line
    if section:
        result[section]= result[section].strip()
    return result

def construct(data: dict, title= "")->str:
    result= f"# {title.upper()}\n" if title else ""
    for section, text in data.items():
        result+= f"\n## {section.upper()}\n\n{text}\n"
    return result