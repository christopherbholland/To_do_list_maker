from openai import OpenAI
import os
import datetime
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

client = OpenAI()

# Set up OpenAI API key from the environment variable
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    raise ValueError("OpenAI API key not found. Ensure it's in the .env file.")

# openai.api_key = OPENAI_API_KEY

def prompt(language_model, system_prompt, task_definition):
    try:
        completion = client.chat.completions.create(
            model=language_model,
            store = True,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": task_definition}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error while generating prompt: {e}")
        return ""


def save_to_file(language_model, style_name, task_definition, results):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    filename = f"{language_model}_{style_name}_{timestamp}.txt"
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    
    file_contents = f"""
Language Model: {language_model}
System Prompt: {style_name}
Task Definition: {task_definition}
Results: {results}
"""
    with open(filepath, "w") as file:
        file.write(file_contents)
    print(f"Results saved to {filepath}")

# Models
models = ["gpt-4", "gpt-3.5-turbo"]

# Directory containing prompt files
prompt_dir = "prompts"
if not os.path.exists(prompt_dir):
    raise FileNotFoundError(f"Prompt directory '{prompt_dir}' does not exist.")

# Dynamically generate prompt_styles from files in the prompts directory
prompt_styles = {
    os.path.splitext(filename)[0]: os.path.join(prompt_dir, filename)
    for filename in os.listdir(prompt_dir) if filename.endswith(".md")
}

# Directory containing task files
task_dir = "tasks"
if not os.path.exists(task_dir):
    raise FileNotFoundError(f"Task directory '{task_dir}' does not exist.")

task_files = [os.path.join(task_dir, file) for file in os.listdir(task_dir) if file.endswith(".md")]

# Iterate over models, styles, and tasks
try:
    for language_model in models:
        for style_name, prompt_file in prompt_styles.items():
            # Read the system prompt from the .md file
            with open(prompt_file, "r") as file:
                system_prompt = file.read().strip()
            for task_file in task_files:
                with open(task_file, "r") as file:
                    task_definition = file.read().strip()
                try:
                    print(f"Processing {task_file} with {language_model} and {style_name}...")
                    results = prompt(language_model, system_prompt, task_definition)
                except Exception as e:
                    print(f"Error processing {task_file} with {language_model} and {style_name}: {e}")
                    continue
                # Save results to a file
                save_to_file(language_model, style_name, task_definition, results)
except KeyboardInterrupt:
    print("\nProgram interrupted by user. Exiting...")