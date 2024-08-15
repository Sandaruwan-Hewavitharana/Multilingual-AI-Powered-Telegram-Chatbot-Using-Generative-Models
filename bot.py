# Import packages
from deep_translator import GoogleTranslator
import telebot
import google.generativeai as genai

bot = telebot.TeleBot("TELEGRAM-API", parse_mode=None) # You can set parse_moed by defualt.HTML or MARKDOWN
genai.configure(api_key="GEMINI-API")

# Set up the model
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)
convo = model.start_chat(history=[
])

print("System Online...")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    print("message : "+str(message.text))
    messages = message.text
    si_to_en = GoogleTranslator(source='auto',target='en').translate(messages)
    convo.send_message(si_to_en)
    response = convo.last.text
    en_to_si = GoogleTranslator(source='auto',target='si').translate(response)
    bot.reply_to(message, en_to_si)
    print("response : "+en_to_si)

bot .infinity_polling()
