import json
import os
from pathlib import Path
from typing import Dict, List, Union
from openai import OpenAI
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

class TaskListProcessor:
    def __init__(self):
        self.task_list_dir = Path("task_list_results")
        self.scoring_dir = Path("task_list_result_scoring")
        self.system_prompt = """You are a to-do-list evaluation critic. Your role is to review the to-do lists written by another large language model and make sure they meet the following criteria:
1. Time-Bound but Flexible Timing
2. Energy-State Matching
3. Sensory-Aware Task Grouping
4. Momentum-Based Sequencing
5. Concrete Next Actions
6. Built-In Recovery Planning
7. Overall Synergy Across Tasks

Please review the following to-do list and any supporting documents used to produce it, and give the following for **each** point above:
1. a 1-5 score
2. true or false
3. a 1-5 score
4. true or false
5. true or false
6. a 1-5 score
7. a 1-5 score

Please present your evaluations as a list from 1-7, exactly as above. **Do not label the points**; simply use the same list of numbers, as this output will be parsed by a script, so it is important to keep the format exactly."""
        
        # Create necessary directories
        self.task_list_dir.mkdir(exist_ok=True)
        self.scoring_dir.mkdir(exist_ok=True)

    def parse_task_list(self, content: str) -> Dict:
        """
        Parse the task list content and extract tasks.
        Implement custom parsing logic based on your file format.
        """
        # This is a basic implementation - modify based on your actual file format
        tasks = []
        current_task = ""
        
        for line in content.split('\n'):
            line = line.strip()
            if line.startswith(('- ', '* ', '• ')):
                if current_task:
                    tasks.append(current_task)
                current_task = line[2:]
            elif line and current_task:
                current_task += f" {line}"
        
        if current_task:
            tasks.append(current_task)
            
        return {"tasks": tasks}

    def process_files(self, input_dir: str) -> None:
        """Process all task list files in the input directory."""
        input_path = Path(input_dir)
        
        for file_path in input_path.glob('*.txt'):  # Adjust file extension as needed
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Parse and convert to JSON
                task_data = self.parse_task_list(content)
                output_file = self.task_list_dir / f"{file_path.stem}_parsed.json"
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(task_data, f, indent=2)
                
                print(f"Processed {file_path.name} -> {output_file.name}")
                
            except Exception as e:
                print(f"Error processing {file_path.name}: {e}")

    def evaluate_task_list(self, task_list: Dict) -> str:
        """Send task list to OpenAI for evaluation."""
        try:
            response = client.chat.completions.create(
                model="gpt-4",  # or your preferred model
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": json.dumps(task_list, indent=2)}
                ]
            )
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error during evaluation: {e}")
            return ""

    def process_evaluations(self) -> None:
        """Process all task lists and generate evaluations."""
        for json_file in self.task_list_dir.glob('*.json'):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    task_list = json.load(f)
                
                # Get evaluation
                evaluation = self.evaluate_task_list(task_list)
                
                # Save evaluation
                output_file = self.scoring_dir / f"{json_file.stem}_evaluation.txt"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(evaluation)
                
                print(f"Evaluated {json_file.name} -> {output_file.name}")
                
            except Exception as e:
                print(f"Error evaluating {json_file.name}: {e}")

    def parse_evaluation_scores(self, evaluation: str) -> Dict[str, Union[int, bool]]:
        """Parse the evaluation text into structured data."""
        lines = evaluation.strip().split('\n')
        scores = {}
        
        criteria = [
            "Time-Bound but Flexible Timing",
            "Energy-State Matching",
            "Sensory-Aware Task Grouping",
            "Momentum-Based Sequencing",
            "Concrete Next Actions",
            "Built-In Recovery Planning",
            "Overall Synergy Across Tasks"
        ]
        
        for i, line in enumerate(lines):
            if i < len(criteria):
                # Extract score or boolean based on the criteria
                values = re.findall(r'\d+|true|false', line.lower())
                if values:
                    if criteria[i] in ["Concrete Next Actions"]:
                        scores[criteria[i]] = values[0] == 'true'
                    else:
                        scores[criteria[i]] = int(values[0]) if values[0].isdigit() else values[0] == 'true'
        
        return scores

    def generate_summary_report(self) -> None:
        """Generate a summary report of all evaluations."""
        all_scores = []
        
        for eval_file in self.scoring_dir.glob('*_evaluation.txt'):
            try:
                with open(eval_file, 'r', encoding='utf-8') as f:
                    evaluation = f.read()
                
                scores = self.parse_evaluation_scores(evaluation)
                scores['file_name'] = eval_file.stem
                all_scores.append(scores)
                
            except Exception as e:
                print(f"Error processing evaluation {eval_file.name}: {e}")

        # Generate summary report
        summary_file = Path("evaluation_summary.json")
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(all_scores, f, indent=2)
        
        print(f"Generated summary report: {summary_file}")

def main():
    processor = TaskListProcessor()
    
    # Process input files
    print("Processing input files...")
    processor.process_files("input_tasks")  # Adjust directory name as needed
    
    # Generate evaluations
    print("\nGenerating evaluations...")
    processor.process_evaluations()
    
    # Create summary report
    print("\nGenerating summary report...")
    processor.generate_summary_report()
    
    print("\nProcessing complete!")

if __name__ == "__main__":
    main()