from rich.console import Console
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from promt import Promt


#  Collection of free and stable(no) models
TEXT_MODELS = ["gpt-4o", "gpt-4o-mini", "llama-3.2-11b", 
          "gemini-1.5-flash", "gemini-1.5-pro", "phi-4", "command-r", 
          "command-r-plus", "command-r7b", "command-a", 
          "qwen-2-72b", "qwen-2.5-coder-32b", "qwen-2.5-1m", 
          "deepseek-v3", "deepseek-r1",
          "mistral-nemo", "felo-ai", "evil"]


completer = WordCompleter(["model_list", "set_model", "clean"] + TEXT_MODELS)

# Here we go!
data = prompt("You: ", completer=completer, complete_while_typing=False)

# Formatting AI output, uploading files, truncates history and more
promt = Promt()

# For beautiful output
console = Console()

while data != "exit":
    
    # User wants to change model
    if data.split()[0] == "set_model":
        promt.model = data.split()[1]
        console.print(promt.format("Config:</think> ***setted model to " + data.split()[1] + "***"))
        data = prompt("You: ", completer=completer, complete_while_typing=False)
        continue
    
    # User wants to see all models
    elif data == "model_list":
        console.print(promt.format("Config:</think> ***all models list:***"))
        for el in TEXT_MODELS:
            console.print(promt.format("***" + el + "***"), end="\n")
        data = prompt("You: ", completer=completer, complete_while_typing=False)
        continue
    
    # User wants to clean history
    elif data == "clean":
        console.print(promt.format("Config:</think> ***history cleaned***"))
        promt.history = []
        data = prompt("You: ", completer=completer, complete_while_typing=False)
        continue
    
    # Adding user promt
    promt.content = data
    
    # Setting language
    promt.language = "ru"
    
    # Formatting promt
    promt.create()
    
    # No comments
    console.print(promt.format(f"{promt.model}: ***typing...***"))
    
    # Adding to history
    promt.history.append({"role": "assistant", "content": promt.compute()})
    
    # Deleting "typing..."
    print("\033[F\033[K", end='')
    
    # Formatting output
    formatted = promt.format(promt.history[-1]["content"])
    
    # We did it!
    console.print(f"{promt.model}:", formatted)
    
    # Oh shit...
    data = prompt("You: ", completer=completer, complete_while_typing=False)
