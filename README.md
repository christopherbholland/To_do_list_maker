# Todo List Generator and Evaluator

A Python tool that generates and evaluates todo lists using OpenAI's language models.

## Features

- Generate todo lists using multiple LLMs (GPT-4, GPT-3.5-turbo)
- Evaluate lists on clarity, actionability, priority, timeframes, task breakdown
- Track performance with detailed CSV analytics
- Progress visualization during generation/evaluation

## Setup

1. Clone repository
2. Install dependencies: `pip install -r requirements.txt`
3. Add OpenAI API key to `.env` file: `OPENAI_API_KEY=your_key_here`

## Usage

Generate todo lists:
```bash
python main.py generate
```

Evaluate existing lists:
```bash
python main.py evaluate
```

Clear output directory:
```bash
python main.py generate --clear # clears outputs generated by the LLM
python main.py evaluate --clear # clears evaluations
```

## Directory Structure

- `/prompts`: System prompts for LLMs
- `/tasks`: Input tasks to generate lists for
- `/output`: Generated lists and evaluations

## Output Format

- Todo lists saved as text files with unique IDs
- Evaluation scores stored in `analysis_scores.csv`
- Results grouped by prompt and sorted by score

## Requirements

- Python 3.8+
- OpenAI API key
- Dependencies in requirements.txt