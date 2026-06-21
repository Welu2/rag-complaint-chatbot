from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def load_embedding_model():

    return SentenceTransformer(MODEL_NAME)


def create_embeddings(model, texts):

    return model.encode(
        texts,
        batch_size=64,
        show_progress_bar=True
    )