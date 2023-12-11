# Imports a PyMilvus package:
from pymilvus import (
    connections,
    utility,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection,
)


# Connects to a server:
connections.connect("default", host="localhost", port="19530")


# Creates a collection:
fields = [
    FieldSchema(name="pk", dtype=DataType.INT64, is_primary=True, auto_id=False),
    FieldSchema(name="random", dtype=DataType.DOUBLE),
    FieldSchema(name="embeddings", dtype=DataType.FLOAT_VECTOR, dim=8)
]
schema = CollectionSchema(fields, "hello_milvus is the simplest demo to introduce the APIs")
hello_milvus = Collection("hello_milvus", schema)


# Inserts vectors in the collection:
import random
entities = [
    [i for i in range(3000)],  # field pk
    [float(random.randrange(-20, -10)) for _ in range(3000)],  # field random
    [[random.random() for _ in range(8)] for _ in range(3000)],  # field embeddings
]
# insert_result = hello_milvus.insert(entities)
# hello_milvus.flush()  


# Builds indexes on the entities:
# index = {
#     "index_type": "IVF_FLAT",
#     "metric_type": "L2",
#     "params": {"nlist": 128},
# }
# hello_milvus.create_index("embeddings", index)


# Loads the collection to memory and performs a vector similarity search:
# hello_milvus.load()
# vectors_to_search = entities[-1][-2:]
# search_params = {
#     "metric_type": "L2",
#     "params": {"nprobe": 10},
# }
# result = hello_milvus.search(vectors_to_search, "embeddings", search_params, limit=3, output_fields=["random"])

# print("Results=====", result)


# Performs a vector query:
# result = hello_milvus.query(expr="random > -14", output_fields=["random", "embeddings"])


# # Performs a hybrid search:
# result = hello_milvus.search(vectors_to_search, "embeddings", search_params, limit=3, expr="random > -12", output_fields=["random"])


# # Deletes entities by their primary keys:
expr = f"pk in [{entities[0][0]}, {entities[0][1]}]"
print("Expression------", expr)
hello_milvus.delete(expr)


# # Drops the collection:
# utility.drop_collection("hello_milvus")
