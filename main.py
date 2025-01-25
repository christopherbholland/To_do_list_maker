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

#------------------------------------------------------------------------------
# INITIALIZATION AND ENVIRONMENT SETUP
#------------------------------------------------------------------------------

# Load environment variables from the .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI()

# Set up OpenAI API key from the environment variable
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
   raise ValueError("OpenAI API key not found. Ensure it's in the .env file.")

#------------------------------------------------------------------------------
# DIRECTORY AND FILE MANAGEMENT
#------------------------------------------------------------------------------

def setup_directory_structure():
   """
   Creates the necessary directory structure for the project if it doesn't exist.
   Returns a tuple of (created_dirs, already_existed) for feedback to user.
   """
   required_dirs = ['prompts', 'tasks', 'output']
   created = []
   existed = []
   
   for dir_name in required_dirs:
       if not os.path.exists(dir_name):
           os.makedirs(dir_name)
           created.append(dir_name)
       else:
           existed.append(dir_name)
   
   # Create example prompt and task files if prompts directory is empty
   if 'prompts' in created:
       example_prompt = """You are a todo list generator. Create clear, actionable todo lists."""
       with open(os.path.join('prompts', 'example_prompt.md'), 'w') as f:
           f.write(example_prompt)
   
   if 'tasks' in created:
       example_task = """Create a todo list for cleaning the house."""
       with open(os.path.join('tasks', 'example_task.md'), 'w') as f:
           f.write(example_task)

   # Print feedback
   if created:
       print(f"Created directories: {', '.join(created)}")
   if existed:
       print(f"Using existing directories: {', '.join(existed)}")

#------------------------------------------------------------------------------
# TODO LIST GENERATION
#------------------------------------------------------------------------------

def prompt(language_model, system_prompt, task_definition):
   """
   Generates a todo list using specified language model and prompts.
   
   Args:
       language_model: The model to use (e.g., "gpt-4")
       system_prompt: The system instructions
       task_definition: The user's task input
       
   Returns:
       str: Generated todo list
       str: Empty string if generation fails
   """
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
   """
   Saves the complete output (todo list and metadata) to a text file.
   """
   timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
   task_name = os.path.splitext(os.path.basename(task_filename))[0]
   filename = f"{task_name}_{style_name}_{language_model}_{timestamp}.txt"
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
   print(f"Results saved to {filepath}")
   return filename

def save_scores_csv(output_filename, scores_string, total_score):
   """
   Saves evaluation scores to a CSV file for easy analysis.
   
   Args:
       output_filename: Name of the corresponding output file
       scores_string: Comma-separated scores from critic
       total_score: Sum of individual scores
   """
   csv_file = "analysis_scores.csv"
   file_exists = os.path.isfile(csv_file)
   
   with open(csv_file, 'a', newline='') as f:
       writer = csv.writer(f)
       if not file_exists:
           writer.writerow(['Output File', 'Score String', 'Total Score'])
       writer.writerow([output_filename, scores_string, total_score])

#------------------------------------------------------------------------------
# MAIN EXECUTION FUNCTIONS
#------------------------------------------------------------------------------

def run_generation():
   """Runs the todo list generation phase"""
   print("Running todo list generation...")
   
   # Define models to test
   models = ["gpt-4", "gpt-3.5-turbo", "gpt-4-0125-preview"]

   # Set up directory paths and validate
   prompt_dir = "prompts"
   if not os.path.exists(prompt_dir):
       raise FileNotFoundError(f"Prompt directory '{prompt_dir}' does not exist.")

   # Load prompt styles from files
   prompt_styles = {
       os.path.splitext(filename)[0]: os.path.join(prompt_dir, filename)
       for filename in os.listdir(prompt_dir) if filename.endswith(".md")
   }

   # Load task files
   task_dir = "tasks"
   if not os.path.exists(task_dir):
       raise FileNotFoundError(f"Task directory '{task_dir}' does not exist.")

   task_files = [os.path.join(task_dir, file) for file in os.listdir(task_dir) if file.endswith(".md")]

   # Main generation loop
   try:
       for language_model in models:
           for style_name, prompt_file in prompt_styles.items():
               # Read the system prompt
               with open(prompt_file, "r") as file:
                   system_prompt = file.read().strip()
               
               for task_file in task_files:
                   with open(task_file, "r") as file:
                       task_definition = file.read().strip()
                   
                   try:
                       print(f"Processing {task_file} with {language_model} and {style_name}...")
                       results = prompt(language_model, system_prompt, task_definition)
                       save_to_file(language_model, style_name, task_file, task_definition, results)
                           
                   except Exception as e:
                       print(f"Error processing {task_file}: {e}")
                       continue

   except KeyboardInterrupt:
       print("\nProgram interrupted by user. Exiting...")

def run_critic():
   """Runs only the critic evaluation on existing output files"""
   print("Running critic evaluation on existing outputs...")
   
   # Clear existing analysis file
   with open("analysis_scores.csv", 'w', newline='') as f:
       writer = csv.writer(f)
       writer.writerow(['Output File', 'Score String', 'Total Score'])
   
   # Get all output files
   output_files = glob.glob('output/*.txt')
   
   for output_file in output_files:
       try:
           # Read the results from the file
           with open(output_file, 'r') as f:
               content = f.read()
               # Extract just the Results section
               results_section = content.split('Results:')[1].split('Scores:')[0].strip()
           
           # Run critic on the results
           print(f"Evaluating {output_file}...")
           scores = evaluate_todo(client, results_section)
           if scores:
               score_list = [int(x) for x in scores.split(',')]
               total_score = sum(score_list)
               save_scores_csv(os.path.basename(output_file), scores, total_score)
               print(f"Evaluated {output_file}")
           
       except Exception as e:
           print(f"Error processing {output_file}: {e}")

#------------------------------------------------------------------------------
# SCRIPT ENTRY POINT
#------------------------------------------------------------------------------

if __name__ == "__main__":
   setup_directory_structure()
   parser = argparse.ArgumentParser(description='Todo List Generator and Critic')
   parser.add_argument('mode', choices=['generate', 'evaluate'],
                      help='Mode to run: "generate" for todo list generation, "evaluate" for running critic')
   
   args = parser.parse_args()
   
   if args.mode == 'generate':
       run_generation()
   else:
       run_critic()