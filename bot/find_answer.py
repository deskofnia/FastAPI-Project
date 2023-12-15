from transformers import pipeline

async def find_answer(story, question) -> tuple[str, int, int]:
    model_name = "deepset/bert-large-uncased-whole-word-masking-squad2"

    nlp = pipeline("question-answering", model=model_name, tokenizer=model_name)
    QA_input = {"question": question, "context": story}
    res = nlp(QA_input)

    sentence = story[res["start"] : res["end"]].strip()

    return sentence, res["start"], res["end"]
