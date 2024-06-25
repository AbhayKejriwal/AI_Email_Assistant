import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part, FinishReason
import vertexai.preview.generative_models as generative_models

def generate(text1):
  vertexai.init(project="delta-era-422106-j1", location="asia-south1")
  model = GenerativeModel("gemini-1.5-pro-preview-0409")
  responses = model.generate_content(
      [text1],
      generation_config=generation_config,
      safety_settings=safety_settings,
      stream=True,
  )
  final_response = ""
  for response in responses:
    # print(response.text, end="")
    final_response += response.text
  return final_response

def gen_prompt(message):
  prompt = """You are a personal email assistant. Your job is to know my priorities, preferences and requirements about my email and filter out the content and display it to me in the set format.

#Preferences & Special Instructions: \"I have subscribed to newsletters in my mail. However, they contain sponsored contents. I want you to remove those.\"

The email message is provide in HTML format and the output should be strictly returned in the specified JSON format with no other prefix or suffix. Filter the right content according to my requirements, provide a brief summary of the mail content and categorize the mail. The various categories are: \"Important\", \"NotImportant\", \"Spam\" and \"CannotClasify\"(not enough data in preferences to categorize the mail).

OUTPUT FORMAT:
{
\"Summary\": \"<summary_of_the_mail>\",
\"Category\": \"<category_of_the_mail>\"
}

EMAIL MESSAGE in HTML format:
\"\"\"""" + message + """\"\"\""""
  
  return prompt
#\"Filtered_Message\": \"<filtered_content_of_the_mail_based_on_my_preferences>\",
generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}

safety_settings = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}

if __name__ == "__main__":
  with open("sample.txt", "r") as f:
    message = f.read()
  prompt = gen_prompt(message)
  generate(prompt)