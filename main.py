from g4f.client import Client
from rich.console import Console
from promt import Promt


#  Collection of free and stable(no) models
TEXT_MODELS = ["gpt-4o", "gpt-4o-mini", "llama-3.2-11b", 
          "gemini-1.5-flash", "gemini-1.5-pro", "phi-4", "command-r", 
          "command-r-plus", "command-r7b", "command-a", 
          "qwen-2-72b", "qwen-2.5-coder-32b", "qwen-2.5-1m", 
          "deepseek-v3", "deepseek-r1",
          "mistral-nemo", "evil(18+ mode)"]


# Here we go!
data = input("You: ")

# Formatting AI output, uploading files, truncates history and more
promt = Promt()

# For beautiful output
console = Console()

# GPT
client = Client()

while data != "exit":
    
    # User wants to change model
    if data.split()[0] == "set_model":
        promt.model = data.split()[1]
        console.print(promt.format("Config:</think> ***setted model to " + data.split()[1] + "***"))
        data = input("You: ")
        continue
    
    # User wants to see all models
    elif data == "model_list":
        console.print(promt.format("Config:</think> ***all models list:***"))
        for el in TEXT_MODELS:
            console.print(promt.format("***" + el + "***"), end="\n")
        data = input("You: ")
        continue
    
    # User wants to clean history
    elif data == "clean":
        console.print(promt.format("Config:</think> ***history cleaned***"))
        promt.history = []
        data = input("You: ")
        continue
    
    # Adding user promt
    promt.content = data
    
    # Setting language
    promt.language = "ru"
    
    # Formatting promt
    promt.create()
    
    # No comments
    console.print(promt.format(f"{promt.model}: ***typing...***"))
    
    # Getting AI's response
    response = client.chat.completions.create(
        model=promt.model,
        messages=promt.history,
        web_search=False
    )
    
    # Adding to history
    promt.history.append({"role": "assistant", "content": response.choices[0].message.content})
    
    # Deleting "typing..."
    print("\033[F\033[K", end='')
    
    # Formatting output
    formatted = promt.format(promt.history[-1]["content"])
    
    # We did it!
    console.print(f"{promt.model}:", formatted)
    
    # Oh shit...
    data = input("You: ")
