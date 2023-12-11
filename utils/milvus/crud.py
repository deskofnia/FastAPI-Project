from models.milvus.collection.questions import (questions_msmarcos_collection, questions_multi_qa_mpnet_base)
from utils.transformers.models import msmarco_model, multi_qa_mpnet_model


def _insert_questions_to_milvus(
    ans_id: int,
    bot_id: int,
    que_id: int,
    processed_answer_id: int,
    type: int,
    questionList: list[str],
):
    chunk_size = 64
    
    for question in questionList:    
        data = [question]   
        for i in range(0, len(data), chunk_size):
            chunk = data[i : i + chunk_size]    
            msmarco_embeddings = msmarco_model.encode(chunk, normalize_embeddings=True)
            qa_embeddings = multi_qa_mpnet_model.encode(chunk, normalize_embeddings=True)

            try:
                # Do not remove unused variable
                qu_res =  questions_multi_qa_mpnet_base.insert(
                [
                    [ans_id] * len(chunk),
                    [bot_id] * len(chunk),
                    [processed_answer_id] * len(chunk),
                    [que_id] * len(chunk),
                    [type] * len(chunk),
                    qa_embeddings.tolist(),
                ],
                _async=False,
                )
                
                
            except Exception as e:
                # Handle the error condition
                print("Error inserting data outer qu_res:", str(e))
            try:
                # Do not remove unused variable
                msmarcos_response =  questions_msmarcos_collection.insert(
                    [
                        [ans_id] * len(chunk),
                        [bot_id] * len(chunk),
                        [processed_answer_id] * len(chunk),
                        [que_id] * len(chunk),
                        [type] * len(chunk),
                        msmarco_embeddings.tolist(),
                    ],
                    _async=False,
                )
                
            except Exception as e:
                # Handle the error condition
                print("Error inserting data Outer msmarcos:", str(e))


def _bulk_insert_questions_to_milvus(
    ans_id: int,
    bot_id: int,
    que_id: int,
    type: int,
    processed_answers: list[tuple[int,str]],
):
    chunk_size = 64
    for processed_answer_id, processed_question in processed_answers:
        data = [processed_question]
        for i in range(0, len(data), chunk_size):
            chunk = data[i : i + chunk_size]
            msmarco_embeddings = msmarco_model.encode(chunk, normalize_embeddings=True)
            qa_embeddings = multi_qa_mpnet_model.encode(chunk, normalize_embeddings=True)
            try:
                # Do not remove unused variable
                qu_res =  questions_multi_qa_mpnet_base.insert(
                    [
                        [ans_id] * len(chunk),
                        [bot_id] * len(chunk),
                        [processed_answer_id] * len(chunk),
                        [que_id] * len(chunk),
                        [type] * len(chunk),
                        qa_embeddings.tolist(),
                    ],
                    _async=True,
                )
            except Exception as e:
                # Handle the error condition
                print("Error inserting data Outer qa_mpnet:", str(e))
            try:
                # Do not remove unused variable
                msmarcos_response =  questions_msmarcos_collection.insert(
                    [
                        [ans_id] * len(chunk),
                        [bot_id] * len(chunk),
                        [processed_answer_id] * len(chunk),
                        [que_id] * len(chunk),
                        [type] * len(chunk),
                        msmarco_embeddings.tolist(),
                    ],
                    _async=True,
                )
            except Exception as e:
                # Handle the error condition
                print("Error inserting data Outer msmarcos:", str(e))
           
            # print(msmarcos_response.err_count,"msmarcos_response.err_count")
