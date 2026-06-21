import faiss
import pickle


def create_faiss_index(embeddings):

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    return index


def save_index(index, path):

    faiss.write_index(index, path)


def save_metadata(metadata, path):

    with open(path, "wb") as f:
        pickle.dump(metadata, f)