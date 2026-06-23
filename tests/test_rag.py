from src.rag_pipeline import (
    ComplaintRAG
)


def test_rag_pipeline():

    rag = ComplaintRAG()

    result = rag.answer_question(
        "Why are customers disputing credit card charges?"
    )

    assert isinstance(
        result["answer"],
        str
    )

    assert len(
        result["sources"]
    ) > 0