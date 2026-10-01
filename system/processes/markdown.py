from pathlib import Path

def construct(content, title=""):
    result= f"# {title.upper()}\n" if title else ""
    render= content if isinstance(content, (list, tuple)) else (content,)
    for content in render:
        if isinstance(content, dict):
            for subtitle, info in content.items():
                result+= f"\n## {str(subtitle).upper()}\n"
                if isinstance(info, (list, tuple)):
                    text, deep= info
                elif isinstance(info, dict):
                    text, deep= "", info
                else:
                    text, deep= info, {}
                if text:
                    result+= f"\n{str(text)}\n"
                for deeptitle, body in deep.items():
                    result+= f"\n### {str(deeptitle).upper()}\n\n{str(body)}\n"
        else:
            result+= f"\n{str(content)}\n"
    return result.strip() + "\n"

def extract(path: Path):
    result= ["",{}]
    with path.open("r", encoding="utf-8") as file:
        title= ""
        subtitle= ""
        deeptitle= ""
        code= False
        for line in file:
            if line.startswith("```"):
                code= not code
            if not code:
                if line.startswith("# "):
                    title= line[2:].strip().lower()
                    continue
                elif line.startswith("## "):
                    subtitle= line[3:].strip().lower()
                    result[1][subtitle]= ["", {}]
                    deeptitle= ""
                    continue
                elif line.startswith("### "):
                    deeptitle= line[4:].strip().lower()
                    result[1][subtitle][1][deeptitle]= ""
                    continue
            if deeptitle:
                result[1][subtitle][1][deeptitle]+= line
            elif subtitle:
                result[1][subtitle][0]+= line
            else:
                result[0]+= line
    for sub, (text, deep) in result[1].items():
        text= text.strip()
        deep= {k: v.strip() for k, v in deep.items()}
        if text and deep:
            result[1][sub]= [text, deep]
        else:
            result[1][sub]= text or deep
    text, children= result[0].strip(), result[1]
    if text and children:
        result= [text, children]
    else:
        result= text or children
    return {title: result} if title else result