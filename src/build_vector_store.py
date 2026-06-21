import pandas as pd

from sampling import stratified_sample
from chunking import chunk_text
from embeddings import (
    load_embedding_model,
    create_embeddings,
)
from vector_store import (
    create_faiss_index,
    save_index,
    save_metadata,
)

DATA_PATH = "data/processed/filtered_complaints.csv"


def main():

    df = pd.read_csv(DATA_PATH)

    sampled_df = stratified_sample(df)

    documents = []

    for _, row in sampled_df.iterrows():

        chunks = chunk_text(
            row["Consumer complaint narrative"]
        )

        for idx, chunk in enumerate(chunks):

            documents.append(
                {
                    "text": chunk,
                    "complaint_id": row["Complaint ID"],
                    "product": row["Product"],
                    "chunk_id": idx,
                }
            )

    model = load_embedding_model()

    embeddings = create_embeddings(
        model,
        [d["text"] for d in documents],
    )

    index = create_faiss_index(embeddings)

    save_index(
        index,
        "vector_store/complaints.index"
    )

    save_metadata(
        documents,
        "vector_store/metadata.pkl"
    )

    print(
        f"Stored {len(documents)} chunks."
    )


if __name__ == "__main__":
    main()