import os
from rich.text import Text
import re


class Promt:
    def __init__(self):
        self.content = ""
        self.model = "gpt-4o"
        self.language = "ru"
        self.language_ru = "Type the answer using the RUSSIAN LANGUAGE."
        self.language_en = "Type the answer using the ENGLISH LANGUAGE."
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
        if self.language == "ru":
            self.content += self.language_ru
        else:
            self.content += self.language_en
        self.content += "\n"
        self.content += self.parse_files()
        self.truncate_history()
        self.history.append({"role": "user", "content": self.content.rstrip()})
        return True
    
    
    def format(self, text: str) -> Text:
        if len(text) > 10 and text[:7:].lstrip().rstrip() == "<think>":
            text = text[7::]
        console_text = Text()
        parts = re.split(r'(</think>)', text, maxsplit=1, flags=re.IGNORECASE)
        if len(parts) > 1:
            before_think = parts[0]
            after_think = parts[2] if len(parts) > 2 else ""
            before_text = self.parse_all(before_think)
            before_text.stylize("italic")
            console_text.append(before_text)
            after_text = self.parse_all(after_think)
            console_text.append(after_text)
        else:
            console_text = self.parse_all(text)
        return console_text


    def parse_all(self, text: str) -> Text:
        result = Text()
        lines = text.splitlines(keepends=True)
        for line in lines:
            if line.startswith("###"):
                content = line[3:].lstrip()
                t = self.parse_bold(content)
                t.stylize("bold italic underline")
                result.append(t)
            elif line.startswith("##"):
                content = line[2:].lstrip()
                t = self.parse_bold(content)
                t.stylize("bold underline")
                result.append(t)
            else:
                t = self.parse_bold(line)
                result.append(t)

        return result


    def parse_bold(self, text: str) -> Text:
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
