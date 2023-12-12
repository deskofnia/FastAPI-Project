"""
Asymmetric search:
https://www.sbert.net/examples/applications/semantic-search/README.html#symmetric-vs-asymmetric-semantic-search

Models tuned for cosine-similarity will prefer the retrieval of shorter passages,
while models for dot-product will prefer the retrieval of longer passages.
Depending on your task, you might prefer the one or the other type of model.
"""

import logging

from models.milvus.client import connect_to_milvus
from pymilvus import Collection, CollectionSchema, DataType, FieldSchema
from pymilvus.exceptions import ConnectionNotExistException, MilvusException

logger = logging.getLogger(__name__)


id = FieldSchema(
    name="id",
    dtype=DataType.INT64,
    is_primary=True,
    auto_id=True,
    description="Id",
)

message_vector = FieldSchema(
    name="message_vector",
    dtype=DataType.FLOAT_VECTOR,
    dim=768
)

message = FieldSchema(
    name="message",
    dtype=DataType.STRING,
)


def create_collection(model: str, tries: int = 0) -> Collection | None:
    schema = CollectionSchema(
        fields=[message_vector, message],
        description="chatbot_collection is the simplest demo to introduce the APIs"
    )
    collection_name = "chatbot_collection"
    kwargs = {
        "name": collection_name,
        "schema": schema,
    }
    try:
        collection = Collection(**kwargs)

        if not collection.has_index():
            collection.create_index(
                field_name="message_vector",
                # https://milvus.io/docs/build_index.md
                index_params={
                    "metric_type": "IP",
                    "index_type": "IVF_FLAT",
                    "params": {"nlist": 1024},
                },
            )

        collection.load()

    except ConnectionNotExistException:
        try:
            connect_to_milvus()
        except MilvusException as e:
            logger.error(e)
            if tries < 5:
                return create_collection(model, tries + 1)
            raise e
        return create_collection(model, tries + 1)
    return collection


questions_msmarcos_collection = create_collection("msmarco_distilbert_base_tas_b")
questions_multi_qa_mpnet_base = create_collection("multi_qa_mpnet_base_dot_v1")
