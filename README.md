# ✨ Todo List Generator & Evaluator ✨

Welcome to an innovative tool that combines the power of AI with todo list generation! This project doesn't just create todo lists – it experiments with different prompting strategies and leverages advanced language models to discover what makes a truly effective task organization system.

## 🌟 What Makes This Special?

Imagine having a laboratory where you can experiment with different AI approaches to task management. That's exactly what this tool provides! By combining various prompting styles with different language models, we can scientifically determine what creates the most effective, actionable, and user-friendly todo lists.

## 🚀 Getting Started

First, make sure you have your OpenAI API key ready and Python installed. Then:

```bash
# Clone the repository
git clone [your-repo-url]

# Install dependencies
pip install -r requirements.txt

# Create a .env file and add your OpenAI API key
echo "OPENAI_API_KEY=your-key-here" > .env
```

## 🎮 How to Use

The system works in three magical stages:

### 1. Generation 🎨
Create todo lists using different prompts and models:
```bash
python main.py generate
```
Want to start fresh? Use:
```bash
python main.py generate --clear
```

### 2. Evaluation 📊
Let AI evaluate the effectiveness of each todo list:
```bash
python main.py evaluate
```
Need to redo evaluation without touching your generated lists?
```bash
python main.py evaluate --clear
```

### 3. Analysis 🔍
Discover which combinations work best:
```bash
python main.py analyze
```

## 📁 Project Structure

The project maintains a clean, organized structure:
- `prompts/`: Your collection of different prompting strategies
- `tasks/`: The task descriptions to generate todo lists for
- `output/`: Where the magic happens - all generated lists and their metadata

## 🎯 Understanding the Evaluation

Each todo list is evaluated on five critical dimensions:
1. Task Clarity: How well-defined are the items?
2. Actionability: Can tasks be acted on immediately?
3. Priority Clarity: Is importance/urgency clear?
4. Timeframes: Are deadlines reasonable?
5. Task Breakdown: Are complex items properly subdivided?

## 🔬 The Science Behind It

The system employs a sophisticated evaluation pipeline:
1. First, it generates todo lists using various prompt-model combinations
2. Then, it evaluates each list using consistent criteria
3. Finally, it analyzes patterns to identify the most effective approaches

## 🎨 Customization

Make it your own! Add new prompts in `prompts/` or new tasks in `tasks/`. Each prompt represents a different style or approach to todo list generation, and each task presents a unique challenge to test these approaches.

## 📈 Getting Insights

After running the complete pipeline, check:
- `analysis_scores.csv`: Raw evaluation data
- `analysis_report_[timestamp].txt`: Detailed analysis of what works best

## 🤝 Contributing

Have ideas for new prompts? Discovered an interesting evaluation criterion? We'd love to see your contributions! Feel free to submit pull requests or open issues with your suggestions.

Remember: The best todo list is one that actually helps people get things done. Let's discover together what makes that happen! ✨