from src.rag_pipeline import (
    ComplaintRAG
)

rag = ComplaintRAG()

questions = [
    "Why are customers disputing credit card charges?",
    "What mortgage servicing issues are common?",
    "Why are customers unhappy with debt collection?",
    "What billing problems appear frequently?",
    "What complaints are made about loan payments?",
]

for question in questions:

    result = rag.answer_question(
        question
    )

    print("\n")
    print("=" * 80)

    print("QUESTION:")
    print(question)

    print("\nANSWER:")
    print(result["answer"])

    print("\nSOURCES:")

    for source in result["sources"][:2]:

        print(
            source["text"][:200]
        )