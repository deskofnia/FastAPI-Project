from sentence_transformers import CrossEncoder, SentenceTransformer

msmarco_model = SentenceTransformer("msmarco-distilbert-base-tas-b")
multi_qa_mpnet_model = SentenceTransformer("multi-qa-mpnet-base-dot-v1")
cross_encoder_model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
