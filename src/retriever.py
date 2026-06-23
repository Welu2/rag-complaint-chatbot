import pickle
import faiss
import numpy as np

from .embeddings import (
    load_embedding_model,
    create_embeddings,
)


class ComplaintRetriever:

    def __init__(
        self,
        index_path="vector_store/complaints.index",
        metadata_path="vector_store/metadata.pkl",
    ):

        self.index = faiss.read_index(index_path)

        with open(metadata_path, "rb") as f:
            self.metadata = pickle.load(f)

        self.embedding_model = (
            load_embedding_model()
        )

    def retrieve(
        self,
        query,
        k=5,
    ):

        query_embedding = create_embeddings(
            self.embedding_model,
            [query]
        )

        distances, indices = self.index.search(
            np.array(query_embedding),
            k
        )

        results = []

        for idx in indices[0]:

            if idx < len(self.metadata):

                results.append(
                    self.metadata[idx]
                )

        return results