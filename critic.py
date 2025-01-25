#==============================================================================
# CRITIC MODULE
# Evaluates generated todo lists using defined criteria
#==============================================================================

from openai import OpenAI
import os

def evaluate_todo(client, todo_output):
    """Evaluates a todo list output using GPT-4 as a critic."""
    critic_prompt = """Rate this todo list from 1-5 on each criteria:
1. Task clarity: Are items clearly defined?
2. Actionability: Can tasks be acted on immediately?
3. Priority clarity: Is importance/urgency clear?
4. Timeframes: Are deadlines reasonable?
5. Task breakdown: Are complex items properly subdivided?

Return only numbers separated by commas (e.g. 4,3,5,4,2)"""

    try:
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": critic_prompt},
                {"role": "user", "content": todo_output}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Critic error: {e}")
        return None

#==============================================================================
# ANALYSIS FUNCTION
# Evaluates which prompt/model combo is best
#==============================================================================

def analyze_scores(client, csv_content):
    """Analyzes the scores.csv to determine the most effective prompt and model combinations."""
    analysis_prompt = """You are analyzing the results of different todo list prompts and models. The data shows scores for different combinations, where each row contains:
    - Prompt: The prompt style used
    - Output File: Contains the model name used (e.g., gpt-4o-mini)
    - Score String: Five comma-separated scores (1-5) for:
        1. Task clarity
        2. Actionability
        3. Priority clarity
        4. Timeframes
        5. Task breakdown
    - Total Score: Sum of the individual scores

    Analyze this data and tell me:
    1. Which prompt consistently produces the best results?
    2. Are there any notable patterns in what makes certain prompts more effective?
    3. How do different models perform with these prompts?

    Keep your analysis focused and data-driven."""

    try:
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": analysis_prompt},
                {"role": "user", "content": csv_content}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Analysis error: {e}")
        return None