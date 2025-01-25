# critic.py
from openai import OpenAI
import os

def evaluate_todo(client, todo_output):
    """
    Evaluates a todo list output using GPT-4 as a critic.
    
    Args:
        client: OpenAI client instance
        todo_output: The generated todo list to evaluate
        
    Returns:
        str: Comma-separated scores (e.g., "4,3,5,4,2")
        None: If evaluation fails
    """
    critic_prompt = """Rate this todo list from 1-5 on each criteria:
1. Task clarity: Are items clearly defined?
2. Actionability: Can tasks be acted on immediately?
3. Priority clarity: Is importance/urgency clear?
4. Timeframes: Are deadlines reasonable?
5. Task breakdown: Are complex items properly subdivided?

Return only numbers separated by commas (e.g. 4,3,5,4,2)"""

    try:
        completion = client.chat.completions.create(
            model="gpt-4",  # Using GPT-4 for evaluation as it tends to be more consistent
            messages=[
                {"role": "system", "content": critic_prompt},
                {"role": "user", "content": todo_output}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Critic error: {e}")
        return None