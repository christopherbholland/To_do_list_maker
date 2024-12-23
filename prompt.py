import os
from main import prompt, save_to_file

# Models and prompt styles
models = ["gpt-4o", "gpt-4o-mini"]
prompt_styles = {
    "poetry": "You are a poem-writing agent. Please write a nice poem.",
    "dickinson": "You are a poet influenced by Emily Dickinson. Please write a poem in something similar to her style."
}

# Directory containing task files
task_dir = "tasks"
if not os.path.exists(task_dir):
    raise FileNotFoundError(f"Task directory '{task_dir}' does not exist.")

task_files = [os.path.join(task_dir, file) for file in os.listdir(task_dir) if file.endswith(".txt")]

# Iterate over models, styles, and tasks
for language_model in models:
    for style_name, system_prompt in prompt_styles.items():
        for task_file in task_files:
            with open(task_file, "r") as file:
                task_definition = file.read().strip()
            try:
                results = prompt(language_model, system_prompt, task_definition)
            except Exception as e:
                print(f"Error processing {task_file} with {language_model} and {style_name}: {e}")
                continue
            # Save results to a file
            save_to_file(language_model, style_name, task_definition, results)