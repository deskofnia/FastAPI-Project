from transformers import pipeline

async def generate_questions(story):
    # Load the question-generation pipeline
    nlp = pipeline("text2text-generation", model="valhalla/t5-base-e2e-qg")

    return nlp(story)
