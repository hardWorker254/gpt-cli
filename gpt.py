from g4f.client import Client
import os
import re
from rich.console import Console
from rich.text import Text


TEXT_MODELS = ["gpt-4o", "gpt-4o-mini", "llama-3.2-11b", 
          "gemini-1.5-flash", "gemini-1.5-pro", "command-r(глупый)", 
          "command-r-plus", "command-r7b", "command-a", 
          "qwen-2-72b", "qwen-2.5-coder-32b", "qwen-2.5-1m", 
          "deepseek-v3(иногда)", "deepseek-r1(иногда)",
          "evil"]


class Promt:
    def __init__(self):
        self.content = ""
        self.model = "gpt-4o"
        self.language = "Type the answer using the RUSSIAN LANGUAGE."
        self.history = []
    
    
    def parse_files(self):
        files = []
        for el in self.content.split():
            if os.path.isfile(el):
                files.append(el)
            elif os.path.isfile(el[:-1]):
                files.append(el)
        files_content = ""
        for el in files:   
            try:
                open(el).close()
                print("Attach file " + el + "?")
                answer = input("[Y/N]: ")
                if answer.lower() == "n":
                    continue
                files_content += el
                files_content += "\n"
                files_content += open(el).read()
                files_content += "\n"
            except:
                print("Attach file " + el[:-1] + "?")
                answer = input("[Y/N]: ")
                if answer.lower() == "n":
                    continue
                files_content += el[:-1]
                files_content += "\n"
                files_content += open(el[:-1]).read()
                files_content += "\n"
            files_content += "\nEnd of " + el + "\n"
        return files_content
    
    
    def truncate_history(self):
        if len(self.history) >= 6:
            self.history.pop(0)
            self.history.pop(0)
    
    
    def create(self):
        self.content += "\n"
        self.content += self.language
        self.content += "\n"
        self.content += self.parse_files()
        self.truncate_history()
        self.history.append({"role": "user", "content": self.content.rstrip()})
        return True


def format(text: str) -> Text:
    if len(text) > 10 and text[:7:].lstrip().rstrip() == "<think>":
        text = text[7::]
    console_text = Text()
    parts = re.split(r'(</think>)', text, maxsplit=1, flags=re.IGNORECASE)
    if len(parts) > 1:
        before_think = parts[0]
        after_think = parts[2] if len(parts) > 2 else ""
        before_text = parse_bold(before_think)
        before_text.stylize("italic")
        console_text.append(before_text)
        after_text = parse_bold(after_think)
        console_text.append(after_text)
    else:
        console_text = parse_bold(text)
    return console_text


def parse_bold(text: str) -> Text:
    result = Text()
    pattern = re.compile(r'(\*\*\*|\*\*|`)(.+?)(\1)')
    last_index = 0
    for match in pattern.finditer(text):
        start, end = match.span()
        if start > last_index:
            result.append(text[last_index:start])
        bold_text = match.group(2)
        result.append(bold_text, style="bold")
        last_index = end
    if last_index < len(text):
        result.append(text[last_index:])
    return result


data = input("You: ")
promt = Promt()
console = Console()
client = Client()
while data != "exit":
    if data.split()[0] == "set_model":
        promt.model = data.split()[1]
        console.print(format("Config:</think> ***setted model to " + data.split()[1] + "***"))
        data = input("You: ")
        continue
    elif data == "model_list":
        console.print(format("Config:</think> ***all models list:***"))
        for el in TEXT_MODELS:
            console.print(format("***" + el + "***"), end="\n")
        data = input("You: ")
        continue
    elif data == "clear":
        console.print(format("Config:</think> ***history cleaned***"))
        promt.history = []
        data = input("You: ")
        continue
    promt.content = data
    promt.create()
    console.print(format(f"{promt.model}: ***typing...***"))
    response = client.chat.completions.create(
        model=promt.model,
        messages=promt.history,
        web_search=False
    )
    promt.history.append({"role": "assistant", "content": response.choices[0].message.content})
    print("\033[F\033[K", end='')
    formatted = format(promt.history[-1]["content"])
    console.print(f"{promt.model}:", formatted)
    data = input("You: ")
