import openai
import os
import datetime

# Set up OpenAI API key from an environment variable for security
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    raise ValueError("OpenAI API key not found. Set the OPENAI_API_KEY environment variable.")
openai.api_key = OPENAI_API_KEY

def prompt(language_model, system_prompt, task_definition):
    try:
        response = openai.ChatCompletion.create(
            model=language_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": task_definition}
            ]
        )
        return response.choices[0].message.content
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