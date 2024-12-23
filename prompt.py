import os

# Models and prompt styles
models = ["gpt-4o", "gpt-4o-mini"]
prompt_styles = {
    "poetry": "You are a poem-writing agent. Please write a nice poem.",
    "dickinson": "You are a poet influenced by Emily Dickinson. Please write a poem in something similar to her style."
}

# Directory containing task files
task_dir = "tasks"
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
                print(e)
            # Save results to a file
            output_dir = os.path.join("output", language_model, style_name)
            os.makedirs(output_dir, exist_ok=True)
            output_file = os.path.join(output_dir, os.path.basename(task_file))
            with open(output_file, "w") as f:
                f.write(results)