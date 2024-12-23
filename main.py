from openai import OpenAI
from google.colab import userdata
OPENAI_API_KEY = userdata.get('OPENAI_API_KEY')
client = OpenAI(api_key=OPENAI_API_KEY)

def prompt(language_model, system_prompt, task_definition):

  response = client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
          {"role": "system", "content": system_prompt},
          {
              "role": "user",
              "content": task_definition
          }
      ]
  )
  return response.choices[0].message.content



import datetime

def save_to_file(language_model, style_name, task_definition, results):
    filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    filemodelname = f"{language_model}_{style_name}_"  # Added style_name here
    file = open("./" + filemodelname + filename + ".txt", 'w')
    file_contents = f"""
    Language Model: {language_model}
    System Prompt: {prompt_styles[style_name]}
    Task Definition: {task_definition}
    Results: {results}
    """
    file.write(file_contents)
    file.close()