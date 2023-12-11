from transformers import pipeline

chatbot = pipeline("text-generation")


def chat(message: str):
    response = chatbot(message, max_length=50, num_return_sequences=1)[0]['generated_text']
    return {"response": response}