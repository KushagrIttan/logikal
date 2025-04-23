import google.generativeai as genai

genai.configure(api_key="AIzaSyCDAo1rRwJp63CJpHfgL9gpzJWoD4KNb4I")

def generate_text(prompt, model_name="gemini-2.0-flash", temperature=0.9, max_output_tokens=1024):
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_output_tokens,
            ),
        )
        return response.text
    except Exception as e:
        print(f"An error occurred: {e}")
        return "error"

def chat_bot_category(inp):
    response = generate_text(f"i will enter an item, classify it in one of the following:[weapons,drugs,alcohol,dangerous chemicals,animals] : {inp}")
    # print(type(response))
    return response

# if __name__ == "__main__":
#     while True:
#         q = input("You: ")
#         if q.lower() in ["exit", "quit"]:
#             print("Goodbye!")
#             break
#         response = chat_bot(q)
#         print("ChatGPT:", response)