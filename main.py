#==============================================================================
# TODO LIST GENERATOR AND EVALUATOR 
# Generates and evaluates todo lists using various language models and prompts
#==============================================================================

from openai import OpenAI
import os
import datetime
from dotenv import load_dotenv
import csv
from critic import evaluate_todo
import argparse
import glob
import json
from tqdm import tqdm
import shutil

#------------------------------------------------------------------------------
# INITIALIZATION AND ENVIRONMENT SETUP
#------------------------------------------------------------------------------

load_dotenv()
client = OpenAI()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
  raise ValueError("OpenAI API key not found. Ensure it's in the .env file.")

#------------------------------------------------------------------------------
# DIRECTORY AND FILE MANAGEMENT 
#------------------------------------------------------------------------------

def get_next_id():
   """Get next available ID from 001-999"""
   try:
       with open('last_id.json', 'r') as f:
           last_id = json.load(f)['id']
   except FileNotFoundError:
       last_id = 0
   
   next_id = (last_id + 1) % 1000
   with open('last_id.json', 'w') as f:
       json.dump({'id': next_id}, f)
   
   return f"{next_id:03d}"


def setup_directory_structure(clear=False):
    """Creates/manages directory structure for the project."""
    required_dirs = ['prompts', 'tasks', 'output']
    created = []
    existed = []
    
    if clear and os.path.exists('output'):
        shutil.rmtree('output')
        print("Cleared output directory")
    
    for dir_name in required_dirs:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            created.append(dir_name)
        else:
            existed.append(dir_name)

    # Example files only created if directories are newly created
    if 'prompts' in created:
        example_prompt = """You are a todo list generator. Create clear, actionable todo lists."""
        with open(os.path.join('prompts', 'example_prompt.md'), 'w') as f:
            f.write(example_prompt)
    
    if 'tasks' in created:
        example_task = """Create a todo list for cleaning the house."""
        with open(os.path.join('tasks', 'example_task.md'), 'w') as f:
            f.write(example_task)

    if created:
        print(f"Created directories: {', '.join(created)}")
    if existed:
        print(f"Using existing directories: {', '.join(existed)}")


#------------------------------------------------------------------------------
# TODO LIST GENERATION
#------------------------------------------------------------------------------

def prompt(language_model, system_prompt, task_definition):
   """Generates a todo list using specified language model and prompts."""
   try:
       completion = client.chat.completions.create(
           model=language_model,
           store=True,
           messages=[
               {"role": "system", "content": system_prompt},
               {"role": "user", "content": task_definition}
           ]
       )
       return completion.choices[0].message.content
   except Exception as e:
       print(f"Error while generating prompt: {e}")
       return ""

#------------------------------------------------------------------------------
# OUTPUT AND ANALYSIS
#------------------------------------------------------------------------------

def save_to_file(language_model, style_name, task_filename, task_definition, results, scores=None):
   """Saves the complete output (todo list and metadata) to a text file."""
   file_id = get_next_id()
   timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
   task_name = os.path.splitext(os.path.basename(task_filename))[0]
   filename = f"{file_id}_{task_name}_{style_name}_{language_model}_{timestamp}.txt"
   output_dir = "output"
   os.makedirs(output_dir, exist_ok=True)
   filepath = os.path.join(output_dir, filename)
   
   file_contents = f"""
Language Model: {language_model}
System Prompt: {style_name}
Task File: {task_filename}
Task Definition: {task_definition}
Results: {results}
"""
   if scores:
       file_contents += f"Scores: {scores}\n"
       
   with open(filepath, "w") as file:
       file.write(file_contents)
   return filename

def save_scores_csv(output_filename, scores_string, total_score):
   """Saves and organizes evaluation scores in CSV file."""
   scores_data = []
   
   if os.path.exists('analysis_scores.csv'):
       with open('analysis_scores.csv', 'r') as f:
           reader = csv.DictReader(f)
           scores_data = list(reader)
   
   scores_data.append({
       'Output File': output_filename,
       'Score String': scores_string,
       'Total Score': total_score,
       'Prompt': output_filename.split('_')[2]
   })
   
   grouped_data = {}
   for row in scores_data:
       prompt = row['Prompt']
       if prompt not in grouped_data:
           grouped_data[prompt] = []
       grouped_data[prompt].append(row)
   
   for prompt in grouped_data:
       grouped_data[prompt].sort(key=lambda x: float(x['Total Score']), reverse=True)
   
   with open('analysis_scores.csv', 'w', newline='') as f:
       writer = csv.DictWriter(f, fieldnames=['Prompt', 'Output File', 'Score String', 'Total Score'])
       writer.writeheader()
       for prompt in sorted(grouped_data.keys()):
           for row in grouped_data[prompt]:
               writer.writerow(row)

#------------------------------------------------------------------------------
# MAIN EXECUTION FUNCTIONS
#------------------------------------------------------------------------------

def run_generation():
   """Runs todo list generation with progress bar."""
   print("Running todo list generation...")
   
   models = ["gpt-4o-mini", "gpt-3.5-turbo"]
   prompt_dir = "prompts"
   if not os.path.exists(prompt_dir):
       raise FileNotFoundError(f"Prompt directory '{prompt_dir}' does not exist.")

   prompt_styles = {
       os.path.splitext(filename)[0]: os.path.join(prompt_dir, filename)
       for filename in os.listdir(prompt_dir) if filename.endswith(".md")
   }

   task_dir = "tasks"
   if not os.path.exists(task_dir):
       raise FileNotFoundError(f"Task directory '{task_dir}' does not exist.")

   task_files = [os.path.join(task_dir, file) for file in os.listdir(task_dir) if file.endswith(".md")]

   total_tasks = len(models) * len(prompt_styles) * len(task_files)
   
   try:
       with tqdm(total=total_tasks, desc="Generating todo lists") as pbar:
           for language_model in models:
               for style_name, prompt_file in prompt_styles.items():
                   with open(prompt_file, "r") as file:
                       system_prompt = file.read().strip()
                   
                   for task_file in task_files:
                       with open(task_file, "r") as file:
                           task_definition = file.read().strip()
                       
                       try:
                           results = prompt(language_model, system_prompt, task_definition)
                           save_to_file(language_model, style_name, task_file, task_definition, results)
                           pbar.update(1)
                       except Exception as e:
                           print(f"\nError: {e}")
                           pbar.update(1)

   except KeyboardInterrupt:
       print("\nProgram interrupted by user. Exiting...")

def run_critic():
   """Runs critic evaluation on existing output files."""
   print("Running critic evaluation...")
   
   with open("analysis_scores.csv", 'w', newline='') as f:
       writer = csv.writer(f)
       writer.writerow(['Output File', 'Score String', 'Total Score'])
   
   output_files = glob.glob('output/*.txt')
   
   with tqdm(total=len(output_files), desc="Evaluating outputs") as pbar:
       for output_file in output_files:
           try:
               with open(output_file, 'r') as f:
                   content = f.read()
                   results_section = content.split('Results:')[1].split('Scores:')[0].strip()
               
               scores = evaluate_todo(client, results_section)
               if scores:
                   score_list = [int(x) for x in scores.split(',')]
                   total_score = sum(score_list)
                   save_scores_csv(os.path.basename(output_file), scores, total_score)
               pbar.update(1)
               
           except Exception as e:
               print(f"\nError processing {output_file}: {e}")
               pbar.update(1)

#------------------------------------------------------------------------------
# SCRIPT ENTRY POINT
#------------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Todo List Generator and Critic')
    parser.add_argument('mode', choices=['generate', 'evaluate'],
                       help='Mode to run: "generate" for todo list generation, "evaluate" for running critic')
    parser.add_argument('--clear', action='store_true', help='Clear all directories before running')
    
    args = parser.parse_args()
    setup_directory_structure(args.clear)
    
    if args.mode == 'generate':
        run_generation()
    else:
        run_critic()