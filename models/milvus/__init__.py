from config import env_variables
from pymilvus import connections as milvus_connections

milvus_alias = "default"


def connect_to_milvus():
    global milvus_alias
    milvus_connections.connect(
        alias=milvus_alias,
        host=env_variables.MILVUS_HOST,
        port=env_variables.MILVUS_PORT,
    )

def disconnect_from_milvus():
    global milvus_alias
    milvus_connections.disconnect(alias=milvus_alias)
