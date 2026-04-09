from typing import List, Tuple

from pymilvus import (
    Collection,
    CollectionSchema,
    DataType,
    FieldSchema,
    connections,
    utility,
)

from .config import (
    MILVUS_COLLECTION,
    MILVUS_HOST,
    MILVUS_INDEX_TYPE,
    MILVUS_METRIC_TYPE,
    MILVUS_NLIST,
    MILVUS_NPROBE,
    MILVUS_PORT,
    VECTOR_DIM,
)


class VectorStore:
    def __init__(self, dim: int = VECTOR_DIM):
        self.dim = dim
        self.collection_name = MILVUS_COLLECTION
        connections.connect(alias="default", host=MILVUS_HOST, port=MILVUS_PORT)
        self.collection = self._get_or_create_collection()
        self.collection.load()

    def _get_or_create_collection(self) -> Collection:
        if utility.has_collection(self.collection_name):
            return Collection(self.collection_name)

        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=self.dim),
            FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=65535),
        ]
        schema = CollectionSchema(fields, description="Knowledge document vectors")
        collection = Collection(self.collection_name, schema)

        index_params = {
            "index_type": MILVUS_INDEX_TYPE,
            "metric_type": MILVUS_METRIC_TYPE,
            "params": {"nlist": MILVUS_NLIST},
        }
        if MILVUS_INDEX_TYPE.upper() == "FLAT":
            index_params["params"] = {}
        collection.create_index(field_name="embedding", index_params=index_params)
        return collection

    def add(self, embedding: List[float], text: str):
        # 添加单条向量数据到 Milvus 集合
        # 参数 embedding: 文本的向量表示，维度为 self.dim
        # 参数 text: 原始文本内容
        if not embedding or not text:
            return
        row = {"embedding": embedding, "content": text}
        self.collection.insert([row])
        self.collection.flush()

    def search(self, query_emb: List[float], k: int = 3) -> List[Tuple[str, float]]:
        search_params = {"metric_type": MILVUS_METRIC_TYPE, "params": {"nprobe": MILVUS_NPROBE}}
        if MILVUS_INDEX_TYPE.upper() == "FLAT":
            search_params = {"metric_type": MILVUS_METRIC_TYPE, "params": {}}

        results = self.collection.search(
            data=[query_emb],
            anns_field="embedding",
            param=search_params,
            limit=k,
            output_fields=["content"],
        )
        hits = results[0] if results else []
        output: List[Tuple[str, float]] = []
        for hit in hits:
            if hasattr(hit, "entity") and hit.entity is not None:
                text = hit.entity.get("content")
            else:
                text = hit.get("content")
            output.append((text, float(hit.distance)))
        return output
