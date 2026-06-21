from src.chunking import chunk_text


def test_chunking():

    text = "hello world " * 1000

    chunks = chunk_text(text)

    assert len(chunks) > 1